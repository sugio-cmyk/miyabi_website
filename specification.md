# みやび社会保険労務士事務所 ウェブサイト仕様書

> **ドキュメント体系**
> - 要求定義書: 何を実現するか
> - 設計書: どのように実現するか
> - **仕様書**（本書）: 具体的な実装内容

---

## 1. デザイントークン

### 1.1 カラーパレット

| 変数名 | HEX | RGB | 用途 |
|--------|-----|-----|------|
| --vk-color-primary | #1a365d | 26, 54, 93 | メインカラー、ヘッダー |
| --vk-color-primary-light | #2c5282 | 44, 82, 130 | hover時 |
| --secondary | #5a7a54 | 90, 122, 84 | CTAセクション |
| --accent | #c9a227 | 201, 162, 39 | ボタン、アクセント |
| --background | #faf9f7 | 250, 249, 247 | 背景 |
| --text | #2d3748 | 45, 55, 72 | 本文テキスト |
| --text-light | #718096 | 113, 128, 150 | サブテキスト |
| --white | #ffffff | 255, 255, 255 | カード背景 |

### 1.2 タイポグラフィ

| 用途 | フォント | サイズ | ウェイト |
|------|----------|--------|:--------:|
| 見出しH1 | Noto Serif JP | 2.2rem (35px) | 600 |
| 見出しH2 | Noto Serif JP | 1.8rem (29px) | 600 |
| 見出しH3 | Noto Serif JP | 1.3rem (21px) | 600 |
| 本文 | Noto Sans JP | 1rem (16px) | 400 |
| 小テキスト | Noto Sans JP | 0.85rem (14px) | 400 |
| ラベル | Noto Sans JP | 0.85rem | 600 |

### 1.3 スペーシング

| 用途 | 値 |
|------|-----|
| セクション上下 | 5rem (80px) |
| セクション左右 | 2rem (32px) |
| カード内padding | 2rem (32px) |
| グリッド間隔 | 2rem (32px) |
| 要素間隔（小） | 1rem (16px) |

### 1.4 角丸

| 用途 | 値 |
|------|-----|
| カード | 16px |
| CTAセクション | 24px |
| ボタン | 50px |
| Trust Badge | 50% |
| 入力欄 | 12px |

### 1.5 シャドウ

| 用途 | 値 |
|------|-----|
| カード | 0 2px 8px rgba(0, 0, 0, 0.08) |
| カードhover | 0 4px 20px rgba(0, 0, 0, 0.12) |

---

## 2. Gutenbergブロック仕様

### 2.1 Cover（ヒーロー）

```json
{
  "name": "core/cover",
  "attributes": {
    "url": "/images/hero-bg.png",
    "dimRatio": 90,
    "customOverlayColor": "#1a365d",
    "minHeight": 600,
    "align": "full",
    "style": {
      "spacing": {
        "padding": {
          "top": "4rem",
          "bottom": "4rem",
          "left": "2rem",
          "right": "2rem"
        }
      }
    }
  }
}
```

### 2.2 Group（カード）

```json
{
  "name": "core/group",
  "attributes": {
    "style": {
      "color": {
        "background": "#ffffff"
      },
      "spacing": {
        "padding": {
          "top": "2rem",
          "bottom": "2rem",
          "left": "2rem",
          "right": "2rem"
        }
      },
      "border": {
        "radius": "16px"
      }
    }
  }
}
```

### 2.3 Button（プライマリ）

```json
{
  "name": "core/button",
  "attributes": {
    "style": {
      "color": {
        "background": "#c9a227",
        "text": "#ffffff"
      },
      "border": {
        "radius": "50px"
      },
      "spacing": {
        "padding": {
          "top": "1rem",
          "bottom": "1rem",
          "left": "2.5rem",
          "right": "2.5rem"
        }
      }
    }
  }
}
```

### 2.4 Columns（3カラム）

```json
{
  "name": "core/columns",
  "attributes": {
    "align": "wide",
    "style": {
      "spacing": {
        "blockGap": "2rem"
      }
    }
  }
}
```

---

## 3. ページ別仕様

### 3.1 ホームページ (/)

| セクション | ブロック | 高さ/幅 | 備考 |
|------------|----------|---------|------|
| ヒーロー | cover | 600px min | - |
| Trust Badges | group + columns | auto | - |
| 選ばれる理由 | group + columns (3) | auto | - |
| サービス紹介 | group + columns (3) | auto | **概要のみ+「詳しく見る」リンク** |
| CTA | group | auto | - |

