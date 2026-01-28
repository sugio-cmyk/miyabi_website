"""
Generator - HTML生成モジュール
JSONからWordPressブロックHTMLを生成

block_generator.pyの正しいテンプレートを使用
"""
import sys
from pathlib import Path
from typing import Optional

# 既存のblock_generator.pyを参照するためパスを追加
TOOLS_DIR = Path(__file__).parent.parent
if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))

# block_generator.pyのBlockGeneratorをインポートして使用
from block_generator import BlockGenerator as _BlockGenerator


class GeneratorError(Exception):
    """Generator関連のエラー"""
    pass


class Generator:
    """JSONからWordPressブロックHTMLを生成するクラス
    
    block_generator.pyのBlockGeneratorをラップして使用
    """
    
    def __init__(self, cta_template_path: Optional[str] = None):
        """
        Args:
            cta_template_path: CTAテンプレートファイルパス
        """
        self._generator = _BlockGenerator()
        self.cta_template = None
        if cta_template_path and Path(cta_template_path).exists():
            self.cta_template = Path(cta_template_path).read_text(encoding='utf-8')
    
    def generate(
        self,
        article_json: dict,
        include_cta: bool = True
    ) -> str:
        """
        JSONからブロックHTMLを生成
        
        Args:
            article_json: 構造化された記事JSON
            include_cta: CTAを追加するか
            
        Returns:
            str: WordPress用ブロックHTML
        """
        # block_generator.pyのgenerateメソッドを使用
        html = self._generator.generate(article_json)
        
        # CTA追加
        if include_cta and self.cta_template:
            html = html + "\n\n" + self.cta_template
        
        return html


if __name__ == "__main__":
    # テスト用
    test_json = {
        "lead": "これはテストのリード文です。",
        "points": {
            "title": "この記事のポイント",
            "items": ["ポイント1", "ポイント2", "ポイント3"]
        },
        "sections": [
            {"type": "heading", "level": 2, "text": "見出し1"},
            {"type": "paragraph", "text": "本文テキストです。"},
            {"type": "warning", "text": "これは注意事項です。"},
        ],
        "summary": {
            "title": "まとめ",
            "items": ["まとめ1", "まとめ2", "まとめ3", "まとめ4"]
        }
    }
    
    generator = Generator()
    html = generator.generate(test_json, include_cta=False)
    print(html)
