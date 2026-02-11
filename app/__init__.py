import logging

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    """Flask アプリケーションファクトリ。"""
    app = Flask(
        __name__,
        template_folder="../templates",
        static_folder="../static",
    )

    # 設定の読み込み
    app.config.from_object("app.config.Config")

    # ロギング設定
    logging.basicConfig(
        level=logging.DEBUG if app.debug else logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )

    # 拡張機能の初期化
    db.init_app(app)
    migrate.init_app(app, db)

    # モデルのインポート（マイグレーション用）
    from app import models  # noqa: F401

    # Blueprint の登録
    from app.routes import register_blueprints

    register_blueprints(app)

    return app
