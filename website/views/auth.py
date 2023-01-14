from flask import Blueprint, render_template, request, url_for, flash,redirect, current_app
from datetime import datetime
# from website.token import generate_confirmation_token, confirm_token
from website.views.forms import RegistrationForm, LoginForm, RequestResetForm, ResetPasswordForm
from website.app import db
from website.models import User
from flask_login import login_user, current_user, logout_user, login_required
from website.app import bcrypt, login_manager
from website.email import send_reset_email, send_mail_confirmation
from .search import history_get, history_delete
from ..models import History, Product as ProductModel, load_user
from sqlalchemy import select, update
import os 

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
        user = User(firstName=form.firstName.data, lastName=form.lastName.data, email=form.email.data, password=hashed_password, registered_on=datetime.now())
        db.session.add(user)
        db.session.commit()
        send_mail_confirmation(user)
        flash(f'Account created for {form.firstName.data}!  Please chceck your email for verification!','success')
        return redirect(url_for('auth.login'))
    return render_template('signup.html',form=form)

@auth.route('/account', methods=('GET', 'POST'))
@login_required
def account():
    # Prepare account data
    user = load_user(current_user.id)
    user.registered_on = user.registered_on.date()
    # Prepare history data
    history_data, _ = history_get()
    history_data = history_data.get_json()
    for product_history in history_data:
        stmt = select(ProductModel).where(ProductModel.history_id == product_history['history_id'])
        products_model = db.session.execute(stmt)
        products = [prod[0] for prod in products_model.fetchall()]
        product_list = list()
        for product_list_item in product_history['products_list']:
            product_name = product_list_item.split(':')[1].strip(' ')
            product_url = '#'
            for product in products:
                if product.name == product_name:
                    product_url = product.url
                    break
            product_list.append(
                {
                    'product_name': product_name,
                    'product_url': product_url,
                }
            )
        product_history['products_list'] = product_list
        product_history['product_url'] = product_url
        product_history['search_date'] = product_history['search_date'].replace(' GMT','')
        product_history['products_list'] = product_list
    search_btn_id = request.args.get('history-btn', None)
    if search_btn_id is not None:
        history_delete(search_btn_id)
        return redirect(url_for('auth.account'))
    if request.method == 'POST':
        image = request.files.get('image', None)
        if image.filename == '':
            flash('No file selected', 'danger')
            return redirect(url_for('auth.account'))
        image_name = str(user.id) + os.path.splitext(image.filename)[1]
        image_path = os.path.join(url_for('static', filename='img'), image_name)
        image_path = os.path.join(current_app.root_path, image_path.strip('/'))
        image.save(image_path)
        stmt = update(User).where(User.id == current_user.id).values(imag_file = image_name)
        db.session.execute(stmt)
        db.session.commit()
        user.image_file = image_name
        return redirect(url_for('auth.account'))
    return render_template('account.html',history_data=history_data, user=user)

@auth.route('/reset_password', methods=['GET','POST'])
def reset_request():
    if current_user.is_authenticated:
        user = User.query.filter_by(id=current_user.id).first()
        send_reset_email(user)
        logout_user()
        flash('An email has been sent with instructions to reset your password.','info')
        return redirect(url_for('auth.login'))
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

