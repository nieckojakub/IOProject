from flask import Blueprint

search = Blueprint('search', __name__)


@search.route('/', methods=['GET'])
def search_get():
    return 'hello search', 200
