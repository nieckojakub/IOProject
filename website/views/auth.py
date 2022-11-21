from flask import Blueprint, render_template, request, url_for, flash,redirect
from website.views.forms import RegistrationForm, LoginForm

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    return render_template("login.html",form=form )


@auth.route('/logout')
def logout():
    return render_template("logout.html")


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.firstName.data}!','success')
        return redirect(url_for('views.home'))
    return render_template('signup.html',form=form)
