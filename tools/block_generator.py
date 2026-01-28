#!/usr/bin/env python3
"""
WordPress Block HTML Generator
構造化データ（JSON/YAML）からWordPressブロックHTMLを生成

使用方法:
    python block_generator.py input.json > output.html
    python block_generator.py input.yaml > output.html
"""

import json
import sys
import io
from pathlib import Path

# Windows環境でのUTF-8出力対応
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

class BlockGenerator:
    """WordPressブロックHTMLジェネレーター"""
    
    def __init__(self):
        self.output = []
        self.h2_counter = 0  # h2のナンバリング用カウンター
    
    def generate(self, data: dict) -> str:
        """メイン生成関数"""
        self.output = []
        self.h2_counter = 0  # h2カウンターをリセット
        
        # ① リード文（あれば）
        if 'lead' in data:
            self.output.append(self._paragraph({'text': data['lead']}))
        
        # ② この記事のポイント（あれば）
        # ※目次はVK Blocksで自動挿入（最初のh2の前）
        if 'points' in data:
            self.output.append(self._conclusion_box(data['points']))
        
        # ③ セクションを順番に処理
        for section in data.get('sections', []):
            self._process_section(section)
        
        # ④ まとめ（あれば）
        if 'summary' in data:
            self.output.append(self._summary_box(data['summary']))
        
        # 旧形式との互換性
        if 'conclusion' in data and 'points' not in data:
            self.output.insert(0, self._conclusion_box(data['conclusion']))
        
        return '\n\n'.join(self.output)
    
    def _process_section(self, section: dict):
        """セクションタイプに応じて処理を振り分け"""
        section_type = section.get('type', 'paragraph')
        
        handlers = {
            'heading': self._heading,
            'paragraph': self._paragraph,
            'list': self._list,
            'faq': self._faq,
            'box': self._box,
            'warning': self._warning_box,
            'table': self._table,
            'spacer': self._spacer,
        }
        
        handler = handlers.get(section_type, self._paragraph)
        result = handler(section)
        if result:
            self.output.append(result)
    
    # ========== 基本ブロック ==========
    
    def _heading(self, section: dict) -> str:
        """見出しブロック"""
        level = section.get('level', 2)
        text = section.get('text', '')
        
        result = ''
        
        # h2の場合: VK Heading Style + スペーサー
        if level == 2:
            self.h2_counter += 1
            # VK Heading Style（下線付き、プライマリカラー、マージン/パディング込み）
            result += f'''<!-- wp:heading {{"className":"is-style-vk-heading-01 is-style-default","style":{{"typography":{{"fontSize":"1.625rem","fontStyle":"normal","fontWeight":"700"}},"spacing":{{"margin":{{"top":"30px","bottom":"20px"}},"padding":{{"bottom":"10px"}}}},"border":{{"bottom":{{"color":"var:preset|color|vk-color-primary-dark","width":"2px"}},"top":{{}},"right":{{}},"left":{{}}}}}},"textColor":"vk-color-primary-dark"}} -->
<h2 class="wp-block-heading is-style-vk-heading-01 is-style-default has-vk-color-primary-dark-color has-text-color" style="border-bottom-color:var(--wp--preset--color--vk-color-primary-dark);border-bottom-width:2px;margin-top:30px;margin-bottom:20px;padding-bottom:10px;font-size:1.625rem;font-style:normal;font-weight:700">{text}</h2>
<!-- /wp:heading -->'''
        
        # h3の場合: 左ボーダースタイル
        elif level == 3:
            result += f'''<!-- wp:heading {{"level":3,"style":{{"border":{{"left":{{"color":"#1a365d","width":"6px"}},"top":{{}},"right":{{}},"bottom":{{}}}},"spacing":{{"padding":{{"left":"10px","top":"5px","bottom":"5px"}},"margin":{{"left":"0","top":"30px","bottom":"20px"}}}},"typography":{{"fontWeight":"700","fontStyle":"normal","fontSize":"1.25rem"}}}}}} -->
<h3 class="wp-block-heading" style="border-left-color:#1a365d;border-left-width:6px;margin-top:30px;margin-bottom:20px;margin-left:0;padding-top:5px;padding-bottom:5px;padding-left:10px;font-size:1.25rem;font-style:normal;font-weight:700">{text}</h3>
<!-- /wp:heading -->'''
        
        # h4の場合: 通常スタイル
        else:
            result += f'''<!-- wp:heading {{"level":{level},"className":"vk_block-margin-sm\\u002d\\u002dmargin-bottom","style":{{"typography":{{"fontWeight":"600","fontStyle":"normal"}}}},"fontSize":"regular"}} -->
<h{level} class="wp-block-heading vk_block-margin-sm--margin-bottom has-regular-font-size" style="font-style:normal;font-weight:600">{text}</h{level}>
<!-- /wp:heading -->'''
        
        return result
    
    def _paragraph(self, section: dict) -> str:
        """段落ブロック"""
        text = section.get('text', '')
        if isinstance(section, str):
            text = section
        
        return f'''<!-- wp:paragraph {{"style":{{"typography":{{"lineHeight":"1.8"}}}}}} -->
<p style="line-height:1.8">{text}</p>
<!-- /wp:paragraph -->'''
    
    def _list(self, section: dict) -> str:
        """リストブロック"""
        items = section.get('items', [])
        ordered = section.get('ordered', False)
        
        tag = 'ol' if ordered else 'ul'
        list_items = '\n'.join([
            f'''<!-- wp:list-item -->
<li>{item}</li>
<!-- /wp:list-item -->'''
            for item in items
        ])
        
        return f'''<!-- wp:list -->
<{tag} class="wp-block-list">
{list_items}
</{tag}>
<!-- /wp:list -->'''
    
    def _spacer(self, section: dict) -> str:
        """スペーサーブロック"""
        height = section.get('height', '2rem')
        return f'''<!-- wp:spacer {{"height":"{height}"}} -->
<div style="height:{height}" aria-hidden="true" class="wp-block-spacer"></div>
<!-- /wp:spacer -->'''
    
    # ========== VK Blocks コンポーネント ==========
    
    def _conclusion_box(self, content) -> str:
        """結論ボックス（VK Blocks Border Box）"""
        # タイトル取得
        if isinstance(content, str):
            items = [content]
            title = "この記事のポイント"
        elif isinstance(content, dict):
            items = content.get('items', [content.get('text', '')])
            title = content.get('title', 'この記事のポイント')
        else:
            items = content
            title = "この記事のポイント"
        
        # リストアイテムを生成
        list_items = '\n'.join([
            f'''<!-- wp:list-item -->
<li>{item}</li>
<!-- /wp:list-item -->'''
            for item in items
        ])
        
        return f'''<!-- wp:vk-blocks/border-box {{"headingTag":"h3","includeInToc":false,"faIcon":"\\u003ci class=\\u0022fa-solid fa-circle-info\\u0022\\u003e\\u003c/i\\u003e","className":"is-style-vk_borderBox-style-solid-kado-tit-banner"}} -->
<div class="wp-block-vk-blocks-border-box vk_borderBox vk_borderBox-background-transparent is-style-vk_borderBox-style-solid-kado-tit-banner"><div class="vk_borderBox_title_container"><i class="fa-solid fa-circle-info"></i><h3 class="vk_borderBox_title">{title}</h3></div><div class="vk_borderBox_body"><!-- wp:list -->
<ul class="wp-block-list">
{list_items}
</ul>
<!-- /wp:list --></div></div>
<!-- /wp:vk-blocks/border-box -->'''
    
    def _summary_box(self, content) -> str:
        """まとめボックス（VK Blocks Border Box）"""
        if isinstance(content, str):
            items = [content]
            title = "まとめ"
        elif isinstance(content, dict):
            items = content.get('items', [content.get('text', '')])
            title = content.get('title', 'まとめ')
        else:
            items = content
            title = "まとめ"
        
        list_items = '\n'.join([
            f'''<!-- wp:list-item -->
<li>{item}</li>
<!-- /wp:list-item -->'''
            for item in items
        ])
        
        return f'''<!-- wp:vk-blocks/border-box {{"headingTag":"h3","includeInToc":false,"faIcon":"\\u003ci class=\\u0022fa-solid fa-check\\u0022\\u003e\\u003c/i\\u003e","className":"is-style-vk_borderBox-style-solid-kado-tit-banner"}} -->
<div class="wp-block-vk-blocks-border-box vk_borderBox vk_borderBox-background-transparent is-style-vk_borderBox-style-solid-kado-tit-banner"><div class="vk_borderBox_title_container"><i class="fa-solid fa-check"></i><h3 class="vk_borderBox_title">{title}</h3></div><div class="vk_borderBox_body"><!-- wp:list -->
<ul class="wp-block-list">
{list_items}
</ul>
<!-- /wp:list --></div></div>
<!-- /wp:vk-blocks/border-box -->'''
    
    def _box(self, section: dict) -> str:
        """汎用ボックス"""
        title = section.get('title', '')
        content = section.get('content', '')
        style = section.get('style', 'info')  # info, success, warning
        
        colors = {
            'info': {'border': '#1a365d', 'bg': 'white'},
            'success': {'border': '#5a7a54', 'bg': 'white'},
            'warning': {'border': '#c9a227', 'bg': 'white'},
        }
        color = colors.get(style, colors['info'])
        
        title_block = ''
        if title:
            title_block = f'''<!-- wp:heading {{"level":4,"className":"vk_block-margin-sm\\u002d\\u002dmargin-bottom","style":{{"typography":{{"fontWeight":"600"}}}}}} -->
<h4 class="wp-block-heading vk_block-margin-sm--margin-bottom" style="font-weight:600">{title}</h4>
<!-- /wp:heading -->

'''
        
        return f'''<!-- wp:group {{"style":{{"border":{{"width":"1px","color":"{color['border']}"}},"spacing":{{"padding":{{"top":"1.5rem","right":"1.5rem","bottom":"1.5rem","left":"1.5rem"}}}}}},"backgroundColor":"{color['bg']}","layout":{{"type":"constrained"}}}} -->
<div class="wp-block-group has-{color['bg']}-background-color has-background" style="border:1px solid {color['border']};padding:1.5rem">{title_block}<!-- wp:paragraph -->
<p>{content}</p>
<!-- /wp:paragraph --></div>
<!-- /wp:group -->'''
    
    def _table(self, section: dict) -> str:
        """表ブロック（WordPress標準テーブル）"""
        headers = section.get('headers', [])
        rows = section.get('rows', [])
        caption = section.get('caption', '')
        has_fixed_layout = section.get('fixed_layout', False)
        
        # ヘッダー行の生成
        header_html = ''
        if headers:
            header_cells = ''.join([f'<th>{cell}</th>' for cell in headers])
            header_html = f'<thead><tr>{header_cells}</tr></thead>'
        
        # ボディ行の生成
        body_rows = []
        for row in rows:
            cells = ''.join([f'<td>{cell}</td>' for cell in row])
            body_rows.append(f'<tr>{cells}</tr>')
        body_html = f'<tbody>{"".join(body_rows)}</tbody>'
        
        # キャプションの生成
        caption_html = ''
        if caption:
            caption_html = f'<figcaption class="wp-element-caption">{caption}</figcaption>'
        
        # テーブル属性
        table_attrs = {
            "hasFixedLayout": has_fixed_layout,
            "className": "is-style-stripes"
        }
        if headers:
            table_attrs["head"] = [[{"content": h, "tag": "th"} for h in headers]]
        if rows:
            table_attrs["body"] = [[{"content": cell, "tag": "td"} for cell in row] for row in rows]
        
        return f'''<!-- wp:table {{"hasFixedLayout":false,"className":"post-table is-style-regular","style":{{"border":{{"width":"1px"}}}},"borderColor":"black"}} -->
<figure class="wp-block-table post-table is-style-regular"><table class="has-border-color has-black-border-color" style="border-width:1px">{header_html}{body_html}</table>{caption_html}</figure>
<!-- /wp:table -->'''
    
    def _warning_box(self, section: dict) -> str:
        """警告ボックス（VK Blocks Alert）"""
        content = section.get('content', section.get('text', ''))
        
        return f'''<!-- wp:vk-blocks/alert {{"style":"warning","icon":"\\u003ci class=\\u0022fa-solid fa-triangle-exclamation\\u0022\\u003e\\u003c/i\\u003e","iconText":"Warning"}} -->
<div class="wp-block-vk-blocks-alert vk_alert alert alert-warning has-alert-icon"><div class="vk_alert_icon"><div class="vk_alert_icon_icon"><i class="fa-solid fa-triangle-exclamation"></i></div><div class="vk_alert_icon_text"><span>Warning</span></div></div><div class="vk_alert_content"><!-- wp:paragraph {{"fontSize":"regular"}} -->
<p class="has-regular-font-size">{content}</p>
<!-- /wp:paragraph --></div></div>
<!-- /wp:vk-blocks/alert -->'''
    
    def _faq(self, section: dict) -> str:
        """FAQブロック（VK Blocks FAQ2形式）"""
        q = section.get('q', section.get('question', ''))
        a = section.get('a', section.get('answer', ''))
        
        return f'''<!-- wp:vk-blocks/faq2 {{"className":"is-style-vk_faq-bgfill-rounded"}} -->
<div class="wp-block-vk-blocks-faq2 vk_faq  [accordion_trigger_switch] is-style-vk_faq-bgfill-rounded"><div class="vk_faq-header"></div><dl class="vk_faq-body"><!-- wp:vk-blocks/faq2-q -->
<dt class="wp-block-vk-blocks-faq2-q vk_faq_title" aria-label="質問"><!-- wp:paragraph {{"fontSize":"regular"}} -->
<p class="has-regular-font-size">{q}</p>
<!-- /wp:paragraph --></dt>
<!-- /wp:vk-blocks/faq2-q -->

<!-- wp:vk-blocks/faq2-a -->
<dd class="wp-block-vk-blocks-faq2-a vk_faq_content" aria-label="回答"><!-- wp:paragraph {{"fontSize":"regular"}} -->
<p class="has-regular-font-size">{a}</p>
<!-- /wp:paragraph --></dd>
<!-- /wp:vk-blocks/faq2-a --></dl><div class="vk_faq-footer"></div></div>
<!-- /wp:vk-blocks/faq2 -->'''


