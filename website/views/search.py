from flask import Blueprint, request, make_response
import json
from flask_login import current_user, login_required
from ..models import History, Product
from ..search_engine.product import Product
from ..search_engine.shop import Shop
from ..search_engine.json_encoder import CustomEncoder
from flask_wtf import FlaskForm
from ..models import History, Shop as ShopModel, Product as ProductModel
from ..app import db

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
@search.route('/history/<int:history_id>', methods=['GET'])
@login_required
def history_get(history_id):
    history = History.query.get_or_404(history_id)
    if history.user_id == current_user.id:
        pass
    else:
        return '', 403
    return 'History', 200


@search.route('/history', methods=['POST'])
@login_required
def history_post():
    products_list = request.get_json()
    history = History(user_id=current_user.id)
    db.session.add(history)
    for productJSON in products_list:
        print(productJSON)
        product_object = Product(**productJSON)
        product = ProductModel(history_id=history.id, name=product_object.name, url=product_object.url,
                               img=product_object.img, description=product_object.description,
                               rating=product_object.rating)
        db.session.add(product)
        for shopJSON in product_object.shop_list:
            shop_object = Shop(**shopJSON)
            shop = ShopModel(product_id=product.id, name=shop_object.name, url=shop_object.url,
                             price=shop_object.price, delivery_price=shop_object.delivery_price,
                             availability=shop_object.availability, delivery_time=shop_object.delivery_time)
            db.session.add(shop)
    db.session.commit()
    return '', 200


@search.route('/history/<int:id>', methods=['DELETE'])
@login_required
def history_delete(id):
    return id, 200
