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
        return s.dumps({'user_id':self.id})

    @staticmethod
    def verify_reset_token(token):
        secret_key = config.Config.SECRET_KEY
        s = Serializer(secret_key)
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

class History(db.Model):
    __tablename__ = 'history'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False)
    search_date = db.Column(db.DateTime(), default=datetime.utcnow)
    is_allegro = db.Column(db.Boolean, nullable=False, default=False)
    is_ceneo = db.Column(db.Boolean, nullable=False, default=False)
    product1_id = db.Column(db.Integer(), db.ForeignKey('product.id'), nullable=False)
    product2_id = db.Column(db.Integer(), db.ForeignKey('product.id'), nullable=True)
    product3_id = db.Column(db.Integer(), db.ForeignKey('product.id'), nullable=True)
    product4_id = db.Column(db.Integer(), db.ForeignKey('product.id'), nullable=True)
    product5_id = db.Column(db.Integer(), db.ForeignKey('product.id'), nullable=True)
    product6_id = db.Column(db.Integer(), db.ForeignKey('product.id'), nullable=True)
    product7_id = db.Column(db.Integer(), db.ForeignKey('product.id'), nullable=True)
    product8_id = db.Column(db.Integer(), db.ForeignKey('product.id'), nullable=True)
    product9_id = db.Column(db.Integer(), db.ForeignKey('product.id'), nullable=True)
    product10_id = db.Column(db.Integer(), db.ForeignKey('product.id'), nullable=True)


class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)
