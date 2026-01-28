#!/usr/bin/env python3
"""
記事自動投稿ツール - メインスクリプト
原稿ファイル → AI構造化 → ブロックHTML生成 → WordPress投稿
"""
import argparse
import json
import os
import sys
import yaml
from pathlib import Path

# .envファイルから環境変数を読み込み
from dotenv import load_dotenv
load_dotenv()
from typing import Optional

# ライブラリパスを追加
sys.path.insert(0, str(Path(__file__).parent))

from lib.loader import Loader, LoaderError
from lib.structurer import Structurer, StructurerError
from lib.validator import Validator
from lib.generator import Generator
from lib.publisher import Publisher, PublisherError
from lib.history import HistoryManager


class Config:
    """設定管理クラス"""
    
    def __init__(self, config_path: str = "config.yaml"):
        self.config = self._load_config(config_path)
    
    def _load_config(self, path: str) -> dict:
        """設定ファイル読み込み（環境変数展開対応）"""
        config_file = Path(path)
        if not config_file.exists():
            # デフォルト設定
            return {
                'gemini': {
                    'api_key': os.environ.get('GEMINI_API_KEY', ''),
                    'model': 'gemini-2.0-flash',
                    'temperature': 0.3,
                },
                'wordpress': {
                    'site_url': os.environ.get('WP_SITE_URL', ''),
                    'username': os.environ.get('WP_USERNAME', 'admin'),
                    'app_password': os.environ.get('WP_APP_PASSWORD', ''),
                    'default_category': 'コラム',
                    'default_status': 'draft',
                },
                'output': {
                    'save_json': True,
                    'save_html': True,
                    'json_dir': 'output/json',
                    'html_dir': 'output/html',
                },
                'cta': {
                    'enabled': True,
                    'template_file': 'block-html/posts/cta.txt',
                },
                'prompt': {
                    'template_file': 'docs/prompts/article_structure.md',
                }
            }
        
        with open(config_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 環境変数展開 ${VAR_NAME}
        import re
        def replace_env(match):
            var_name = match.group(1)
            return os.environ.get(var_name, '')
        
        content = re.sub(r'\$\{(\w+)\}', replace_env, content)
        return yaml.safe_load(content)
    
    def get(self, *keys, default=None):
        """ネストした設定値を取得"""
        value = self.config
        for key in keys:
            if isinstance(value, dict):
                value = value.get(key)
            else:
                return default
        return value if value is not None else default


def print_step(step_num: int, total: int, message: str):
    """ステップ表示"""
    print(f"\n[{step_num}/{total}] {message}")


def print_success(message: str):
    """成功表示"""
    print(f"  ✓ {message}")


def print_warning(message: str):
    """警告表示"""
    print(f"  ⚠ {message}")


def print_error(message: str):
    """エラー表示"""
    print(f"  ✗ {message}")


def main():
    parser = argparse.ArgumentParser(
        description='記事自動投稿ツール - 原稿からWordPress投稿まで自動化'
    )
    parser.add_argument(
        'files',
        nargs='*',
        help='原稿ファイル（複数指定可）'
    )
    parser.add_argument(
        '--config', '-c',
        default='config.yaml',
        help='設定ファイルパス'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='投稿せずにプレビューのみ'
    )
    parser.add_argument(
        '--publish',
        action='store_true',
        help='下書きではなく即公開'
    )
    parser.add_argument(
        '--confirm',
        action='store_true',
        help='JSON生成後に確認'
    )
    parser.add_argument(
        '--force-update',
        action='store_true',
        help='既存投稿を確認なしで更新'
    )
    parser.add_argument(
        '--force-new',
        action='store_true',
        help='既存投稿を無視して新規作成'
    )
    parser.add_argument(
        '--no-cta',
        action='store_true',
        help='CTAを追加しない'
    )
    parser.add_argument(
        '--skip-validation',
        action='store_true',
        help='バリデーションをスキップ'
    )
    parser.add_argument(
        '--test-connection',
        action='store_true',
        help='API接続テスト'
    )
    
    args = parser.parse_args()
    
    # 設定読み込み
    config = Config(args.config)
    
    # 接続テストモード
    if args.test_connection:
        return run_connection_test(config)
    
    # ファイル指定なし
    if not args.files:
        parser.print_help()
        return 1
    
    # 複数ファイル処理
    success_count = 0
    fail_count = 0
    
    for file_path in args.files:
        try:
            result = process_file(file_path, config, args)
            if result:
                success_count += 1
            else:
                fail_count += 1
        except KeyboardInterrupt:
            print("\n\n中断されました")
            return 130
        except Exception as e:
            print_error(f"予期しないエラー: {e}")
            fail_count += 1
    
    # 結果サマリ
    if len(args.files) > 1:
        print("\n" + "=" * 50)
        print(f"完了: {success_count}件成功, {fail_count}件失敗")
    
    return 0 if fail_count == 0 else 1


def run_connection_test(config: Config) -> int:
    """API接続テスト"""
    print("=" * 50)
    print("API接続テスト")
    print("=" * 50)
    
    # Gemini API
    print("\n[Gemini API]")
    api_key = config.get('gemini', 'api_key')
    if api_key:
        try:
            from lib.structurer import Structurer
            structurer = Structurer(api_key)
            print_success("APIキー設定済み")
            print_success("接続OK（実際の呼び出しはスキップ）")
        except Exception as e:
            print_error(f"初期化失敗: {e}")
    else:
        print_error("APIキーが設定されていません")
    
    # WordPress API
    print("\n[WordPress API]")
    site_url = config.get('wordpress', 'site_url')
    username = config.get('wordpress', 'username')
    app_password = config.get('wordpress', 'app_password')
    
    # Basic認証設定
    basic_auth = None
    if config.get('wordpress', 'basic_auth', 'enabled'):
        ba_user = config.get('wordpress', 'basic_auth', 'username')
        ba_pass = config.get('wordpress', 'basic_auth', 'password')
        if ba_user and ba_pass:
            basic_auth = (ba_user, ba_pass)
            print_success("Basic認証: 有効")
    
    if site_url and app_password:
        try:
            publisher = Publisher(site_url, username, app_password, basic_auth=basic_auth)
            if publisher.test_connection():
                print_success(f"サイトURL: {site_url}")
                print_success(f"ユーザー: {username}")
                print_success("接続OK")
            else:
                print_error("接続失敗（認証情報を確認してください）")
        except Exception as e:
            print_error(f"接続失敗: {e}")
    else:
        print_error("WordPress設定が不完全です")
    
    print("\n" + "=" * 50)
    return 0


def process_file(file_path: str, config: Config, args) -> bool:
    """1ファイルを処理"""
    print("\n" + "=" * 50)
    print("記事自動投稿ツール")
    print("=" * 50)
    
    total_steps = 5 if not args.dry_run else 4
    
    # Step 1: 原稿読込
    print_step(1, total_steps, "原稿読込中...")
    try:
        loader = Loader()
        draft = loader.load(file_path)
        print_success(f"タイトル: {draft.title}")
        print_success(f"スラッグ: {draft.slug}")
    except LoaderError as e:
        print_error(str(e))
        return False
    
    # Step 2: AI構造化
    print_step(2, total_steps, "AI構造化中...")
    try:
        api_key = config.get('gemini', 'api_key')
        if not api_key:
            print_error("GEMINI_API_KEYが設定されていません")
            return False
        
        prompt_path = config.get('prompt', 'template_file')
        structurer = Structurer(
            api_key=api_key,
            model=config.get('gemini', 'model'),
            temperature=config.get('gemini', 'temperature', default=0.3),
            prompt_template_path=prompt_path
        )
        
        import time
        start = time.time()
        article_json = structurer.structure(draft.content, draft.title)
        elapsed = time.time() - start
        
        print_success(f"Gemini API: 成功（{elapsed:.1f}秒）")
        
        # JSON保存
        if config.get('output', 'save_json'):
            json_dir = Path(config.get('output', 'json_dir', default='output/json'))
            json_dir.mkdir(parents=True, exist_ok=True)
            json_path = json_dir / f"{draft.slug}.json"
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(article_json.raw_json, f, ensure_ascii=False, indent=2)
            print_success(f"JSON保存: {json_path}")
        
    except StructurerError as e:
        print_error(str(e))
        return False
    
    # バリデーション
    if not args.skip_validation:
        validator = Validator()
        validation_result = validator.validate(article_json.raw_json)
        print("\n" + validation_result.format_report())
        
        if not validation_result.is_valid:
            print_error("バリデーションエラー: 続行できません")
            return False
    
    # 確認モード
    if args.confirm:
        print("\nJSON構造化が完了しました。続行しますか？ [y/n]: ", end="")
        response = input().strip().lower()
        if response != 'y':
            print("中止しました")
            return False
    
    # Step 3: HTML生成
    print_step(3, total_steps, "HTML生成中...")
    
    cta_path = config.get('cta', 'template_file') if config.get('cta', 'enabled') else None
    generator = Generator(cta_template_path=cta_path)
    
    html_content = generator.generate(
        article_json.raw_json,
        include_cta=not args.no_cta and config.get('cta', 'enabled', default=True)
    )
    
    # ブロック数カウント
    block_count = html_content.count('<!-- wp:')
    print_success(f"ブロック数: {block_count}")
    
    # HTML保存
    if config.get('output', 'save_html'):
        html_dir = Path(config.get('output', 'html_dir', default='output/html'))
        html_dir.mkdir(parents=True, exist_ok=True)
        html_path = html_dir / f"{draft.slug}.txt"
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print_success(f"HTML保存: {html_path}")
    
    # ドライランなら終了
    if args.dry_run:
        print("\n" + "=" * 50)
        print("ドライラン完了（投稿はスキップ）")
        print("=" * 50)
        return True
    
    # Step 4: WordPress投稿
    print_step(4, total_steps, "WordPress投稿中...")
    
    site_url = config.get('wordpress', 'site_url')
    username = config.get('wordpress', 'username')
    app_password = config.get('wordpress', 'app_password')
    
    # Basic認証設定
    basic_auth = None
    if config.get('wordpress', 'basic_auth', 'enabled'):
        ba_user = config.get('wordpress', 'basic_auth', 'username')
        ba_pass = config.get('wordpress', 'basic_auth', 'password')
        if ba_user and ba_pass:
            basic_auth = (ba_user, ba_pass)
    
    if not site_url or not app_password:
        print_error("WordPress設定が不完全です")
        return False
    
    try:
        publisher = Publisher(site_url, username, app_password, basic_auth=basic_auth)
        history = HistoryManager()
        
        # 既存投稿チェック
        existing_post_id = None
        if not args.force_new:
            existing_post_id = history.find_by_slug(draft.slug)
            if not existing_post_id:
                existing_post_id = publisher.find_post_by_slug(draft.slug)
        
        # 投稿ステータス
        status = 'publish' if args.publish else config.get('wordpress', 'default_status', default='draft')
        
        if existing_post_id and not args.force_new:
            # 更新モード
            if not args.force_update:
                print(f"\n  既存投稿が見つかりました（ID: {existing_post_id}）")
                print("  更新しますか？ [y/n]: ", end="")
                response = input().strip().lower()
                if response != 'y':
                    print("中止しました")
                    return False
            
            result = publisher.update_post(
                post_id=existing_post_id,
                title=draft.title,
                content=html_content,
                status=status,
                meta_description=draft.description
            )
            history.save_updated(draft.slug, draft.title)
        else:
            # 新規作成
            category_id = None
            if draft.category:
                category_id = publisher.get_category_id(draft.category)
            elif config.get('wordpress', 'default_category'):
                category_id = publisher.get_category_id(
                    config.get('wordpress', 'default_category')
                )
            
            tag_ids = []
            if draft.tags:
                tag_ids = publisher.get_tag_ids(draft.tags)
            
            result = publisher.create_post(
                title=draft.title,
                content=html_content,
                slug=draft.slug,
                status=status,
                category_id=category_id,
                tag_ids=tag_ids,
                meta_description=draft.description
            )
            history.save_created(
                slug=draft.slug,
                post_id=result.post_id,
                title=draft.title,
                source_file=file_path
            )
        
        print_success(f"投稿ID: {result.post_id}")
        print_success(f"アクション: {result.action}")
        print_success(f"ステータス: {result.status}")
        
    except PublisherError as e:
        print_error(str(e))
        return False
    
    # 完了
    print("\n" + "=" * 50)
    print("完了！")
    print(f"編集URL: {result.edit_url}")
    print("=" * 50)
    
    return True


if __name__ == "__main__":
    sys.exit(main())
