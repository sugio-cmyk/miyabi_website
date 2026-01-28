"""
Loader - 原稿ファイル読込モジュール
"""
import yaml
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass
class Draft:
    """原稿データを格納するクラス"""
    title: str
    slug: str
    description: str
    content: str
    category: Optional[str] = None
    tags: Optional[list[str]] = None
    status: str = "draft"
    featured_image: Optional[str] = None
    scheduled_at: Optional[str] = None
    source_file: Optional[str] = None


class LoaderError(Exception):
    """Loader関連のエラー"""
    pass


class Loader:
    """Markdownファイルから原稿を読み込むクラス"""
    
    # 必須フィールド
    REQUIRED_FIELDS = ['title', 'slug', 'description']
    
    def load(self, file_path: str) -> Draft:
        """
        Markdownファイルを読み込み、Draftオブジェクトを返す
        
        Args:
            file_path: 原稿ファイルのパス
            
        Returns:
            Draft: パースされた原稿データ
            
        Raises:
            LoaderError: ファイルが見つからない、またはパース失敗時
        """
        path = Path(file_path)
        
        # ファイル存在確認
        if not path.exists():
            raise LoaderError(f"File not found: {file_path}")
        
        # ファイル読み込み
        try:
            content = path.read_text(encoding='utf-8')
        except Exception as e:
            raise LoaderError(f"Failed to read file: {e}")
        
        # フロントマターと本文を分離
        frontmatter, body = self._parse_frontmatter(content)
        
        # 必須フィールドチェック
        for field in self.REQUIRED_FIELDS:
            if field not in frontmatter or not frontmatter[field]:
                raise LoaderError(f"Missing required field: {field}")
        
        # Draftオブジェクト作成
        draft = Draft(
            title=frontmatter['title'],
            slug=frontmatter['slug'],
            description=frontmatter['description'],
            content=body.strip(),
            category=frontmatter.get('category'),
            tags=frontmatter.get('tags', []),
            status=frontmatter.get('status', 'draft'),
            featured_image=frontmatter.get('featured_image'),
            scheduled_at=frontmatter.get('scheduled_at'),
            source_file=str(path.absolute()),
        )
        
        return draft
    
    def _parse_frontmatter(self, content: str) -> tuple[dict, str]:
        """
        YAMLフロントマターと本文を分離
        
        Args:
            content: ファイル全体の内容
            
        Returns:
            (frontmatter_dict, body_text)
        """
        # フロントマターのパターン: ---\n...\n---
        pattern = r'^---\s*\n(.*?)\n---\s*\n(.*)$'
        match = re.match(pattern, content, re.DOTALL)
        
        if not match:
            raise LoaderError("Invalid frontmatter: Missing YAML header (---)")
        
        yaml_content = match.group(1)
        body = match.group(2)
        
        try:
            frontmatter = yaml.safe_load(yaml_content)
            if frontmatter is None:
                frontmatter = {}
        except yaml.YAMLError as e:
            raise LoaderError(f"Invalid frontmatter: {e}")
        
        return frontmatter, body


if __name__ == "__main__":
    # テスト用
    import sys
    if len(sys.argv) > 1:
        loader = Loader()
        draft = loader.load(sys.argv[1])
        print(f"Title: {draft.title}")
        print(f"Slug: {draft.slug}")
        print(f"Description: {draft.description}")
        print(f"Category: {draft.category}")
        print(f"Content length: {len(draft.content)} chars")
