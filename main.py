from website import create_app
from website import Bcrypt, LoginManager
app= create_app()

if __name__ == '__main__':
    app.run()

