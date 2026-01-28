# WordPress Block HTML 開発パターン集

WordPress Block Editor（Gutenberg）で正しく認識されるHTMLパターンをまとめます。

---

## ✅ 推奨パターン

### ボタン（シンプル）
```html
<!-- wp:button {"backgroundColor":"vk-color-primary","style":{"border":{"radius":"50px"}}} -->
<div class="wp-block-button"><a
    class="wp-block-button__link has-vk-color-primary-background-color has-background wp-element-button"
    href="/contact/" style="border-radius:50px">お問い合わせ</a></div>
<!-- /wp:button -->
```

### カードにシャドウ
```html
<!-- wp:group {"className":"vk-shadow-lv3","style":{"border":{"radius":"16px"}},"backgroundColor":"white"} -->
<div class="wp-block-group vk-shadow-lv3 has-white-background-color has-background"
    style="border-radius:16px">
    <!-- コンテンツ -->
</div>
<!-- /wp:group -->
```

### 画像の角丸（VK Blocks）
```html
<!-- wp:image {"sizeSlug":"full","className":"is-style-vk-image-rounded"} -->
<figure class="wp-block-image size-full is-style-vk-image-rounded">
    <img src="..." alt="..."/>
</figure>
<!-- /wp:image -->
```

### 3カラムレイアウト
```html
<!-- wp:columns {"align":"wide"} -->
<div class="wp-block-columns alignwide">
    <!-- wp:column -->
    <div class="wp-block-column">
        <!-- コンテンツ -->
    </div>
    <!-- /wp:column -->
    
    <!-- wp:column -->
    <div class="wp-block-column">
        <!-- コンテンツ -->
    </div>
    <!-- /wp:column -->
    
    <!-- wp:column -->
    <div class="wp-block-column">
        <!-- コンテンツ -->
    </div>
    <!-- /wp:column -->
</div>
<!-- /wp:columns -->
```

---

## ❌ 避けるべきパターン

### ボタンにカスタムpadding/fontSize
```html
<!-- ❌ WordPressで認識エラーになる -->
<!-- wp:button {"style":{"spacing":{"padding":{"top":"16px"}},"typography":{"fontSize":"16px"}}} -->
```
**代替案**: WordPress上でサイドバーから調整

### 画像に直接border-radius
```html
<!-- ❌ WordPressで認識エラーになる -->
<img style="border-radius:16px;..."/>
```
**代替案**: `is-style-vk-image-rounded` を使用

### is-style-rounded（標準スタイル）
```html
<!-- ❌ 画像が完全な円形になる -->
<!-- wp:image {"className":"is-style-rounded"} -->
```
**代替案**: VK Blocksの `is-style-vk-image-rounded` を使用

---

## VK Blocksで使える便利なクラス

| クラス名 | 効果 |
|---------|------|
| `vk-shadow-lv1` | 軽いシャドウ |
| `vk-shadow-lv2` | 中程度シャドウ（料金カード向け） |
| `vk-shadow-lv3` | 強めシャドウ（サービスカード向け） |
| `vk-shadow-lv4` | 最も強いシャドウ |
| `is-style-vk-image-rounded` | 画像の角丸（約8px） |

---

## 色の参照

| 色名 | クラス | 用途 |
|-----|--------|------|
| 紺色 | `vk-color-primary` | 見出し、CTA背景 |
| オレンジ | `vk-color-accent` | ボタン、バッジ |
| 薄いグレー | `vk-color-light` | セクション背景 |
| 白 | `white` | カード背景 |

---

## Tips

1. **複雑なスタイルはWP上で調整**  
   HTMLではシンプルに保ち、詳細な調整はWordPressエディタで行う

2. **VK Blocksを活用**  
   シャドウや角丸はVK Blocksのクラスを使う

3. **絵文字 vs VK Blocksアイコン**  
   - CTAの連絡先など → 絵文字でOK（シンプルで認識エラーなし）
   - セクションタイトルのアイコン → WP上でVK Blocksに置換推奨

---

## VK Blocks アイコンの使い方

### HTML内に書くリスク
VK Blocksアイコンのブロックコードは複雑で、HTMLに直接書くと認識エラーのリスクあり。

### 推奨アプローチ
**HTMLではプレースホルダーを使用 → WP上で置換**

```html
<!-- HTML内 -->
<h4>✓ こんな方におすすめ</h4>
<!-- ↓ WP上でVK Blocksアイコンに置換 -->
```

### 推奨Font Awesomeアイコン一覧

| 用途 | アイコン名 | クラス |
|-----|----------|--------|
| チェックマーク | Check | `fas fa-check` |
| チェック（円） | Check Circle | `fas fa-check-circle` |
| リスト | List | `fas fa-list` または `fas fa-bars` |
| おすすめ | Star | `fas fa-star` |
| ユーザー | User | `fas fa-user` |
| 会社・建物 | Building | `fas fa-building` |
| 電話 | Phone | `fas fa-phone` |
| メール | Envelope | `fas fa-envelope` |
| 場所 | Map Marker | `fas fa-map-marker-alt` |
| 時計 | Clock | `fas fa-clock` |
| 書類 | File | `fas fa-file-alt` |
| 計算機 | Calculator | `fas fa-calculator` |
| 握手 | Handshake | `fas fa-handshake` |
| ビデオ | Video | `fas fa-video` |

### VK Blocksアイコン設定手順（WP上）

1. 置換したいテキスト/パラグラフを選択 → 削除
2. 「＋」→「アイコン」（VK Blocks）を追加
3. アイコン選択画面でFont Awesomeを検索
4. サイズ設定（例: 16px〜48px）
5. 色設定（例: `#1a365d` 紺色、`#5a7a54` 緑色）

---

## services.html のアイコン置換リスト

以下はWP上でVK Blocksアイコンに置換推奨：

| 現在の表示 | 推奨アイコン | 色 |
|-----------|------------|-----|
| ✓ こんな方におすすめ | `fas fa-check-circle` | #1a365d |
| ≡ 主な対応業務 | `fas fa-list` | #1a365d |
