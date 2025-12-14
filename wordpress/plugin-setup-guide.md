# プラグイン設定ガイド

みやび社会保険労務士事務所サイトで使用する必須プラグインの設定手順です。

---

## 1. Lightning G3 Pro Unit / VK Blocks

### インストール

1. 管理画面 → プラグイン → 新規追加
2. 「VK Blocks」で検索 → インストール → 有効化
3. （有料版の場合）Lightning G3 Pro Unitをアップロードして有効化

### 推奨設定

- 外観 → カスタマイズ → Lightning デザイン設定
  - キーカラー: `#1a365d`（深い紺色）
  - カスタムCSS: 必要に応じて追加

---

## 2. Contact Form 7

### インストール

1. 管理画面 → プラグイン → 新規追加
2. 「Contact Form 7」で検索 → インストール → 有効化

### フォーム作成

1. お問い合わせ → 新規追加
2. タイトル: 「お問い合わせフォーム」
3. フォームテンプレート:

```
<label>お名前（必須）
[text* your-name]</label>

<label>会社名
[text company-name]</label>

<label>メールアドレス（必須）
[email* your-email]</label>

<label>電話番号
[tel your-tel]</label>

<label>お問い合わせ内容（必須）
[textarea* your-message]</label>

[submit "送信する"]
```

4. メール設定は使用しない（Slack連携で通知）

### ページへの設置

1. お問い合わせページを編集
2. ショートコードブロックを追加
3. `[contact-form-7 id="フォームID" title="お問い合わせフォーム"]`

---

## 3. CF7 to Webhook（Slack連携）

→ 詳細は `slack-integration-guide.md` を参照

---

## 4. UpdraftPlus

### インストール

1. 管理画面 → プラグイン → 新規追加
2. 「UpdraftPlus」で検索 → インストール → 有効化

### バックアップ設定

1. 設定 → UpdraftPlus バックアップ
2. 「設定」タブを開く
3. スケジュール設定:
   - ファイルバックアップ: 週1回
   - データベースバックアップ: 週1回
   - 保持数: 4
4. 保存先: Google Drive を選択
5. 「Googleで認証」をクリック → アカウント連携
6. 「変更を保存」

### 手動バックアップ

- 「今すぐバックアップ」ボタンで即時バックアップ可能

---

## 5. Site Kit by Google

### インストール

1. 管理画面 → プラグイン → 新規追加
2. 「Site Kit by Google」で検索 → インストール → 有効化

### GA4設定

1. Site Kit → ダッシュボード
2. 「Googleアカウントでログイン」
3. 権限を許可
4. サイトを確認（HTMLタグまたはDNS）
5. Google アナリティクスを有効化
6. GA4プロパティを選択または新規作成

### 確認

- GA4 → リアルタイム レポートで計測確認

---

## 6. Wordfence Security

### インストール

1. 管理画面 → プラグイン → 新規追加
2. 「Wordfence」で検索 → インストール → 有効化

### 初期設定

1. Wordfence → ダッシュボード
2. メールアドレスを登録（セキュリティアラート受信用）
3. 無料ライセンスを取得

### 推奨設定

- Wordfence → ファイアウォール
  - 「学習モード」で1週間運用後、「有効化して保護」に変更
- Wordfence → スキャン
  - 週1回のスキャンを設定

---

## チェックリスト

- [ ] VK Blocks インストール・有効化
- [ ] Contact Form 7 フォーム作成
- [ ] CF7 to Webhook Slack連携設定
- [ ] UpdraftPlus Google Drive連携・スケジュール設定
- [ ] Site Kit GA4連携・計測確認
- [ ] Wordfence 初期設定・スキャン実行
