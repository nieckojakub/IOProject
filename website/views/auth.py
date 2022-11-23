from flask import Blueprint, render_template, request, url_for, flash,redirect
from datetime import datetime
# from website.token import generate_confirmation_token, confirm_token
from website.views.forms import RegistrationForm, LoginForm
from website.app import db
from website.models import User
from flask_login import login_user, current_user, logout_user, login_required
from website.app import bcrypt, login_manager


auth = Blueprint('auth', __name__)



@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('views.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('views.home'))
        else:
            flash(f'Login Unsuccessful. Please check email and password', 'danger')
    return render_template("login.html", form=form)


@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('views.home'))


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('views.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(firstName=form.firstName.data, lastName=form.lastName.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        # token = generate_confirmation_token(user.email)
        flash(f'Account created for {form.firstName.data}!  Please chceck your email for verification!','success!')
        return redirect(url_for('auth.login'))
    return render_template('signup.html',form=form)

@auth.route('/account')
@login_required
def account():
    return render_template('account.html')

@auth.route('/confirm/<token>')
#@login_required
def confirm_email(token):
    try:
        #email = confirm_token(token)
        email=''
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