### 3.2 サービスページ (/services/)

| セクション | ブロック | 備考 |
|----------|----------|------|
| タイトル | heading H1 | - |
| サービスカード | columns (3) + image + paragraph + list | **詳細説明+箇条書きリスト** |
| CTA | group | - |

### 3.3 事務所概要ページ (/about/)

| セクション | ブロック |
|------------|----------|
| タイトル | heading H1 |
| 代表挨拶 | group + paragraph |
| 事務所情報 | table |
| 対応エリア | paragraph |
| CTA | group |

### 3.4 お問い合わせページ (/contact/)

| セクション | ブロック |
|------------|----------|
| タイトル | heading H1 |
| Trust Badges | columns (3) |
| ご相談の流れ | columns (4) |
| フォーム | shortcode [contact-form-7] |
| 連絡先カード | columns (2) |

### 3.5 FAQページ (/faq/)

| カテゴリ | 問数 |
|----------|:----:|
| 社会保険労務士全般 | 3 |
| 社会保険・労働保険手続き | 4 |
| 給与計算 | 3 |
| 就業規則 | 3 |
| 助成金 | 2 |

### 3.6 プライバシーポリシーページ (/privacy-policy/)

| セクション | ブロック |
|------------|----------|
| タイトル | heading H1 |
| 各条項 | heading H2 + paragraph |
| 連絡先 | group |

---

## 4. WordPress設定仕様

### 4.1 Lightning カスタマイザー

| 設定項目 | 設定値 |
|----------|--------|
| Lightning デザイン設定 → レイアウト | 1カラム |
| Lightning デザイン設定 → キーカラー | #1a365d |
| サイト基本情報 → タイトル | みやび社会保険労務士事務所 |
| サイト基本情報 → キャッチフレーズ | 愛される会社へ、寄り添いながら。 |

### 4.2 Rank Math設定

| 設定項目 | 設定値 |
|----------|--------|
| 一般設定 → 区切り文字 | ｜ |
| ローカルSEO → ビジネスタイプ | ProfessionalService |
| ローカルSEO → 会社名 | みやび社会保険労務士事務所 |
| スキーマ → デフォルトタイプ | Organization |

### 4.3 メニュー設定

#### ヘッダーメニュー（メニュー名: main-menu）
| 順序 | ラベル | URL |
|:----:|--------|-----|
| 1 | ホーム | / |
| 2 | サービス | /services/ |
| 3 | 事務所概要 | /about/ |
| 4 | FAQ | /faq/ |
| 5 | お問い合わせ | /contact/ |

#### フッターメニュー（メニュー名: footer-menu）
| ラベル | URL |
|--------|-----|
| サービス | /services/ |
| 事務所概要 | /about/ |
| FAQ | /faq/ |
| お問い合わせ | /contact/ |
| プライバシーポリシー | /privacy-policy/ |

### 4.4 Contact Form 7

#### フォームタグ
```
<label>お名前 <span class="required">*必須</span>
[text* your-name placeholder "山田 太郎"]</label>

<label>会社名
[text your-company placeholder "株式会社○○"]</label>

<label>メールアドレス <span class="required">*必須</span>
[email* your-email placeholder "example@example.com"]</label>

<label>ご相談内容 <span class="required">*必須</span>
[textarea* your-message placeholder "ご相談内容をご記入ください"]</label>

[submit "送信する"]
```

#### メールテンプレート（管理者宛）
```
件名: 【お問い合わせ】[your-name] 様より

本文:
ウェブサイトからお問い合わせがありました。

────────────────────
お名前: [your-name]
会社名: [your-company]
メール: [your-email]
────────────────────
ご相談内容:
[your-message]
────────────────────
```

#### 自動返信メール（お客様宛）
```
件名: 【みやび社会保険労務士事務所】お問い合わせありがとうございます

本文:
[your-name] 様

このたびはお問い合わせいただき、誠にありがとうございます。

内容を確認のうえ、2営業日以内にご連絡させていただきます。
しばらくお待ちください。

────────────────────
みやび社会保険労務士事務所
TEL: XXX-XXX-XXXX
Email: info@miyabi-sr.com
────────────────────
```

### 4.5 Slack Webhook設定（CF7 to Webhook）

| 設定項目 | 値 |
|----------|-----|
| Webhook URL | 【Slackで取得した URL】 |
| POST Body | 下記参照 |

