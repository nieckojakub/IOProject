from flask import Blueprint, render_template, request, url_for, flash,redirect
from datetime import datetime
# from website.token import generate_confirmation_token, confirm_token
from website.views.forms import RegistrationForm, LoginForm
from website.app import db
from website.models import User
from flask_login import login_user, current_user, logout_user
from flask_bcrypt import Bcrypt


auth = Blueprint('auth', __name__)
bcrypt = Bcrypt()


@auth.route('/login', methods=['GET', 'POST'])
def login():
    #if current_user.is_authenticated:
    #    return redirect(url_for('views.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            # login_user(user, remember=form.remember.data)
            return redirect(url_for('views.home'))

        else:
            flash(f'Login Unsuccessful. Please check username and password', 'danger')
    return render_template("login.html", form=form)


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
        #hashed_password = 'test'
        user = User(firstName=form.firstName.data, lastName=form.lastName.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        # token = generate_confirmation_token(user.email)
        flash(f'Account created for {form.firstName.data}!','success')
        return redirect(url_for('auth.login'))
    return render_template('signup.html',form=form)


@auth.route('/confirm/<token>')
#@login_required
def confirm_email(token):
    try:
        email = confirm_token(token)
    except:
        flash('The confirmation link is invalid or has expired.', 'danger')
    user = User.query.filter_by(email=email).first_or_404()
    if user.confirmed:
        flash('Account already confirmed. Please login.', 'success')
    else:
        user.confirmed = True
        user.confirmed_on = datetime.now()
        db.session.add(user)
        db.session.commit()
        flash('You have confirmed your account. Thanks!', 'success')
    return redirect(url_for('main.home'))