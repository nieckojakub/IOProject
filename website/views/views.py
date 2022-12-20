from flask import Blueprint, render_template

views = Blueprint('views', __name__)


@views.route('/')
def home():
    return render_template('home.html')


@views.route("/results/<token>")
def results(token):
    return render_template('results.html')

