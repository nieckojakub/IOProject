from .app import db, login_manager, app
from datetime import datetime
from flask_login import UserMixin
from itsdangerous import URLSafeTimedSerializer as Serializer
import config


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(30), nullable=False)
    lastName = db.Column(db.String(30), nullable=False)
    imag_file = db.Column(db.String(20), nullable=True, default='default.jpg')
    email = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    registered_on = db.Column(db.DateTime())
    confirmed = db.Column(db.Boolean, nullable=True, default=False)
    confirmed_on = db.Column(db.DateTime())

    def get_reset_token(self):
        secret_key = config.Config.SECRET_KEY
        s = Serializer(secret_key)
        return s.dumps({'user_id': self.id})

    @staticmethod
    def verify_reset_token(token):
        secret_key = config.Config.SECRET_KEY
        s = Serializer(secret_key)
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def get_mail_confirm_token(self):
        secret_key = config.Config.SECRET_KEY
        s = Serializer(secret_key)
        return s.dumps(self.email)
        # return s.dumps({'user_id': self.id})

    @staticmethod
    def verify_mail_confirm_token(token):
        secret_key = config.Config.SECRET_KEY
        try:
            s = Serializer(secret_key)
            email = s.loads(token, max_age=3600)
            return email
        except:
            return None


class History(db.Model):
    __tablename__ = 'history'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False)
    search_date = db.Column(db.DateTime(), default=datetime.utcnow)


class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)
    history_id = db.Column(db.Integer(), db.ForeignKey('history.id'), nullable=False)
    inaccurate_name = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    url = db.Column(db.String, nullable=False)
    img = db.Column(db.String, nullable=True)
    description = db.Column(db.String, nullable=True)
    rating = db.Column(db.Float, nullable=True)
    amount = db.Column(db.Integer, default=1)


class Shop(db.Model):
    __tablename__ = 'shop'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer(), db.ForeignKey('product.id'), nullable=False)
    name = db.Column(db.String, nullable=False)
    url = db.Column(db.String, nullable=False)
    price = db.Column(db.Float, nullable=False)
    delivery_price = db.Column(db.Float, nullable=True)
    availability = db.Column(db.Integer, nullable=True)
    delivery_time = db.Column(db.Float, nullable=True)
