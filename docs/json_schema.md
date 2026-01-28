# JSON スキーマ仕様書

`block_generator.py` が処理するJSONファイルのフォーマット仕様です。

## 基本構造

```json
{
  "lead": "リード文（記事冒頭の導入文）",
  "points": {
    "title": "この記事のポイント",
    "items": ["ポイント1", "ポイント2", "ポイント3"]
  },
  "sections": [
    // 各ブロックを配列で記述
  ],
  "summary": {
    "title": "まとめ",
    "items": ["要点1", "要点2", "要点3"]
  }
}
```

---

## ブロックタイプ一覧

### heading（見出し）

```json
{"type": "heading", "level": 2, "text": "見出しテキスト"}
{"type": "heading", "level": 3, "text": "小見出しテキスト"}
```

| プロパティ | 型 | 説明 |
|------------|-----|------|
| level | int | 2（h2）または 3（h3） |
| text | string | 見出しテキスト |

---

### paragraph（段落）

```json
{"type": "paragraph", "text": "本文テキスト。<strong>強調</strong>も可能。"}
```

| プロパティ | 型 | 説明 |
|------------|-----|------|
| text | string | 段落テキスト（HTMLタグ使用可） |

**対応HTMLタグ**: `<strong>`, `<br>`

---

### list（箇条書き）

```json
{"type": "list", "items": ["項目1", "項目2", "項目3"]}
```

| プロパティ | 型 | 説明 |
|------------|-----|------|
| items | array[string] | リスト項目（最大6個推奨） |

---

### warning（警告ボックス）

```json
{"type": "warning", "content": "注意すべき内容"}
```

| プロパティ | 型 | 説明 |
|------------|-----|------|
| content | string | 警告メッセージ |

**用途**: 期限、罰則、よくあるミス

---

### table（表）

```json
{
  "type": "table",
  "headers": ["列1", "列2", "列3"],
  "rows": [
    ["値1-1", "値1-2", "値1-3"],
    ["値2-1", "値2-2", "値2-3"]
  ],
  "caption": "表のキャプション（任意）"
}
```

| プロパティ | 型 | 説明 |
|------------|-----|------|
| headers | array[string] | ヘッダー行 |
| rows | array[array[string]] | データ行 |
| caption | string | キャプション（省略可） |

---

### faq（よくある質問）

```json
{"type": "faq", "q": "質問文？", "a": "回答文。"}
```

| プロパティ | 型 | 説明 |
|------------|-----|------|
| q | string | 質問文 |
| a | string | 回答文 |

---

## 生成されるVK Blocksコンポーネント

| JSONタイプ | VK Blocksコンポーネント |
|------------|------------------------|
| lead | `wp:paragraph` |
| points | `wp:vk-blocks/border-box`（info） |
| heading level:2 | `wp:heading`（下線付き） |
| heading level:3 | `wp:heading`（左ボーダー） |
| paragraph | `wp:paragraph` |
| list | `wp:list` |
| warning | `wp:vk-blocks/alert`（warning） |
| table | `wp:table`（post-table） |
| faq | `wp:vk-blocks/faq2` |
| summary | `wp:vk-blocks/border-box`（check） |

---

## サンプルファイル

- `block-html/posts/hiring_procedures.json` - 入社手続き記事
- `block-html/posts/midnight_allowance.json` - 深夜手当記事

---

## HTML化コマンド

```bash
py tools/block_generator.py block-html/posts/[ファイル名].json -o block-html/posts/[ファイル名].txt
```
