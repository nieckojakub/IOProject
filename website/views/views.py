from flask import Blueprint, render_template

views = Blueprint('views', __name__)


@views.route('/')
def home():
    return render_template('home.html')


@views.route("/results/<token>")
def results(token):
    return render_template('results.html')

##### testing purposes ####
@views.route("/results")
def results_no_token():
    return render_template('results.html')
