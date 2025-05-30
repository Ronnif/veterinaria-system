from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    login_manager.login_view = 'main.index'  # <-- Mejor para blueprint

    with app.app_context():
        from . import routes, models
        app.register_blueprint(routes.bp)
        # db.create_all()  # <-- Elimina si usas Flask-Migrate

    return app