import pytest
from website.app import create_app
from flask_sqlalchemy import SQLAlchemy

@pytest.fixture(scope="session")
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })

    # other setup can go here

    yield app

    # clean up / reset resources here


@pytest.fixture(scope="session")
def client(app):
    return app.test_client()


@pytest.fixture(scope="session")
def runner(app):
    return app.test_cli_runner()

@pytest.fixture(scope="session")
def _db(app):
    app_ctx = app.app_context()
    app_ctx.push()
    db = SQLAlchemy(app=app)
    return db