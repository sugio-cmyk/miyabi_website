# VK Blocks & Lightning Design Patterns (Knowledge Base)

このプロジェクトで使用している主要な VK Blocks パターンとデザインナレッジのまとめです。
再利用する際は、以下のHTMLをブロックエディタの「コードエディター」モードに貼り付けてください。

## 1. アイコン (VK Blocks Icon)

### 枠線付きアイコン（信頼バッジ等で使用）
```html
<!-- wp:vk-blocks/icon {"faIcon":"<i class=\"fas fa-user-tie\"></i>","iconSize":48,"iconAlign":"center","iconColor":"#1a365d"} -->
<div class="wp-block-vk-blocks-icon vk_icon">
    <div class="vk_icon_frame text-center">
        <div class="vk_icon_border has-background"
            style="background-color:#1a365d;width:calc(48px + 44px);height:calc(48px + 44px)"><i
                style="font-size:48px" class="fas vk_icon_font fa-user-tie"></i></div>
    </div>
</div>
<!-- /wp:vk-blocks/icon -->
```

### シンプルなアイコン（リスト内などで使用）
```html
<!-- wp:vk-blocks/icon {"faIcon":"<i class=\"fas fa-check-circle\"></i>","iconSize":16,"iconMargin":6,"iconType":"2","iconColor":"#1a365d"} -->
<div class="wp-block-vk-blocks-icon vk_icon">
    <div class="vk_icon_frame is-style-noline">
        <div class="vk_icon_border has-text-color"
            style="color:#1a365d;width:calc(16px + 12px);height:calc(16px + 12px)"><i
                style="font-size:16px" class="fas vk_icon_font fa-check-circle"></i></div>
    </div>
</div>
<!-- /wp:vk-blocks/icon -->
```

## 2. FAQ (VK Blocks FAQ2)

アコーディオン開閉式のQ&Aブロックです。

```html
<!-- wp:vk-blocks/faq2 -->
<div class="wp-block-vk-blocks-faq2 vk_faq  [accordion_trigger_switch]">
    <div class="vk_faq-header"></div>
    <dl class="vk_faq-body"><!-- wp:vk-blocks/faq2-q -->
        <dt class="wp-block-vk-blocks-faq2-q vk_faq_title" aria-label="質問"><!-- wp:paragraph -->
            <p>ここに質問を入力してください</p>
            <!-- /wp:paragraph -->
        </dt>
        <!-- /wp:vk-blocks/faq2-q -->

        <!-- wp:vk-blocks/faq2-a -->
        <dd class="wp-block-vk-blocks-faq2-a vk_faq_content" aria-label="回答"><!-- wp:paragraph -->
            <p>ここに回答を入力してください。</p>
            <!-- /wp:paragraph -->
        </dd>
        <!-- /wp:vk-blocks/faq2-a -->
    </dl>
    <div class="vk_faq-footer"></div>
</div>
<!-- /wp:vk-blocks/faq2 -->
```

## 3. カードデザイン (Group + Shadow)

### サービスカード（画像丸角 + 影付き）
Lightning標準のスタイルクラス `is-style-vk-group-shadow` と `is-style-vk-image-rounded` を組み合わせたパターンです。

```html
<!-- wp:group {"className":"is-style-vk-group-shadow","style":{"border":{"radius":{"topLeft":"14px","topRight":"14px","bottomLeft":"14px","bottomRight":"14px"},"width":"1px","color":"#e2e8f0"}},"layout":{"type":"constrained"}} -->
<div class="wp-block-group is-style-vk-group-shadow has-border-color"
    style="border-color:#e2e8f0;border-width:1px;border-top-left-radius:14px;border-top-right-radius:14px;border-bottom-left-radius:14px;border-bottom-right-radius:14px">
    
    <!-- 画像 (丸角スタイル) -->
    <!-- wp:image {"aspectRatio":"16/9","scale":"cover","sizeSlug":"full","linkDestination":"none","className":"is-style-vk-image-rounded","style":{"border":{"radius":{"topLeft":"14px","topRight":"14px","bottomLeft":"14px","bottomRight":"14px"}}}} -->
    <figure class="wp-block-image size-full has-custom-border is-style-vk-image-rounded"><img
            src="[画像URL]" alt=""
            style="border-top-left-radius:14px;border-top-right-radius:14px;border-bottom-left-radius:14px;border-bottom-right-radius:14px;aspect-ratio:16/9;object-fit:cover" />
    </figure>
    <!-- /wp:image -->

    <!-- コンテンツエリア -->
    <!-- wp:group {"style":{"spacing":{"padding":{"top":"25px","right":"25px","bottom":"30px","left":"25px"}}},"layout":{"type":"constrained"}} -->
    <div class="wp-block-group"
        style="padding-top:25px;padding-right:25px;padding-bottom:30px;padding-left:25px">
        <!-- wp:heading {"textAlign":"center","level":3,"style":{"typography":{"fontSize":"18px","fontWeight":"600"},"spacing":{"margin":{"bottom":"15px"}}}} -->
        <h3 class="wp-block-heading has-text-align-center"
            style="margin-bottom:15px;font-size:18px;font-weight:600">タイトル</h3>
        <!-- /wp:heading -->

        <!-- wp:paragraph {"align":"center"} -->
        <p class="has-text-align-center">説明文をここに入力します。</p>
        <!-- /wp:paragraph -->
    </div>
    <!-- /wp:group -->
</div>
<!-- /wp:group -->
```

