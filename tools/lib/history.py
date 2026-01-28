"""
History - 投稿履歴管理モジュール
slug → post_id のマッピングを管理
"""
import yaml
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional


@dataclass
class PostHistory:
    """投稿履歴エントリ"""
    post_id: int
    title: str
    created_at: str
    updated_at: Optional[str]
    versions: int
    source_file: str


class HistoryManager:
    """投稿履歴を管理するクラス"""
    
    def __init__(self, history_file: str = "output/post_history.yaml"):
        """
        Args:
            history_file: 履歴ファイルパス
        """
        self.history_file = Path(history_file)
        self.history = self._load()
    
    def _load(self) -> dict:
        """履歴ファイルを読み込む"""
        if self.history_file.exists():
            try:
                content = self.history_file.read_text(encoding='utf-8')
                return yaml.safe_load(content) or {}
            except Exception:
                return {}
        return {}
    
    def _save(self):
        """履歴ファイルを保存"""
        try:
            self.history_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.history_file, 'w', encoding='utf-8') as f:
                yaml.dump(
                    self.history, 
                    f, 
                    allow_unicode=True, 
                    default_flow_style=False,
                    sort_keys=False
                )
        except Exception as e:
            # 履歴保存失敗は警告のみ
            print(f"Warning: Failed to save history: {e}")
    
    def find_by_slug(self, slug: str) -> Optional[int]:
        """
        slugからpost_idを検索
        
        Args:
            slug: URLスラッグ
            
        Returns:
            int or None: 見つかった場合はpost_id
        """
        entry = self.history.get(slug)
        if entry and isinstance(entry, dict):
            return entry.get('post_id')
        return None
    
    def get_entry(self, slug: str) -> Optional[PostHistory]:
        """
        slugから履歴エントリを取得
        
        Args:
            slug: URLスラッグ
            
        Returns:
            PostHistory or None: 履歴エントリ
        """
        entry = self.history.get(slug)
        if entry and isinstance(entry, dict):
            return PostHistory(
                post_id=entry.get('post_id', 0),
                title=entry.get('title', ''),
                created_at=entry.get('created_at', ''),
                updated_at=entry.get('updated_at'),
                versions=entry.get('versions', 1),
                source_file=entry.get('source_file', '')
            )
        return None
    
    def save_created(
        self,
        slug: str,
        post_id: int,
        title: str,
        source_file: str
    ):
        """
        新規作成の履歴を保存
        
        Args:
            slug: URLスラッグ
            post_id: 投稿ID
            title: 記事タイトル
            source_file: 原稿ファイルパス
        """
        now = datetime.now().isoformat()
        
        self.history[slug] = {
            'post_id': post_id,
            'title': title,
            'created_at': now,
            'updated_at': None,
            'versions': 1,
            'source_file': source_file
        }
        
        self._save()
    
    def save_updated(self, slug: str, title: str = None):
        """
        更新の履歴を保存
        
        Args:
            slug: URLスラッグ
            title: 新しいタイトル（変更がある場合）
        """
        if slug not in self.history:
            return
        
        now = datetime.now().isoformat()
        
        self.history[slug]['updated_at'] = now
        self.history[slug]['versions'] = self.history[slug].get('versions', 1) + 1
        
        if title:
            self.history[slug]['title'] = title
        
        self._save()
    
    def list_all(self) -> list[tuple[str, PostHistory]]:
        """
        全履歴を取得
        
        Returns:
            list of (slug, PostHistory) tuples
        """
        result = []
        for slug, entry in self.history.items():
            if isinstance(entry, dict):
                result.append((slug, PostHistory(
                    post_id=entry.get('post_id', 0),
                    title=entry.get('title', ''),
                    created_at=entry.get('created_at', ''),
                    updated_at=entry.get('updated_at'),
                    versions=entry.get('versions', 1),
                    source_file=entry.get('source_file', '')
                )))
        return result


if __name__ == "__main__":
    # テスト用
    manager = HistoryManager("output/test_history.yaml")
    
    # 新規作成
    manager.save_created(
        slug="test-article",
        post_id=123,
        title="テスト記事",
        source_file="drafts/test.md"
    )
    
    # 検索
    post_id = manager.find_by_slug("test-article")
    print(f"Found post_id: {post_id}")
    
    # 更新
    manager.save_updated("test-article")
    
    # エントリ取得
    entry = manager.get_entry("test-article")
    print(f"Entry: {entry}")
