from flask import Blueprint, render_template, request, url_for, flash,redirect
from website.views.forms import RegistrationForm, LoginForm
from website import bcrypt, db
from website.models import User
from flask_login import login_user, current_user, logout_user


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    #if current_user.is_authenticated:
    #    return redirect(url_for('views.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user,remember=form.remember.data)
            return redirect(url_for('views.home'))

        else:
            flash(f'Login Unsuccessful. Please check username and password', 'danger')
    return render_template("login.html",form=form )


@auth.route('/logout')
def logout():
    #logout_user()
    return redirect(url_for('views.home'))


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
   # if current_user.is_authenticated:
    #    return redirect(url_for('views.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(firstName=form.firstName.data, lastName=form.lastName.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.firstName.data}!','success')
        return redirect(url_for('auth.login'))
    return render_template('signup.html',form=form)
