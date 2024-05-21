from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'main.login'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    migrate.init_app(app, db) 
    login_manager.init_app(app)
    from .models import User
    with app.app_context():
        from . import routes
        app.register_blueprint(routes.main_bp)
        db.create_all()

        def format_date(value, format='%Y-%m-%d'):
            if value is None:
                return ""
            return value.strftime(format)
        app.jinja_env.filters['format_date'] = format_date

        @login_manager.user_loader
        def load_user(user_id):
            return User.query.get(int(user_id))

    return app
