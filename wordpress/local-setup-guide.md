# Local（by Flywheel）導入＆インポート手順書

## 概要

Local（旧 Local by Flywheel）は、Windows/Mac/Linuxで使えるWordPressローカル開発環境です。
サーバー契約なしでWordPressサイトをテストできます。

---

## Part 1: Localのインストール

### Step 1: ダウンロード

1. [Local公式サイト](https://localwp.com/) にアクセス
2. 「DOWNLOAD FOR FREE」をクリック
3. プラットフォーム選択: **Windows**
4. 必要情報を入力（メールアドレス等）
5. ダウンロード開始

### Step 2: インストール

1. ダウンロードした `local-X.X.X-windows.exe` を実行
2. インストーラーの指示に従う
3. インストール完了後、Localを起動

> [!NOTE]
> 初回起動時にファイアウォールの許可を求められたら「許可」してください。

---

## Part 2: WordPressサイトの作成

### Step 1: 新規サイト作成

1. Localを起動
2. 「+ Create a new site」をクリック
3. 「Create a new site」を選択して「Continue」

### Step 2: サイト名設定

| 項目 | 入力値 |
|------|--------|
| Site name | `miyabi-sr` |

「Continue」をクリック

### Step 3: 環境設定

「Preferred」を選択（推奨設定）

または「Custom」で以下を選択:
| 項目 | 推奨値 |
|------|--------|
| PHP Version | 8.1+ |
| Web Server | nginx |
| Database | MySQL 8.0 |

「Continue」をクリック

### Step 4: WordPress設定

| 項目 | 入力値 |
|------|--------|
| WordPress Username | `admin` |
| WordPress Password | 任意（メモしておく） |
| WordPress Email | 任意 |

「Add Site」をクリック → サイト作成開始（1〜2分）

---

## Part 3: Lightningテーマのインストール

### Step 1: 管理画面にアクセス

1. Localでサイトを選択
2. 「WP Admin」ボタンをクリック
3. 設定したユーザー名/パスワードでログイン

### Step 2: テーマインストール

1. 管理画面 → 外観 → テーマ → 「新規追加」
2. 検索欄に `Lightning` と入力
3. 「Lightning」テーマの「インストール」→「有効化」

---

## Part 4: 固定ページのインポート

### Step 1: インポートツールの準備

1. 管理画面 → ツール → インポート
2. 「WordPress」の「今すぐインストール」をクリック
3. 「インポーターの実行」をクリック

### Step 2: XMLファイルのインポート

1. 「ファイルを選択」をクリック
2. 以下のファイルを選択:
   ```
   c:\Users\kaede\Documents\MyProjects\miyabi_website\wordpress\pages.xml
   ```
3. 「ファイルをアップロードしてインポート」をクリック

### Step 3: インポート設定

| 項目 | 設定 |
|------|------|
| 投稿者の割り当て | 既存のユーザー `admin` を選択 |
| 添付ファイルのインポート | チェックを入れる |

「実行」をクリック

### Step 4: サンプル記事のインポート（任意）

同様の手順で以下もインポート:
```
c:\Users\kaede\Documents\MyProjects\miyabi_website\wordpress\sample-posts.xml
```

---

## Part 5: 必須プラグインのインストール

### インストールするプラグイン

| プラグイン | 用途 |
|------------|------|
| Lightning G3 Pro Unit | テーマ拡張（有料・任意） |
| VK Blocks | ブロック拡張 |
| Contact Form 7 | 問い合わせフォーム |

### インストール手順

1. 管理画面 → プラグイン → 新規追加
2. 各プラグイン名で検索 → インストール → 有効化

---

## Part 6: 固定ページの設定

### フロントページの設定

1. 管理画面 → 設定 → 表示設定
2. 「ホームページの表示」→「固定ページ」を選択
3. ホームページ: **ホーム** を選択
4. 「変更を保存」

### メニューの設定

1. 管理画面 → 外観 → メニュー
2. 「新しいメニューを作成」→ 名前: `メインメニュー`
3. 固定ページから追加: ホーム、サービス、事務所概要、お問い合わせ
4. メニュー設定: 「Header Navigation」にチェック
5. 「メニューを保存」

---

## Part 7: デザインの適用（重要）

本サイトのデザイン（フォント、配色、ボタン装飾など）を正しく反映させるために、カスタムCSSの適用が必要です。

1. **CSSファイルを開く**
   以下のファイルをテキストエディタで開きます:
   ```
   c:\Users\kaede\Documents\MyProjects\miyabi_website\wordpress\enhanced-theme.css
   ```

2. **追加CSSに貼り付け**
   - 管理画面 → 外観 → カスタマイズ → 「追加CSS」
   - `enhanced-theme.css` の内容をすべてコピーして貼り付け
   - 「公開」をクリック

---

## Part 8: サイト確認

1. Localで「Open Site」をクリック
2. ブラウザでサイトが表示されることを確認

---

## トラブルシューティング

| 問題 | 解決策 |
|------|--------|
| サイトが起動しない | Localを再起動、またはサイトを「Start」 |
| インポートエラー | XMLファイルの文字コードがUTF-8か確認 |
| テーマが反映されない | キャッシュクリア（Ctrl+Shift+R） |

---

## 次のステップ

- [ ] Contact Form 7でフォーム作成
- [ ] Yoast SEOインストール（SEO管理）
- [ ] カラー設定（カスタマイザー）
