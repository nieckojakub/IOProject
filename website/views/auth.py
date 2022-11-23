from flask import Blueprint, render_template, request, url_for, flash,redirect
from datetime import datetime
# from website.token import generate_confirmation_token, confirm_token
from website.views.forms import RegistrationForm, LoginForm, RequestResetForm, ResetPasswordForm
from website.app import db
from website.models import User
from flask_login import login_user, current_user, logout_user, login_required
from website.app import bcrypt, login_manager
from website.email import send_reset_email, send_mail_confirmation

auth = Blueprint('auth', __name__)



@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('views.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            if user.confirmed:
                login_user(user, remember=form.remember.data)
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('views.home'))
            else:
                flash('Check your mail associated with this account to confirm the account.', 'info')
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
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
        send_mail_confirmation(user)
        flash(f'Account created for {form.firstName.data}!  Please chceck your email for verification!','success')
        return redirect(url_for('auth.login'))
    return render_template('signup.html',form=form)

@auth.route('/account')
@login_required
def account():
    return render_template('account.html')

@auth.route('/reset_password', methods=['GET','POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('views.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.','info')
        return redirect(url_for('auth.login'))
    return render_template('reset_request.html', form=form)

@auth.route('/reset_password/<token>', methods=['GET','POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('views.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('auth.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been update! You are now able to log in.','success')
        return redirect(url_for('auth.login'))
    return render_template('reset_token.html', form=form)

@auth.route('/confirm_email/<token>', methods=['GET','POST'])
def confirm_email(token):
    if current_user.is_authenticated:
        return redirect(url_for('views.home'))
    email = User.verify_mail_confirm_token(token)
    if email:
        user = db.session.query(User).filter(User.email == email).one_or_none()
        user.confirmed =True
        user.confirmed_on=datetime.now()
        db.session.add(user)
        db.session.commit()
        flash(f"Your email has been verified and you can now login to your account","success",)
        return redirect(url_for('auth.login'))
    else:
        flash('The confirmation link is invalid or has expired.', 'warning')
        return redirect(url_for('auth.signup'))

