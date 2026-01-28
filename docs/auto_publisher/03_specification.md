# 記事自動投稿ツール - 仕様書

## 1. 原稿ファイル仕様

### 1.1 ファイル形式

- **拡張子**: `.md`（Markdown）
- **エンコーディング**: UTF-8
- **改行コード**: LF または CRLF

### 1.2 フロントマター仕様

YAMLフロントマターで記事メタ情報を定義する。

```yaml
---
title: 記事タイトル（必須）
slug: url-slug（必須）
description: メタディスクリプション（必須）
category: カテゴリ名（任意、デフォルト: config.yamlの設定）
tags:
  - タグ1
  - タグ2
status: draft | publish（任意、デフォルト: draft）
featured_image: /path/to/image.jpg（任意）
scheduled_at: 2026-02-01T10:00:00+09:00（任意、予約投稿用）
---
```

### 1.3 フィールド定義

| フィールド | 必須 | 型 | 説明 | 例 |
|------------|------|-----|------|-----|
| title | ○ | string | 記事タイトル | 法改正ロードマップ |
| slug | ○ | string | URLスラッグ（半角英数-_） | law-reform-2026 |
| description | ○ | string | メタディスクリプション（120文字以内推奨） | 法改正への対応方法を... |
| category | × | string | カテゴリ名（既存カテゴリと一致） | コラム |
| tags | × | list | タグ名のリスト | [法改正, 就業規則] |
| status | × | enum | draft / publish | draft |
| featured_image | × | string | アイキャッチ画像パス | /images/hero.jpg |
| scheduled_at | × | datetime | 予約公開日時（ISO 8601） | 2026-02-01T10:00:00+09:00 |

### 1.4 本文仕様

フロントマター以降の部分が本文として扱われる。

- 通常のMarkdown記法で記述
- 見出し・段落・リストを自然に書けばAIが構造化
- 特別なフォーマットは不要

```markdown
---
title: ...
---

（ここから本文）

法改正対応は、確定した内容の反映と、見込み段階の備えを分けるのが最も安全です。
会社がまず整えるべきは「対象判定」「規程・運用の棚卸し」「社内周知」の3点。

## なぜ法改正対応は"漏れやすい"のか

法改正は、施行日や対象範囲の細部が更新されたり...

（以下続く）
```

---

## 2. 構造化プロンプト仕様

### 2.1 プロンプトテンプレート

`docs/prompts/article_structure.md` に定義済みのプロンプトを使用する。

### 2.2 JSON出力仕様

`docs/json_schema.md` に定義済みのスキーマに従う。

### 2.3 Gemini API呼び出し仕様

| 項目 | 値 |
|------|-----|
| モデル | gemini-3-pro |
| temperature | 0.3（安定した出力） |
| max_output_tokens | 8192 |
| response_mime_type | application/json |

---

## 3. ブロックHTML仕様

### 3.1 生成されるブロック

既存の `block_generator.py` に準拠。

| JSONタイプ | WordPress ブロック |
|------------|-------------------|
| lead | `wp:paragraph` |
| points | `wp:vk-blocks/border-box` (info) |
| heading (level:2) | `wp:heading` (下線付き) |
| heading (level:3) | `wp:heading` (左ボーダー) |
| paragraph | `wp:paragraph` |
| list | `wp:list` |
| warning | `wp:vk-blocks/alert` (warning) |
| table | `wp:table` (.post-table) |
| faq | `wp:vk-blocks/faq2` |
| summary | `wp:vk-blocks/border-box` (check) |

### 3.2 CTA自動追加

`cta.enabled: true` の場合、記事末尾に `block-html/posts/cta.txt` の内容を追加する。

---

## 4. WordPress API仕様

### 4.1 認証

| 項目 | 値 |
|------|-----|
| 方式 | Basic認証 |
| ユーザー名 | WordPressログインユーザー名 |
| パスワード | Application Password |

### 4.2 投稿作成エンドポイント

```
POST /wp-json/wp/v2/posts
```

