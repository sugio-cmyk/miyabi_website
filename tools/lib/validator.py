"""
Validator - 構造バリデーションモジュール
生成されたJSONの品質をチェック
"""
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class ValidationResult:
    """バリデーション結果"""
    is_valid: bool = True
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    
    def add_error(self, code: str, message: str):
        """エラーを追加"""
        self.errors.append(f"[{code}] {message}")
        self.is_valid = False
    
    def add_warning(self, code: str, message: str):
        """警告を追加"""
        self.warnings.append(f"[{code}] {message}")
    
    def has_warnings(self) -> bool:
        """警告があるか"""
        return len(self.warnings) > 0
    
    def format_report(self) -> str:
        """レポート形式で出力"""
        lines = ["[Validation]"]
        
        if self.errors:
            for err in self.errors:
                lines.append(f"  ✗ Error: {err}")
        
        if self.warnings:
            for warn in self.warnings:
                lines.append(f"  ⚠ Warning: {warn}")
        
        if not self.errors and not self.warnings:
            lines.append("  ✓ すべてのチェックに合格しました")
        
        if self.is_valid:
            if self.warnings:
                lines.append(f"\n結果: {len(self.warnings)}件の警告あり（続行可能）")
            else:
                lines.append("\n結果: 問題なし")
        else:
            lines.append(f"\n結果: {len(self.errors)}件のエラーあり（続行不可）")
        
        return "\n".join(lines)


class Validator:
    """記事JSONの品質をチェックするクラス"""
    
    # バリデーションルール設定
    MIN_H2_COUNT = 3
    MAX_H2_COUNT = 5
    REQUIRED_POINTS_ITEMS = 3
    MIN_SUMMARY_ITEMS = 4
    MIN_FAQ_COUNT = 2
    
    def validate(self, article_json: dict) -> ValidationResult:
        """
        JSONの構造を検証
        
        Args:
            article_json: 構造化された記事JSON（raw_json形式）
            
        Returns:
            ValidationResult: バリデーション結果
        """
        result = ValidationResult()
        
        # 1. 必須フィールドチェック
        self._check_required_fields(article_json, result)
        
        # 2. H2見出しチェック
        self._check_headings(article_json, result)
        
        # 3. ブロック種類チェック
        self._check_block_types(article_json, result)
        
        # 4. pointsチェック
        self._check_points(article_json, result)
        
        # 5. summaryチェック
        self._check_summary(article_json, result)
        
        return result
    
    def _check_required_fields(self, data: dict, result: ValidationResult):
        """必須フィールドの存在チェック"""
        # lead
        if not data.get('lead'):
            result.add_error('ERR-003', 'leadが存在しません')
        
        # sections
        if not data.get('sections'):
            result.add_error('ERR-001', 'sectionsが存在しません')
        
        # summary
        if not data.get('summary'):
            result.add_error('ERR-002', 'summaryが存在しません')
    
    def _check_headings(self, data: dict, result: ValidationResult):
        """H2見出しの数をチェック"""
        sections = data.get('sections', [])
        
        h2_count = sum(
            1 for s in sections 
            if s.get('type') == 'heading' and s.get('level') == 2
        )
        
        if h2_count == 0:
            result.add_error('ERR-001', 'h2見出しが0個です')
        elif h2_count < self.MIN_H2_COUNT:
            result.add_warning('WRN-001', f'h2が{h2_count}個（推奨: {self.MIN_H2_COUNT}〜{self.MAX_H2_COUNT}個）')
        elif h2_count > self.MAX_H2_COUNT:
            result.add_warning('WRN-001', f'h2が{h2_count}個（推奨: {self.MIN_H2_COUNT}〜{self.MAX_H2_COUNT}個）')
    
    def _check_block_types(self, data: dict, result: ValidationResult):
        """ブロック種類の多様性をチェック"""
        sections = data.get('sections', [])
        
        types_used = set(s.get('type') for s in sections)
        
        has_table = 'table' in types_used
        has_warning = 'warning' in types_used
        has_faq = 'faq' in types_used
        has_list = 'list' in types_used
        
        # table/warningのどちらも無い
        if not has_table and not has_warning:
            result.add_warning('WRN-002', 'tableとwarningがどちらもありません（どちらか1つ推奨）')
        
        # FAQ数チェック
        faq_count = sum(1 for s in sections if s.get('type') == 'faq')
        # faqブロック内のitems数もカウント
        faq_items_count = 0
        for s in sections:
            if s.get('type') == 'faq':
                items = s.get('items', [])
                if isinstance(items, list):
                    faq_items_count += len(items)
        
        if faq_items_count < self.MIN_FAQ_COUNT:
            result.add_warning('WRN-003', f'FAQが{faq_items_count}個（{self.MIN_FAQ_COUNT}個以上推奨）')
    
    def _check_points(self, data: dict, result: ValidationResult):
        """pointsの項目数チェック"""
        points = data.get('points', {})
        items = points.get('items', [])
        
        if len(items) != self.REQUIRED_POINTS_ITEMS:
            result.add_warning('WRN-004', f'pointsが{len(items)}項目（{self.REQUIRED_POINTS_ITEMS}項目推奨）')
    
    def _check_summary(self, data: dict, result: ValidationResult):
        """summaryの項目数チェック"""
        summary = data.get('summary', {})
        items = summary.get('items', [])
        
        if len(items) < self.MIN_SUMMARY_ITEMS:
            result.add_warning('WRN-005', f'summaryが{len(items)}項目（{self.MIN_SUMMARY_ITEMS}項目以上推奨）')


if __name__ == "__main__":
    # テスト用
    test_json = {
        "lead": "これはテストのリード文です。",
        "points": {
            "title": "ポイント",
            "items": ["ポイント1", "ポイント2", "ポイント3"]
        },
        "sections": [
            {"type": "heading", "level": 2, "text": "見出し1"},
            {"type": "paragraph", "text": "本文"},
            {"type": "heading", "level": 2, "text": "見出し2"},
            {"type": "paragraph", "text": "本文"},
            {"type": "heading", "level": 2, "text": "見出し3"},
            {"type": "list", "items": ["項目1", "項目2"]},
            {"type": "faq", "items": [{"q": "質問?", "a": "回答。"}]},
        ],
        "summary": {
            "title": "まとめ",
            "items": ["まとめ1", "まとめ2", "まとめ3", "まとめ4"]
        }
    }
    
    validator = Validator()
    result = validator.validate(test_json)
    print(result.format_report())
