from flask import Flask
from flask_session import Session
from flask_migrate import Migrate
from flask_mail import Mail
from config import Config
from app.user.models import db
import logging
import os

mail = Mail()

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)
    
    if test_config:
        app.config.from_mapping(test_config)

    initialize_extensions(app)
    register_blueprints(app)
    setup_logging(app)

    with app.app_context():
        db.create_all()

    app_title = os.getenv('APP_TITLE')
    @app.context_processor
    def inject_app_title():
        return dict(app_title=app_title)

    return app

def initialize_extensions(app):
    db.init_app(app)
    Migrate(app, db)
    Session(app)
    mail.init_app(app)

def register_blueprints(app):
    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.user import bp as user_bp
    app.register_blueprint(user_bp)

def setup_logging(app):
    if not app.debug:
        # Set up logging to file
        logging.basicConfig(filename='app.log', level=logging.INFO,
                            format='%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')

        # Set up logging to console
        console = logging.StreamHandler()
        console.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
        console.setFormatter(formatter)
        logging.getLogger('').addHandler(console)
    else:
        logging.basicConfig(level=logging.DEBUG)