```json
{
  "text": "📩 新規お問い合わせ\nお名前: [your-name]\n会社名: [your-company]\nメール: [your-email]\n内容: [your-message]"
}
```

---

## 5. ブログ記事テンプレート

### 5.1 記事構成

| セクション | 内容 |
|------------|------|
| タイトル | 【カテゴリ】記事タイトル（キーワード含む） |
| リード文 | 2-3文で記事の概要 |
| 見出し | H2で3-5セクション |
| 本文 | 各セクション200-400文字 |
| CTA | 記事末尾に問い合わせ誘導 |

### 5.2 カテゴリ

| カテゴリ名 | スラッグ | 内容 |
|----------|--------|------|
| 法改正情報 | law-update | 労働法、社会保険法の改正解説 |
| お役立ち情報 | useful-info | 新規顧客獲得向けコンテンツ |

---

## 6. GA4イベント設定

### 6.1 計測イベント

| イベント名 | トリガー | 目的 |
|----------|---------|------|
| cta_click | CTAボタンクリック | 問い合わせ誘導測定 |
| form_submit | フォーム送信完了 | コンバージョン |
| tel_click | 電話番号クリック | 電話問い合わせ |

### 6.2 コンバージョン設定

| コンバージョン | イベント | 値 |
|--------------|--------|-----|
| 問い合わせ完了 | form_submit | 1件 |

---

## 7. ファイル構成

### 7.1 WordPress メディア

```
/wp-content/uploads/
├── hero-bg.png          (1920×1080)
├── service-insurance.png (16:9)
├── service-payroll.png   (16:9)
├── service-support.png   (16:9)
├── ogp-home.jpg          (1200×630)
└── logo.svg
```

### 7.2 プロジェクトファイル

```
miyabi_website/
├── requirements.md        # 要求定義書
├── preview.html           # HTMLプレビュー
├── privacy-policy.txt     # プライバシーポリシー原稿
├── images/                # 画像素材
│   ├── hero-bg.png
│   ├── service-insurance.png
│   ├── service-payroll.png
│   └── service-support.png
└── wordpress/
    └── pages.xml          # WPインポート用XML
```

---

## 8. SEO仕様

### 8.1 メタ情報一覧

| ページ | title | robots |
|--------|-------|--------|
| ホーム | みやび社会保険労務士事務所｜香川県坂出市の社労士 | index,follow |
| サービス | サービス一覧｜みやび社会保険労務士事務所 | index,follow |
| 事務所概要 | 事務所概要｜みやび社会保険労務士事務所 | index,follow |
| お問い合わせ | お問い合わせ｜みやび社会保険労務士事務所 | index,follow |
| FAQ | よくある質問｜みやび社会保険労務士事務所 | index,follow |
| プライバシー | プライバシーポリシー｜みやび社会保険労務士事務所 | noindex,follow |

### 8.2 meta description原稿（コピペ用）

#### ホーム
```
香川県坂出市のみやび社会保険労務士事務所。中小企業の社会保険・労働保険手続き、給与計算、就業規則作成、助成金申請をサポート。初回相談無料。オンライン対応可。
```

#### サービス
```
社会保険・労働保険手続き代行、給与計算代行、就業規則作成、助成金申請サポート。香川県の中小企業様の人事労務をトータルサポート。顧問料月額2万円から。
```

#### 事務所概要
```
みやび社会保険労務士事務所の概要。香川県坂出市を拠点に、高松市・丸亀市など香川県全域の中小企業様をサポート。「人を大切にする会社づくり」をモットーに。
```

#### お問い合わせ
```
みやび社会保険労務士事務所へのお問い合わせ。初回相談無料。お電話・フォームからお気軽にどうぞ。2営業日以内に返信。オンライン相談にも対応。
```

#### FAQ
```
社会保険労務士への依頼、顧問契約、給与計算、就業規則、助成金に関するよくある質問。香川県坂出市のみやび社会保険労務士事務所がお答えします。
```

### 8.3 構造化データ

詳細は `seo_llmo_design.md` を参照。

---

## 9. 画像仕様

詳細は「サービスカード画像仕様書 v3」を参照。

### 9.1 サマリー

| 画像 | サイズ | 形式 | 最大容量 |
|------|--------|------|----------|
| ヒーロー背景 | 1920×1080 | PNG/WebP | 200KB |
| サービスカード | 800×450 | PNG/WebP | 100KB |
| OGP | 1200×630 | JPG | 150KB |

---

## 10. スタイル管理ポリシー

