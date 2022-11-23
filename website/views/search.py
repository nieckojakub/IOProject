from flask import Blueprint, request
from flask_login import current_user, login_required
from ..models import History, Product

search = Blueprint('search', __name__)


# search
@search.route('/', methods=['GET'])
def search_get():
    # get params
    products_list = request.args.get('list')
    is_ceneo = request.args.get('ceneo')
    is_allegro = request.args.get('allegro')

    # simple validation
    if products_list is None:
        return '', 400

    if is_ceneo is None:
        is_ceneo = False
    else:
        is_ceneo = True

    if is_allegro is None:
        is_allegro = False
    else:
        is_allegro = True

    if not (is_ceneo or is_allegro):
        return '', 400

    # ceneo results
    if is_ceneo:
        pass

    # allegro results
    if is_allegro:
        pass

    # add to history
    # history = History(user_id=current_user.id, is_allegro=is_allegro, is_ceneo=is_ceneo)

    # return results
    return str(products_list) + ", ceneo: " + str(is_ceneo) + \
           ", allegro: " + str(is_allegro), 200


# search history
# TODO: login_required
@search.route('/history', methods=['GET'])
def history_get():
    return 'History', 200


@search.route('/history/<int:id>', methods=['DELETE'])
def history_delete(id):
    return id, 200