### 特徴・理由カード（アイコン + 影付き）

```html
<!-- wp:group {"className":"is-style-vk-group-shadow","style":{"spacing":{"padding":{"top":"40px","right":"30px","bottom":"40px","left":"30px"}},"border":{"radius":{"topLeft":"14px","topRight":"14px","bottomLeft":"14px","bottomRight":"14px"}},"dimensions":{"minHeight":"100%"}},"backgroundColor":"white","layout":{"type":"constrained"}} -->
<div class="wp-block-group is-style-vk-group-shadow has-white-background-color has-background"
    style="border-top-left-radius:14px;border-top-right-radius:14px;border-bottom-left-radius:14px;border-bottom-right-radius:14px;min-height:100%;padding-top:40px;padding-right:30px;padding-bottom:40px;padding-left:30px">
    
    <!-- アイコン -->
    <!-- wp:vk-blocks/icon {"faIcon":"<i class=\"fas fa-handshake\"></i>","iconSize":56,"iconAlign":"center","iconColor":"#5a7a54"} -->
    <div class="wp-block-vk-blocks-icon vk_icon">
        <div class="vk_icon_frame text-center">
            <div class="vk_icon_border has-background"
                style="background-color:#5a7a54;width:calc(56px + 44px);height:calc(56px + 44px)"><i
                    style="font-size:56px" class="fas vk_icon_font fa-handshake"></i></div>
        </div>
    </div>
    <!-- /wp:vk-blocks/icon -->

    <!-- wp:spacer {"height":"15px"} -->
    <div style="height:15px" aria-hidden="true" class="wp-block-spacer"></div>
    <!-- /wp:spacer -->

    <!-- wp:heading {"textAlign":"center","level":3} -->
    <h3 class="wp-block-heading has-text-align-center">タイトル</h3>
    <!-- /wp:heading -->

    <!-- wp:paragraph {"align":"center"} -->
    <p class="has-text-align-center">説明文</p>
    <!-- /wp:paragraph -->
</div>
<!-- /wp:group -->
```

## 4. 料金カード (Pricing Table Like)

`vk-shadow-lv2` クラスを使用した、少しのシャドウを持つカードデザインです。

```html
<!-- wp:group {"className":"vk-shadow-lv2","style":{"border":{"radius":"16px"},"spacing":{"padding":{"top":"30px","right":"25px","bottom":"30px","left":"25px"}}},"backgroundColor":"white","layout":{"type":"constrained"}} -->
<div class="wp-block-group vk-shadow-lv2 has-white-background-color has-background"
    style="border-radius:16px;padding-top:30px;padding-right:25px;padding-bottom:30px;padding-left:25px">
    
    <!-- プラン名 -->
    <!-- wp:heading {"textAlign":"center","level":3,"style":{"typography":{"fontSize":"18px","fontWeight":"600"},"spacing":{"margin":{"bottom":"15px"}}}} -->
    <h3 class="wp-block-heading has-text-align-center"
        style="margin-bottom:15px;font-size:18px;font-weight:600">プラン名</h3>
    <!-- /wp:heading -->

    <!-- 価格 -->
    <!-- wp:paragraph {"align":"center","style":{"typography":{"fontSize":"28px","fontWeight":"700"},"color":{"text":"#1a365d"},"spacing":{"margin":{"bottom":"10px"}}}} -->
    <p class="has-text-align-center has-text-color"
        style="color:#1a365d;margin-bottom:10px;font-size:28px;font-weight:700">10,000円〜</p>
    <!-- /wp:paragraph -->

    <!-- 補足 -->
    <!-- wp:paragraph {"align":"center","style":{"typography":{"fontSize":"13px"},"color":{"text":"#666666"}}} -->
    <p class="has-text-align-center has-text-color" style="color:#666666;font-size:13px">補足テキスト</p>
    <!-- /wp:paragraph -->
</div>
<!-- /wp:group -->
```

## 5. ボタン (VK Color Primary)

テーマカラー（`vk-color-primary`）を適用したボタンです。

```html
<!-- wp:buttons {"layout":{"type":"flex","justifyContent":"center"}} -->
<div class="wp-block-buttons">
    <!-- wp:button {"backgroundColor":"vk-color-primary","style":{"border":{"radius":{"topLeft":"12px","topRight":"12px","bottomLeft":"12px","bottomRight":"12px"}},"typography":{"fontSize":"14px"},"spacing":{"padding":{"left":"30px","right":"30px","top":"14px","bottom":"14px"}}}} -->
    <div class="wp-block-button"><a
            class="wp-block-button__link has-vk-color-primary-background-color has-background has-custom-font-size wp-element-button"
            href="#"
            style="border-top-left-radius:12px;border-top-right-radius:12px;border-bottom-left-radius:12px;border-bottom-right-radius:12px;padding-top:14px;padding-right:30px;padding-bottom:14px;padding-left:30px;font-size:14px">詳しく見る</a>
    </div>
    <!-- /wp:button -->
</div>
<!-- /wp:buttons -->
```
