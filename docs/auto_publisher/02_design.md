# 記事自動投稿ツール - 設計書

## 1. システム構成

### 1.1 全体アーキテクチャ

```
┌──────────────────────────────────────────────────────────────────┐
│                        auto_publish.py                            │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────┐   ┌─────────────┐   ┌─────────────┐            │
│  │  Loader     │ → │ Structurer  │ → │ Validator   │            │
│  │  (原稿読込) │   │ (AI構造化)  │   │ (品質チェック) │            │
│  └─────────────┘   └─────────────┘   └─────────────┘            │
│                                              ↓                   │
│  ┌─────────────┐   ┌─────────────┐   ┌─────────────┐            │
│  │ History     │ ← │ Publisher   │ ← │ Generator   │            │
│  │ (履歴管理)   │   │ (WP投稿)    │   │ (HTML生成)  │            │
│  └─────────────┘   └─────────────┘   └─────────────┘            │
└──────────────────────────────────────────────────────────────────┘
                            ↓
┌──────────────────────────────────────────────────────────────────┐
│                       外部サービス                                │
├────────────────────────────┬─────────────────────────────────────┤
│     Gemini API             │          WordPress REST API         │
│   (Google AI Studio)       │        (Application Password)       │
└────────────────────────────┴─────────────────────────────────────┘
```

### 1.2 ファイル構成

```
miyabi_website/
├── tools/
│   ├── auto_publish.py       # メインスクリプト（新規）
│   ├── block_generator.py    # 既存のHTML生成
│   ├── config.example.yaml   # 設定ファイルテンプレート
│   └── lib/
│       ├── __init__.py
│       ├── loader.py         # 原稿読込モジュール
│       ├── structurer.py     # AI構造化モジュール
│       ├── validator.py      # 構造バリデーションモジュール（新規）
│       ├── generator.py      # HTML生成ラッパー
│       ├── publisher.py      # WordPress投稿モジュール
│       └── history.py        # 投稿履歴管理モジュール（新規）
├── drafts/                   # 原稿ファイル置き場
│   └── example.md
├── output/                   # 中間ファイル出力
│   ├── json/
│   ├── html/
│   └── post_history.yaml     # 投稿履歴（新規）
└── config.yaml               # 設定ファイル（.gitignore）
```

---

## 2. モジュール設計

### 2.1 Loader（原稿読込）

**責務**: Markdownファイルからメタ情報と本文を抽出

```python
class Loader:
    def load(self, file_path: str) -> Draft:
        """
        Markdownファイルを読み込み、Draftオブジェクトを返す
        - YAMLフロントマターをパース
        - 本文を抽出
        """
        pass

@dataclass
class Draft:
    title: str           # 記事タイトル
    slug: str            # URLスラッグ
    description: str     # メタディスクリプション
    category: str        # カテゴリ名
    tags: list[str]      # タグリスト
    status: str          # draft / publish
    content: str         # 本文（Markdown）
```

### 2.2 Structurer（AI構造化）

**責務**: Gemini APIを使用してJSON構造化

```python
class Structurer:
    def __init__(self, api_key: str):
        self.model = genai.GenerativeModel('gemini-3-pro')
    
    def structure(self, content: str) -> ArticleJSON:
        """
        本文をJSON構造に変換
        - プロンプトテンプレートを適用
        - Gemini APIを呼び出し
        - JSONをパースして返す
        """
        pass

@dataclass
class ArticleJSON:
    lead: str
    points: dict
    sections: list[dict]
    summary: dict
```

### 2.3 Generator（HTML生成）

**責務**: 既存のblock_generator.pyをラップ

```python
class Generator:
    def generate(self, article_json: ArticleJSON, 
                 include_cta: bool = True) -> str:
        """
        JSONからブロックHTMLを生成
        - block_generator.pyの機能を呼び出し
        - オプションでCTAを追加
        """
        pass
```

### 2.4 Publisher（WordPress投稿）

**責務**: WordPress REST APIで投稿

```python
class Publisher:
    def __init__(self, site_url: str, username: str, 
                 app_password: str):
        self.api_url = f"{site_url}/wp-json/wp/v2"
        self.auth = (username, app_password)
    
    def create_post(self, draft: Draft, content: str) -> PostResult:
        """
        WordPressに下書き投稿を作成
        - タイトル、本文、スラッグを設定
        - カテゴリ・タグを設定
        - 投稿IDとURLを返す
        """
        pass

@dataclass
class PostResult:
    post_id: int
    edit_url: str
    view_url: str
    status: str
```

---

## 3. 処理フロー

### 3.1 メイン処理フロー

```
1. コマンドライン引数を解析
2. 設定ファイル（config.yaml）を読み込み
3. Loaderで原稿ファイルを読み込み
4. Structurerで本文をJSON構造化
5. Validatorで構造をバリデーション（警告/エラー出力）
6. （--confirmモード）確認プロンプト表示→続行/中止
7. （オプション）JSONを中間ファイルとして保存
8. GeneratorでブロックHTMLを生成
9. （オプション）HTMLを中間ファイルとして保存
10. Historyで既存投稿を検索（slug一致）
11. PublisherでWordPressに投稿（新規 or 更新）
12. Historyに投稿履歴を保存
13. 結果を出力
```

### 3.2 新規投稿 vs 更新判定フロー