### 10.1 設計方針

WordPressの標準的な運用に従い、**スタイルは以下のように管理する**。

| 管理場所 | 管理内容 | 理由 |
|----------|----------|------|
| **XML（コンテンツ）** | フォントサイズ、色、パディング等 | エディタで直接編集可能 |
| **追加CSS** | ホバー効果、アニメーション等 | エディタでは設定不可 |

### 10.2 XML（Gutenbergブロック）で管理すべき項目

以下のスタイルはブロックエディタで設定し、**XMLのインラインスタイルとして保存**する。

| カテゴリ | 項目 |
|----------|------|
| タイポグラフィ | font-size、color、font-weight |
| スペーシング | padding、margin |
| ボーダー | border-radius、border-color、border-width |
| 背景 | background-color、グラデーション |
| レイアウト | align、justify |

### 10.3 追加CSS（enhanced-theme.css）で管理すべき項目

以下はGutenbergエディタでは設定できないため、**CSSで管理**する。

| カテゴリ | 項目 | 例 |
|----------|------|
| インタラクション | :hover | カードホバー時 translateY(-8px) |
| アニメーション | transition | 0.3s ease |
| フォントインポート | @import | Google Fonts |

> **注意**: カラーやサイズはXMLで管理。**rgbaもXMLで設定可能**（JSON属性とHTML出力の一致が必要）。

### 10.4 禁止事項

| ❌ 禁止 | 理由 |
|--------|------|
| CSSでfont-size等を`!important`上書き | XMLの設定と競合し、エディタでの変更が反映されない |
| XMLにホバー効果を記述 | Gutenbergでは対応していない |

### 10.5 参照スタイル値

> **方針**: HEX値およびrgbaを使用可能。重要なのはJSON属性とHTML出力の一致。

#### ヒーローセクション
| 要素 | プロパティ | 値 | 管理場所 |
|------|----------|-----|----------|
| ヒーローバッジ | background | rgba(255,255,255,0.15) | **XML** |
| ヒーローバッジ | color | #ffffff | **XML** |
| ヒーローバッジ | border | 1px solid rgba(255,255,255,0.2) | **XML** |
| ヒーローバッジ | padding | 0.5rem 1.5rem | XML |
| ヒーローバッジ | font-size | 0.9rem | XML |
| ヒーロータイトル | font-size | 2.5rem | XML |
| ヒーロータイトル | color | #ffffff | XML |

#### ボタン
| 要素 | プロパティ | 値 |
|------|----------|-----|
| 共通 | padding | **1rem 2.5rem** |
| 共通 | border-radius | 50px |
| 共通 | font-size | 1rem |
| Primary | background | linear-gradient(135deg, #c9a227, #dbb94a) |
| Outline（暗背景） | border | 2px solid **#ffffff** |
| Outline（暗背景） | color | **#ffffff** |

#### セクション
| 要素 | プロパティ | 値 |
|------|----------|-----|
| セクションタイトル | font-size | **2.2rem** |
| セクション | padding | 5rem 2rem |

#### カード
| 要素 | プロパティ | 値 |
|------|----------|-----|
| 通常 | background | #ffffff |
| 通常 | border | 1px solid #cbd5e0 |
| hover | transform | translateY(-8px) ← **CSS** |
| hover | box-shadow | 0 8px 30px rgba(0,0,0,0.12) ← **CSS** |

---

## 改訂履歴

| 日付 | バージョン | 内容 |
|------|:----------:|------|
| 2024/12/12 | 1.0 | 初版作成 |
| 2024/12/12 | 1.1 | 全ページ仕様追加、meta description原稿、メニュー設定追加 |
| 2024/12/12 | 1.2 | CF7メールテンプレート、Slack Webhook設定追加 |
| 2024/12/12 | 1.3 | ブログテンプレート、GA4イベント設定追加、最終ブラッシュアップ |
| 2024/12/13 | **1.4** | **ホーム/サービスページの役割分担明確化、サービス説明文更新** |
| 2024/12/14 | **1.5** | **スタイル管理ポリシー（XMLとCSS役割分担）セクション追加** |
| 2024/12/14 | **1.6** | **WordPressネイティブ対応：HEX値のみ使用、CSSをホバー効果のみに限定** |
| 2024/12/14 | **1.7** | **rgba半透明スタイルはCSSで管理する方針に更新** |
| 2024/12/14 | **1.8** | **rgbaはXMLで設定可能に変更（JSON-HTML一致が必要）** |
