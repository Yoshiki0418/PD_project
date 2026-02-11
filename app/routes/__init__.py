from app.routes.main import main_bp
from app.routes.recipes import recipes_bp


def register_blueprints(app):
    from .foods import foods_bp
    """全 Blueprint をアプリに登録する。"""
    app.register_blueprint(main_bp)
    app.register_blueprint(recipes_bp)
    app.register_blueprint(foods_bp)
