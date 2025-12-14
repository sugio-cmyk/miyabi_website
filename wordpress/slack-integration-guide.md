# Slack連携設定ガイド

お問い合わせフォームからの送信をSlackに通知する設定手順です。

---

## 1. Slack側の設定

### Incoming Webhook の作成

1. Slackにログイン
2. https://api.slack.com/apps にアクセス
3. 「Create New App」→「From scratch」を選択
4. App Name: `みやびWebお問い合わせ`、Workspace: 通知を受けるワークスペースを選択
5. 「Create App」をクリック

### Webhook URLの取得

1. 左メニュー → 「Incoming Webhooks」
2. 「Activate Incoming Webhooks」を ON
3. 「Add New Webhook to Workspace」をクリック
4. 通知を送るチャンネルを選択（例: `#お問い合わせ`）
5. 「Allow」をクリック
6. **Webhook URL** をコピー（`https://hooks.slack.com/services/...` 形式）

> ⚠️ このURLは秘密情報です。外部に公開しないでください。

---

## 2. WordPress側の設定

### プラグインのインストール

1. 管理画面 → プラグイン → 新規追加
2. 「CF7 to Webhook」で検索
3. インストール → 有効化

### Webhook設定

1. お問い合わせ → 対象フォームを編集
2. 「Webhook」タブを開く
3. 設定項目:

| 項目 | 値 |
|------|-----|
| Webhook URL | 取得したSlackのURL |
| Request Method | POST |
| Request Format | JSON |

4. 「JSON Template」に以下を入力:

```json
{
  "text": "🔔 ウェブサイトからお問い合わせがありました",
  "blocks": [
    {
      "type": "header",
      "text": {
        "type": "plain_text",
        "text": "📩 新規お問い合わせ"
      }
    },
    {
      "type": "section",
      "fields": [
        {
          "type": "mrkdwn",
          "text": "*お名前:*\n[your-name]"
        },
        {
          "type": "mrkdwn",
          "text": "*会社名:*\n[company-name]"
        }
      ]
    },
    {
      "type": "section",
      "fields": [
        {
          "type": "mrkdwn",
          "text": "*メール:*\n[your-email]"
        },
        {
          "type": "mrkdwn",
          "text": "*電話:*\n[your-tel]"
        }
      ]
    },
    {
      "type": "section",
      "text": {
        "type": "mrkdwn",
        "text": "*お問い合わせ内容:*\n[your-message]"
      }
    },
    {
      "type": "context",
      "elements": [
        {
          "type": "mrkdwn",
          "text": "📅 送信日時: [_date] [_time]"
        }
      ]
    }
  ]
}
```

5. 「保存」をクリック

---

## 3. テスト送信

1. ウェブサイトのお問い合わせページにアクセス
2. テストデータを入力して送信
3. Slackの指定チャンネルに通知が届くことを確認

### トラブルシューティング

| 症状 | 対処法 |
|------|--------|
| 通知が届かない | Webhook URLが正しいか確認 |
| フォーム送信エラー | Request Method が POST か確認 |
| 文字化け | Request Format が JSON か確認 |

---

## 4. メール通知について

Slack連携を使用する場合、Contact Form 7のメール通知は不要です。

### メール通知を無効化（任意）

1. お問い合わせ → フォーム編集
2. 「メール」タブ
3. 送信先を空欄にするか、無効なアドレスを設定

> 💡 バックアップとしてメール通知も残しておくことをおすすめします。

---

## チェックリスト

- [ ] Slack App作成
- [ ] Incoming Webhook有効化
- [ ] Webhook URL取得
- [ ] CF7 to Webhook インストール
- [ ] フォームにWebhook設定
- [ ] テスト送信で通知確認
