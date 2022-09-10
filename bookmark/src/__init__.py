from flask import Flask
import os

from src.database import db
from src.auth import auth
from src.bookmarks import bookmarks


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        app.config.from_mapping(
            SECRET_KEY=os.environ.get('SECRET_KEY'),
            SQLALCHEMY_DATABASE_URI=os.environ.get('SQLALCHEMY_DATABASE_URI'),
            SQLALCHEMY_TRACK_MODIFICATIONS=os.environ.get(
                'SQLALCHEMY_TRACK_MODIFICATIONS')
        )
    else:
        app.config.from_mapping(test_config)

    db.app = app
    db.init_app(app)

    app.register_blueprint(auth)
    app.register_blueprint(bookmarks)

    @app.get('/')
    def index():
        return 'Homepage'

    return app