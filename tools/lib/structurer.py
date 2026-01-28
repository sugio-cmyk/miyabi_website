"""
Structurer - AI構造化モジュール
Gemini APIを使用して原稿をJSON形式に構造化
"""
import json
import re
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

try:
    import google.generativeai as genai
except ImportError:
    genai = None


@dataclass
class ArticleJSON:
    """構造化された記事データ"""
    lead: str
    points: dict
    sections: list[dict]
    summary: dict
    raw_json: dict  # 元のJSON全体


class StructurerError(Exception):
    """Structurer関連のエラー"""
    pass


class Structurer:
    """Gemini APIを使用して記事を構造化するクラス"""
    
    DEFAULT_MODEL = "gemini-2.0-flash"
    MAX_RETRIES = 3
    RETRY_DELAY = 2  # seconds
    
    def __init__(
        self,
        api_key: str,
        model: str = None,
        temperature: float = 0.3,
        max_output_tokens: int = 8192,
        prompt_template_path: Optional[str] = None
    ):
        """
        Args:
            api_key: Gemini APIキー
            model: 使用するモデル名
            temperature: 生成温度（低いほど安定）
            max_output_tokens: 最大出力トークン数
            prompt_template_path: プロンプトテンプレートファイルパス
        """
        if genai is None:
            raise StructurerError(
                "google-generativeai package not installed. "
                "Run: pip install google-generativeai"
            )
        
        genai.configure(api_key=api_key)
        self.model_name = model or self.DEFAULT_MODEL
        self.temperature = temperature
        self.max_output_tokens = max_output_tokens
        
        # モデル初期化
        self.model = genai.GenerativeModel(
            self.model_name,
            generation_config=genai.GenerationConfig(
                temperature=self.temperature,
                max_output_tokens=self.max_output_tokens,
                response_mime_type="application/json",
            )
        )
        
        # プロンプトテンプレート読み込み
        self.prompt_template = self._load_prompt_template(prompt_template_path)
    
    def _load_prompt_template(self, path: Optional[str]) -> str:
        """プロンプトテンプレートを読み込む"""
        if path and Path(path).exists():
            return Path(path).read_text(encoding='utf-8')
        
        # デフォルトプロンプト
        return """あなたは記事構造化の専門家です。
以下の記事原稿を、指定されたJSON形式に構造化してください。

## 出力形式
```json
{
  "lead": "リード文（150〜200文字）",
  "points": {
    "title": "この記事のポイント",
    "items": ["ポイント1", "ポイント2", "ポイント3"]
  },
  "sections": [
    {
      "type": "heading",
      "level": 2,
      "text": "見出し"
    },
    {
      "type": "paragraph",
      "text": "段落テキスト"
    },
    {
      "type": "list",
      "items": ["項目1", "項目2"]
    },
    {
      "type": "warning",
      "text": "警告・注意内容"
    },
    {
      "type": "table",
      "headers": ["列1", "列2"],
      "rows": [["セル1", "セル2"]]
    },
    {
      "type": "faq",
      "items": [{"q": "質問?", "a": "回答。"}]
    }
  ],
  "summary": {
    "title": "まとめ",
    "items": ["まとめ1", "まとめ2", "まとめ3", "まとめ4"]
  }
}
```

## ルール
- h2見出しは3〜5個
- 各h2直後には必ずparagraphを配置
- list/table/warning/faqのうち最低2種類を使用
- points.itemsは3項目固定
- summary.itemsは4項目以上

## 記事原稿
"""
    
    def structure(self, content: str, title: str = "") -> ArticleJSON:
        """
        記事本文をJSON構造に変換
        
        Args:
            content: 記事本文（Markdown形式）
            title: 記事タイトル（プロンプトに含める）
            
        Returns:
            ArticleJSON: 構造化された記事データ
            
        Raises:
            StructurerError: API呼び出し失敗、またはJSON解析失敗時
        """
        # プロンプト構築
        prompt = self.prompt_template
        if title:
            prompt += f"\n### タイトル: {title}\n"
        prompt += f"\n{content}"
        
        # リトライ付きでAPI呼び出し
        last_error = None
        for attempt in range(self.MAX_RETRIES):
            try:
                response = self.model.generate_content(prompt)
                raw_text = response.text
                
                # JSON解析
                json_data = self._parse_json(raw_text)
                
                # ArticleJSONオブジェクト作成
                return ArticleJSON(
                    lead=json_data.get('lead', ''),
                    points=json_data.get('points', {}),
                    sections=json_data.get('sections', []),
                    summary=json_data.get('summary', {}),
                    raw_json=json_data
                )
                
            except Exception as e:
                last_error = e
                if attempt < self.MAX_RETRIES - 1:
                    time.sleep(self.RETRY_DELAY * (attempt + 1))
        
        raise StructurerError(f"Gemini API failed after {self.MAX_RETRIES} retries: {last_error}")
    
    def _parse_json(self, raw_text: str) -> dict:
        """
        APIレスポンスからJSONを解析
        コードブロックの除去やエスケープ修正も行う
        """
        text = raw_text.strip()
        
        # コードブロック除去
        if text.startswith('```'):
            # ```json\n...\n``` 形式
            text = re.sub(r'^```(?:json)?\s*\n?', '', text)
            text = re.sub(r'\n?```\s*$', '', text)
        
        # 不正なエスケープを修正
        text = self._repair_json(text)
        
        try:
            return json.loads(text)
        except json.JSONDecodeError as e:
            raise StructurerError(f"Failed to parse JSON: {e}\nRaw text: {text[:500]}...")
    
    def _repair_json(self, text: str) -> str:
        """
        軽微なJSONエラーを修復
        - 末尾カンマ除去
        - アンエスケープされたダブルクォート対策
        """
        # 末尾カンマ除去（配列・オブジェクト）
        text = re.sub(r',(\s*[\]}])', r'\1', text)
        
        return text


if __name__ == "__main__":
    # テスト用
    import os
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key:
        structurer = Structurer(api_key)
        result = structurer.structure("これはテスト記事です。\n\n## 見出し1\n\n本文です。")
        print(json.dumps(result.raw_json, ensure_ascii=False, indent=2))
    else:
        print("GEMINI_API_KEY not set")