### 4.3 リクエストボディ

```json
{
  "title": "記事タイトル",
  "content": "<!-- wp:paragraph -->...",
  "slug": "url-slug",
  "status": "draft",
  "categories": [5],
  "tags": [10, 12],
  "meta": {
    "_yoast_wpseo_metadesc": "メタディスクリプション"
  }
}
```

### 4.4 レスポンス（成功時）

```json
{
  "id": 123,
  "link": "https://example.com/url-slug/",
  "status": "draft"
}
```

### 4.5 投稿更新エンドポイント【新規】

```
PUT /wp-json/wp/v2/posts/{id}
```

リクエストボディは新規作成と同じ形式。

### 4.6 投稿検索エンドポイント【新規】

```
GET /wp-json/wp/v2/posts?slug={slug}&status=any
```

既存投稿の有無を確認するために使用。

### 4.7 エラーコード

| コード | 意味 | 対処 |
|--------|------|------|
| 401 | 認証失敗 | Application Passwordを確認 |
| 403 | 権限不足 | ユーザー権限を確認 |
| 400 | 不正なリクエスト | カテゴリID等を確認 |
| 404 | 投稿が見つからない | post_idを確認 |
| 500 | サーバーエラー | WordPress側を確認 |

---

## 5. 設定ファイル仕様

### 5.1 config.yaml

```yaml
# ============================================
# 記事自動投稿ツール 設定ファイル
# ============================================

# Gemini API設定
gemini:
  # APIキー（環境変数を推奨）
  api_key: ${GEMINI_API_KEY}
  # 使用モデル
  model: gemini-3-pro
  # 生成パラメータ
  temperature: 0.3
  max_output_tokens: 8192

# WordPress設定
wordpress:
  # サイトURL（末尾スラッシュなし）
  site_url: https://example.com
  # ログインユーザー名
  username: admin
  # Application Password（環境変数を推奨）
  app_password: ${WP_APP_PASSWORD}
  # デフォルトカテゴリ（名前 or ID）
  default_category: コラム
  # デフォルト投稿ステータス
  default_status: draft

# 出力設定
output:
  # 中間ファイルを保存するか
  save_json: true
  save_html: true
  # 保存先ディレクトリ
  json_dir: output/json
  html_dir: output/html

# CTA設定
cta:
  # CTAを自動追加するか
  enabled: true
  # CTAテンプレートファイル
  template_file: block-html/posts/cta.txt

# プロンプト設定
prompt:
  # 構造化プロンプトファイル
  template_file: docs/prompts/article_structure.md
```

### 5.2 環境変数

| 変数名 | 必須 | 説明 |
|--------|------|------|
| GEMINI_API_KEY | ○ | Gemini APIキー |
| WP_APP_PASSWORD | ○ | WordPress Application Password |

### 5.3 .gitignore追加

```
config.yaml
.env
```

---

## 6. エラーメッセージ仕様

| エラー | メッセージ | 終了コード |
|--------|-----------|-----------|
| 原稿ファイル不存在 | `Error: File not found: {path}` | 1 |
| フロントマター不正 | `Error: Invalid frontmatter: {detail}` | 1 |
| 必須フィールド不足 | `Error: Missing required field: {field}` | 1 |
| Gemini API失敗 | `Error: Gemini API failed: {detail}` | 2 |
| JSON解析失敗 | `Error: Failed to parse JSON: {detail}` | 2 |
| バリデーションエラー | `Error: Validation failed: {detail}` | 2 |
| WordPress認証失敗 | `Error: WordPress auth failed: {detail}` | 3 |
| WordPress投稿失敗 | `Error: WordPress post failed: {detail}` | 3 |

---

## 7. バリデーション仕様【新規】

### 7.1 バリデーションルール

