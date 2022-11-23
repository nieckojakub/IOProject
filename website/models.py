from .app import db
from datetime import datetime
from flask_login import UserMixin


#@login_manager.user_loader
#def load_user(user_id):
#   return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(30), nullable=False)
    lastName = db.Column(db.String(30), nullable=False)
    imag_file = db.Column(db.String(20), nullable=True, default='default.jpg')
    email = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    registered_on = db.Column(db.DateTime())
    confirmed = db.Column(db.Boolean, nullable=True, default=False)
    confirmed_on = db.Column(db.DateTime())
