from flask import Blueprint, request

search = Blueprint('search', __name__)


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

    # return results
    return str(products_list) + ", ceneo: " + str(is_ceneo) + \
           ", allegro: " + str(is_allegro), 200