| コード | ルール | 重要度 | 説明 |
|--------|--------|--------|------|
| ERR-001 | h2が0個 | Error | 記事として成立しない |
| ERR-002 | summaryが存在しない | Error | まとめセクション必須 |
| ERR-003 | leadが存在しない | Error | リード文必須 |
| WRN-001 | h2が3個未満 or 6個以上 | Warning | 推奨範囲外 |
| WRN-002 | table/warningがどちらも0個 | Warning | 構造化ブロック推奨 |
| WRN-003 | faqが2個未満 | Warning | FAQ推奨 |
| WRN-004 | pointsが3項目でない | Warning | ポイント3項目推奨 |
| WRN-005 | summaryが4項目未満 | Warning | まとめ4項目以上推奨 |

### 7.2 バリデーション結果例

```
[Validation]
  ✓ Lead: あり
  ✓ Points: 3項目
  ✓ H2見出し: 4個
  ⚠ Warning: tableがありません（推奨）
  ⚠ Warning: faqが1個のみ（2個以上推奨）
  ✓ Summary: 5項目

結果: 2件の警告あり（続行可能）
```

---

## 8. 投稿履歴仕様【新規】

### 8.1 履歴ファイル形式

```yaml
# output/post_history.yaml
law-reform-roadmap-2026:
  post_id: 123
  title: "法改正ロードマップ（2026年版）"
  created_at: "2026-01-27T19:00:00+09:00"
  updated_at: "2026-01-28T10:00:00+09:00"
  versions: 2
  source_file: "drafts/law-reform-roadmap-2026.md"

hiring-procedures:
  post_id: 124
  title: "採用手続きの基本"
  created_at: "2026-01-28T12:00:00+09:00"
  updated_at: null
  versions: 1
  source_file: "drafts/hiring-procedures.md"
```

### 8.2 履歴の用途

| 用途 | 説明 |
|------|------|
| 既存投稿検出 | slugからpost_idを高速取得 |
| 更新回数追跡 | versionsをインクリメント |
| 監査ログ | いつ何を投稿したか記録 |

---

## 9. コマンドラインオプション仕様【拡張】

```bash
# 基本使用
py tools/auto_publish.py drafts/記事名.md

# 投稿モード
py tools/auto_publish.py drafts/記事名.md --dry-run       # 投稿せずプレビュー
py tools/auto_publish.py drafts/記事名.md --publish       # 即公開（draft→publish）
py tools/auto_publish.py drafts/記事名.md --confirm       # JSON生成後に確認

# 更新モード
py tools/auto_publish.py drafts/記事名.md --force-update  # 確認なしで更新
py tools/auto_publish.py drafts/記事名.md --force-new     # 既存無視で新規作成

# その他
py tools/auto_publish.py drafts/記事名.md --no-cta        # CTAなし
py tools/auto_publish.py drafts/記事名.md --skip-validation # バリデーションスキップ
py tools/auto_publish.py drafts/*.md                      # バッチ処理
py tools/auto_publish.py --test-connection                # 接続テスト
```

---

## 10. テスト仕様

### 10.1 テストケース

| ID | テスト内容 | 期待結果 |
|----|-----------|----------|
| T-001 | 正常な原稿で投稿 | 下書き作成成功 |
| T-002 | 必須フィールド不足 | エラー終了 |
| T-003 | Gemini API失敗 | リトライ後エラー |
| T-004 | WordPress認証失敗 | エラー終了 |
| T-005 | --dry-runオプション | 投稿せず成功 |
| T-006 | --publishオプション | 公開状態で投稿 |
| T-007 | バッチ処理（複数ファイル） | 全ファイル処理 |
| T-008 | **既存slugで再実行** | **更新確認→PUT成功** |
| T-009 | **--force-updateオプション** | **確認なしでPUT成功** |
| T-010 | **バリデーションエラー** | **エラー終了** |
| T-011 | **バリデーション警告** | **警告表示→続行可能** |
| T-012 | **--confirmオプション** | **確認プロンプト表示** |
| T-013 | **--test-connection** | **接続テスト成功/失敗** |

### 10.2 テスト用原稿

`drafts/test_article.md` を用意し、テスト実行に使用する。

