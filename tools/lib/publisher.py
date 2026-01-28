"""
Publisher - WordPress投稿モジュール
REST APIを使用してWordPressに投稿
"""
import time
from dataclasses import dataclass
from typing import Optional

import requests


@dataclass
class PostResult:
    """投稿結果"""
    post_id: int
    edit_url: str
    view_url: str
    status: str
    action: str  # "created" or "updated"


class PublisherError(Exception):
    """Publisher関連のエラー"""
    pass


class Publisher:
    """WordPress REST APIで投稿を管理するクラス"""
    
    MAX_RETRIES = 2
    RETRY_DELAY = 2  # seconds
    
    def __init__(
        self,
        site_url: str,
        username: str,
        app_password: str,
        basic_auth: Optional[tuple[str, str]] = None
    ):
        """
        Args:
            site_url: WordPressサイトURL（末尾スラッシュなし）
            username: WordPressユーザー名
            app_password: Application Password
            basic_auth: サーバーBasic認証情報 (user, password) または None
        """
        self.site_url = site_url.rstrip('/')
        
        # セッションを作成
        self.session = requests.Session()
        
        # サーバーBasic認証がある場合、URLに認証情報を埋め込む
        # 例: https://user:pass@example.com/wp-json/wp/v2
        if basic_auth:
            from urllib.parse import urlparse, urlunparse
            parsed = urlparse(self.site_url)
            # 認証情報をURLに埋め込み
            netloc_with_auth = f"{basic_auth[0]}:{basic_auth[1]}@{parsed.netloc}"
            self.site_url = urlunparse((
                parsed.scheme,
                netloc_with_auth,
                parsed.path,
                parsed.params,
                parsed.query,
                parsed.fragment
            ))
        
        self.api_url = f"{self.site_url}/wp-json/wp/v2"
        
        # WordPress Application Password認証
        # URL方式でBasic認証を突破した後、AuthorizationヘッダーでWP認証
        self.session.auth = (username, app_password)
        
        self._basic_auth_enabled = basic_auth is not None
        
        # カテゴリ/タグのキャッシュ
        self._categories_cache = None
        self._tags_cache = None
    
    def _make_request(self, method: str, url: str, **kwargs) -> requests.Response:
        """HTTPリクエストを実行"""
        return getattr(self.session, method)(url, **kwargs)
    
    def test_connection(self) -> bool:
        """
        接続テスト
        
        Returns:
            bool: 接続成功ならTrue
        """
        try:
            response = self._make_request(
                'get',
                f"{self.api_url}/users/me",
                timeout=10
            )
            return response.status_code == 200
        except Exception:
            return False
    
    def find_post_by_slug(self, slug: str) -> Optional[int]:
        """
        slugで既存投稿を検索
        
        Args:
            slug: URLスラッグ
            
        Returns:
            int or None: 見つかった場合はpost_id
        """
        try:
            response = self._make_request(
                'get',
                f"{self.api_url}/posts",
                params={"slug": slug, "status": "any"},
                timeout=10
            )
            
            if response.status_code == 200:
                posts = response.json()
                if posts and len(posts) > 0:
                    return posts[0]['id']
        except Exception:
            pass
        
        return None
    
    def create_post(
        self,
        title: str,
        content: str,
        slug: str,
        status: str = "draft",
        category_id: Optional[int] = None,
        tag_ids: Optional[list[int]] = None,
        meta_description: Optional[str] = None
    ) -> PostResult:
        """
        新規投稿を作成
        
        Args:
            title: 記事タイトル
            content: 記事本文（ブロックHTML）
            slug: URLスラッグ
            status: 投稿ステータス（draft/publish）
            category_id: カテゴリID
            tag_ids: タグIDリスト
            meta_description: メタディスクリプション
            
        Returns:
            PostResult: 投稿結果
        """
        data = {
            "title": title,
            "content": content,
            "slug": slug,
            "status": status,
        }
        
        if category_id:
            data["categories"] = [category_id]
        
        if tag_ids:
            data["tags"] = tag_ids
        
        # メタディスクリプション（Yoast SEO用）
        if meta_description:
            data["meta"] = {
                "_yoast_wpseo_metadesc": meta_description
            }
        
        return self._post_with_retry(data, action="created")
    
    def update_post(
        self,
        post_id: int,
        title: str,
        content: str,
        status: str = "draft",
        meta_description: Optional[str] = None
    ) -> PostResult:
        """
        既存投稿を更新
        
        Args:
            post_id: 投稿ID
            title: 記事タイトル
            content: 記事本文（ブロックHTML）
            status: 投稿ステータス
            meta_description: メタディスクリプション
            
        Returns:
            PostResult: 投稿結果
        """
        data = {
            "title": title,
            "content": content,
            "status": status,
        }
        
        if meta_description:
            data["meta"] = {
                "_yoast_wpseo_metadesc": meta_description
            }
        
        return self._put_with_retry(post_id, data)
    
    def _post_with_retry(self, data: dict, action: str = "created") -> PostResult:
        """リトライ付きPOST"""
        last_error = None
        
        for attempt in range(self.MAX_RETRIES):
            try:
                response = self._make_request(
                    'post',
                    f"{self.api_url}/posts",
                    json=data,
                    timeout=30
                )
                
                if response.status_code == 201:
                    result = response.json()
                    return PostResult(
                        post_id=result['id'],
                        edit_url=f"{self.site_url}/wp-admin/post.php?post={result['id']}&action=edit",
                        view_url=result.get('link', ''),
                        status=result.get('status', 'draft'),
                        action=action
                    )
                elif response.status_code == 401:
                    raise PublisherError("WordPress auth failed: Invalid credentials")
                elif response.status_code == 403:
                    raise PublisherError("WordPress auth failed: Insufficient permissions")
                else:
                    last_error = f"HTTP {response.status_code}: {response.text}"
                    
            except PublisherError:
                raise
            except Exception as e:
                last_error = str(e)
            
            if attempt < self.MAX_RETRIES - 1:
                time.sleep(self.RETRY_DELAY)
        
        raise PublisherError(f"WordPress post failed: {last_error}")
    
    def _put_with_retry(self, post_id: int, data: dict) -> PostResult:
        """リトライ付きPUT"""
        last_error = None
        
        for attempt in range(self.MAX_RETRIES):
            try:
                response = self._make_request(
                    'put',
                    f"{self.api_url}/posts/{post_id}",
                    json=data,
                    timeout=30
                )
                
                if response.status_code == 200:
                    result = response.json()
                    return PostResult(
                        post_id=result['id'],
                        edit_url=f"{self.site_url}/wp-admin/post.php?post={result['id']}&action=edit",
                        view_url=result.get('link', ''),
                        status=result.get('status', 'draft'),
                        action="updated"
                    )
                elif response.status_code == 401:
                    raise PublisherError("WordPress auth failed: Invalid credentials")
                elif response.status_code == 404:
                    raise PublisherError(f"WordPress post not found: {post_id}")
                else:
                    last_error = f"HTTP {response.status_code}: {response.text}"
                    
            except PublisherError:
                raise
            except Exception as e:
                last_error = str(e)
            
            if attempt < self.MAX_RETRIES - 1:
                time.sleep(self.RETRY_DELAY)
        
        raise PublisherError(f"WordPress update failed: {last_error}")
    
    def get_category_id(self, category_name: str) -> Optional[int]:
        """
        カテゴリ名からIDを取得
        
        Args:
            category_name: カテゴリ名
            
        Returns:
            int or None: カテゴリID
        """
        if self._categories_cache is None:
            try:
                response = self._make_request(
                    'get',
                    f"{self.api_url}/categories",
                    params={"per_page": 100},
                    timeout=10
                )
                if response.status_code == 200:
                    self._categories_cache = {
                        cat['name']: cat['id'] 
                        for cat in response.json()
                    }
                else:
                    self._categories_cache = {}
            except Exception:
                self._categories_cache = {}
        
        return self._categories_cache.get(category_name)
    
    def get_tag_ids(self, tag_names: list[str]) -> list[int]:
        """
        タグ名リストからIDリストを取得
        
        Args:
            tag_names: タグ名リスト
            
        Returns:
            list[int]: タグIDリスト
        """
        if self._tags_cache is None:
            try:
                response = self._make_request(
                    'get',
                    f"{self.api_url}/tags",
                    params={"per_page": 100},
                    timeout=10
                )
                if response.status_code == 200:
                    self._tags_cache = {
                        tag['name']: tag['id'] 
                        for tag in response.json()
                    }
                else:
                    self._tags_cache = {}
            except Exception:
                self._tags_cache = {}
        
        return [
            self._tags_cache[name] 
            for name in tag_names 
            if name in self._tags_cache
        ]


if __name__ == "__main__":
    # テスト用
    import os
    
    site_url = os.environ.get("WP_SITE_URL", "https://example.com")
    username = os.environ.get("WP_USERNAME", "admin")
    app_password = os.environ.get("WP_APP_PASSWORD", "")
    
    if app_password:
        publisher = Publisher(site_url, username, app_password)
        if publisher.test_connection():
            print("Connection successful!")
        else:
            print("Connection failed!")
    else:
        print("WP_APP_PASSWORD not set")
