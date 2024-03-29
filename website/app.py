from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from os import path
import os
from flask_login import LoginManager
from flask_bcrypt import Bcrypt



db = SQLAlchemy()
DB_NAME = 'site.db'


app = Flask(__name__)
login_manager = LoginManager(app)
bcrypt = Bcrypt(app)
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'


def create_app():
    bootstrap = Bootstrap(app)
    """ Configuration for Development, Testing, Production.  """
    app.config.from_object('config.DevelopmentConfig')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # init database
    db.init_app(app)

    # 404 error handler
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    # register blueprints
    from website.views.views import views
    from website.views.auth import auth
    from website.views.search import search

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(search, url_prefix="/")

    create_database(app)

    return app



def create_database(app):
    if not path.exists('website/' + DB_NAME):
        with app.app_context():
            db.create_all()
        print('Created Database!')
