from flask import Blueprint, request, make_response
import json
from flask_login import current_user, login_required
from ..models import History, Product
from ..search_engine.product import Product
from ..search_engine.shop import Shop
from ..search_engine.json_encoder import CustomEncoder

search = Blueprint('search', __name__)


# search
@search.route('/', methods=['GET'])
def search_get():
    # get params
    products_list = list()
    for i in range(10):
        product = request.args.get('list' + str(i))
        if product is not None:
            products_list.append(product)
    is_ceneo = request.args.get('ceneo')
    is_allegro = request.args.get('allegro')

    # simple validation
    if len(products_list) == 0:
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
    ceneo_results = list()
    if is_ceneo:
        for product in products_list:
            ceneo_search_result = []    # TODO: search
            # for testing
            ceneo_search_result = [Product(product, "url", "img",
                                           [Shop('test1', 'url', 150, 20, 0, 10),
                                            Shop('test2', 'url', 150, 20, 0, 10)],
                                           "desc", 4.5)]
            ceneo_results.append(ceneo_search_result)

    # allegro results
    allegro_results = list()
    if is_allegro:
        for product in products_list:
            allegro_search_result = []  # TODO: search
            # for testing
            allegro_search_result = [Product(product, "url", "img",
                                             [Shop('test1', 'url', 150, 20, 0, 10),
                                              Shop('test2', 'url', 150, 20, 0, 10)],
                                             "desc", 4.5)]
            allegro_results.append(allegro_search_result)

    results = {"ceneo": ceneo_results, "allegro": allegro_results}

    # return results
    return make_response(json.dumps(results, indent=4, cls=CustomEncoder), 200)


# search history
# TODO: login_required
@search.route('/history', methods=['GET'])
def history_get():
    return 'History', 200


@search.route('/history/<int:id>', methods=['DELETE'])
def history_delete(id):
    return id, 200