def load_data(filepath: str) -> dict:
    """JSONまたはYAMLファイルを読み込む"""
    path = Path(filepath)
    content = path.read_text(encoding='utf-8')
    
    if path.suffix in ['.yaml', '.yml']:
        try:
            import yaml
            return yaml.safe_load(content)
        except ImportError:
            print("Error: PyYAML is not installed. Use 'pip install pyyaml'", file=sys.stderr)
            sys.exit(1)
    else:
        return json.loads(content)


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='構造化データからWordPressブロックHTMLを生成')
    parser.add_argument('input', nargs='?', help='入力ファイル (JSON/YAML)')
    parser.add_argument('-o', '--output', help='出力ファイル')
    args = parser.parse_args()
    
    if args.input is None:
        # サンプルデータで実行
        sample_data = {
            "conclusion": [
                "入社後5日以内に届出が必要です",
                "必要書類は事前に確認しましょう",
                "不明点は社労士に相談できます"
            ],
            "sections": [
                {"type": "heading", "level": 2, "text": "入社手続きの流れ"},
                {"type": "paragraph", "text": "従業員を採用したら、社会保険と雇用保険の届出が必要です。"},
                {"type": "list", "items": ["年金手帳", "雇用保険被保険者証", "マイナンバー"]},
                {"type": "warning", "title": "注意", "content": "届出期限を過ぎると罰則の対象になる場合があります。"},
                {"type": "faq", "q": "届出期限はいつですか？", "a": "入社日から5日以内に届出が必要です。"}
            ]
        }
        data = sample_data
    else:
        data = load_data(args.input)
    
    generator = BlockGenerator()
    result = generator.generate(data)
    
    if args.output:
        Path(args.output).write_text(result, encoding='utf-8')
        print(f"Generated: {args.output}")
    else:
        print(result)


if __name__ == '__main__':
    main()
