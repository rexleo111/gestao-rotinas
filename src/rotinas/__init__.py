from flask import Flask, render_template
from .config import Config
from .extensions import db, migrate


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    from .blueprints.usuarios import bp as usuarios_bp
    from .blueprints.rotinas_bp import bp as rotinas_bp
    from .blueprints.execucoes import bp as execucoes_bp
    from .blueprints.logs import bp as logs_bp
    from .blueprints.pages import bp as pages_bp

    app.register_blueprint(pages_bp)
    app.register_blueprint(usuarios_bp, url_prefix="/usuarios")
    app.register_blueprint(rotinas_bp, url_prefix="/rotinas")
    app.register_blueprint(execucoes_bp, url_prefix="/execucoes")
    app.register_blueprint(logs_bp, url_prefix="/logs")

    @app.errorhandler(404)
    def not_found(e):
        return render_template("errors/404.html"), 404

    return app
