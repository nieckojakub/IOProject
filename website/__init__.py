from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = 'site.db'
bcrypt = Bcrypt()


def create_app():
    app = Flask(__name__)
    bootstrap = Bootstrap(app)
    """ Configuration for Development, Testing, Production.  """
    app.config.from_object('config.DevelopmentConfig')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

    bcrypt = Bcrypt(app)

    db.init_app(app)

    from website.views.views import views
    from website.views.auth import auth
    from website.views.search import search

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(search, url_prefix="/search")

    from .models import User

    create_database(app)

    return app


def create_database(app):
    if not path.exists('website/' + DB_NAME):
        with app.app_context():
            db.create_all()
        print('Created Database!')