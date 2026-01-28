## MOD_CONCLUSION_BOX（結論ボックス）

### 仕様
- ブロック：VK Blocks / 枠線ボックス（border-box）
- タイトル要素：H4（デフォルト）
- 目次：includeInToc は原則 false（目次が肥大化しやすいため）
- 結論文（太字1文）：本文より少し大きく（推奨 1.1rem、許容 1.05〜1.15rem）
- ポイント（箇条書き）：本文と同サイズ（拡大しない）

### ブロックHTML（標準版）
```html
<!-- wp:vk-blocks/border-box {"includeInToc":false,"bgColor":"white","faIcon":"<i class=\"fa-solid fa-check\"></i>","className":"is-style-vk_borderBox-style-solid-kado-tit-banner"} -->
<div class="wp-block-vk-blocks-border-box vk_borderBox vk_borderBox-background-white is-style-vk_borderBox-style-solid-kado-tit-banner"><div class="vk_borderBox_title_container"><i class="fa-solid fa-check"></i><h4 class="vk_borderBox_title">この記事の結論</h4></div><div class="vk_borderBox_body">
<!-- wp:paragraph {"style":{"typography":{"fontSize":"1.1rem"}}} -->
<p style="font-size:1.1rem"><strong>【結論の文章】</strong></p>
<!-- /wp:paragraph -->

<!-- wp:list -->
<ul class="wp-block-list">
  <li>【ポイント１】</li>
  <li>【ポイント２】</li>
  <li>【ポイント３】</li>
</ul>
<!-- /wp:list -->
</div></div>
<!-- /wp:vk-blocks/border-box -->