```
┌─────────────────────────────────────────────────────────────┐
│                    投稿モード判定                            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. Historyファイルでslugを検索                             │
│     └→ 存在する場合: post_id取得                            │
│                                                             │
│  2. WordPress APIでslugを検索（Historyになければ）          │
│     GET /wp/v2/posts?slug={slug}                            │
│     └→ 存在する場合: post_id取得                            │
│                                                             │
│  3. 判定                                                    │
│     ├─ post_idあり → 「既存投稿を更新しますか？ [y/n]」     │
│     │                 └→ y: PUT更新 / n: 中止               │
│     │                 └→ --force-update: 確認なしで更新     │
│     └─ post_idなし → POST新規作成                           │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 3.3 エラーハンドリング

```
┌─────────────────────────────────────────────────────────────┐
│                    エラー発生時の動作                         │
├─────────────┬───────────────────────────────────────────────┤
│ Loader      │ ファイル不存在 → エラー終了                    │
│ Structurer  │ API失敗 → リトライ3回、失敗で終了              │
│             │ JSON不正 → 修復試行、失敗でJSONを保存して終了  │
│ Validator   │ エラー → 終了 / 警告 → 続行（警告表示）        │
│ Generator   │ 変換失敗 → JSONを保存してエラー終了            │
│ Publisher   │ 認証失敗 → エラー終了                          │
│             │ 投稿失敗 → リトライ2回、失敗でHTMLを保存して終了│
│ History     │ 書込失敗 → 警告のみ（投稿は成功扱い）          │
└─────────────┴───────────────────────────────────────────────┘
```

---

## 2.5 Validator（構造バリデーション）【新規】

**責務**: 生成されたJSONの品質をチェック

```python
class Validator:
    def validate(self, article_json: ArticleJSON) -> ValidationResult:
        """
        JSONの構造を検証
        - h2が3〜5個あるか
        - 各h2直後にparagraphがあるか
        - list/table/warning/faqのうち最低2種類あるか
        - pointsが3項目あるか
        - summaryが4項目以上あるか
        """
        pass

@dataclass
class ValidationResult:
    is_valid: bool           # 致命的エラーがないか
    errors: list[str]        # 致命的エラーリスト
    warnings: list[str]      # 警告リスト
```

### バリデーションルール

| 種別 | ルール | 重要度 |
|------|--------|--------|
| ERR-001 | h2が0個 | Error |
| ERR-002 | summaryが存在しない | Error |
| WRN-001 | h2が3個未満 or 6個以上 | Warning |
| WRN-002 | table/warningがどちらも0個 | Warning |
| WRN-003 | faqが2個未満 | Warning |
| WRN-004 | pointsが3項目でない | Warning |

---

## 2.6 History（投稿履歴管理）【新規】

**責務**: slug→post_idのマッピングを管理

```python
class HistoryManager:
    def __init__(self, history_file: str = "output/post_history.yaml"):
        self.history_file = history_file
        self.history = self._load()
    
    def find_by_slug(self, slug: str) -> Optional[int]:
        """slugからpost_idを検索"""
        pass
    
    def save(self, slug: str, post_id: int, action: str):
        """投稿履歴を保存"""
        pass

# post_history.yaml の形式
# law-reform-roadmap-2026:
#   post_id: 123
#   created_at: "2026-01-27T19:00:00+09:00"
#   updated_at: "2026-01-28T10:00:00+09:00"
#   versions: 2
```

---

## 4. 設定ファイル設計

### 4.1 config.yaml

```yaml
# Gemini API設定
gemini:
  api_key: ${GEMINI_API_KEY}  # 環境変数から読み込み
  model: gemini-3-pro

# WordPress設定
wordpress:
  site_url: https://example.com
  username: admin
  app_password: ${WP_APP_PASSWORD}  # 環境変数から読み込み
  default_category: コラム
  default_status: draft

# 出力設定
output:
  save_json: true
  save_html: true
  json_dir: output/json
  html_dir: output/html

# CTA設定
cta:
  enabled: true
  template_file: block-html/posts/cta.txt
```

---

## 5. インターフェース設計

### 5.1 コマンドライン

```bash
# 基本使用
py tools/auto_publish.py drafts/記事名.md

# オプション
py tools/auto_publish.py drafts/記事名.md --dry-run      # 投稿せずプレビュー
py tools/auto_publish.py drafts/記事名.md --publish      # 即公開
py tools/auto_publish.py drafts/記事名.md --no-cta       # CTAなし
py tools/auto_publish.py drafts/*.md                     # バッチ処理
```

### 5.2 出力形式

```
========================================
記事自動投稿ツール
========================================

[1/4] 原稿読込中...
  ✓ タイトル: 法改正ロードマップ（2026年版）
  ✓ スラッグ: law-reform-roadmap-2026

[2/4] AI構造化中...
  ✓ Gemini API: 成功（2.3秒）
  ✓ JSON保存: output/json/law-reform-roadmap-2026.json

[3/4] HTML生成中...
  ✓ ブロック数: 25
  ✓ HTML保存: output/html/law-reform-roadmap-2026.txt

[4/4] WordPress投稿中...
  ✓ 投稿ID: 123
  ✓ ステータス: draft

========================================
完了！
編集URL: https://example.com/wp-admin/post.php?post=123&action=edit
========================================
```
