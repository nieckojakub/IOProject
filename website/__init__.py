from flask import Flask
from flask_bootstrap import Bootstrap

def create_app():
    app = Flask(__name__)
    bootstrap = Bootstrap(app)
    """ Configuration for Development, Testing, Production.  """
    app.config.from_object('config.DevelopmentConfig')

    from website.views.views import views
    from website.views.auth import auth
    from website.views.search import search

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(search, url_prefix="/search")

    return app

