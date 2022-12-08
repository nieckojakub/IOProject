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
from ..search_engine.ceneo import CeneoBrowser

search = Blueprint('search', __name__)

search_results = dict()


# search
@search.route('/search/add/<token>', methods=['GET'])
def search_add_get(token=None):
    # get params
    product = request.args.get('product')
    target = request.args.get('target')     # ceneo or allegro

    # simple validation
    if product is None:
        return '', 400

    if token is None:
        return '', 400

    if target == "ceneo":
        ceneo_browser = CeneoBrowser()
        ceneo_search_result = ceneo_browser.search(product)
        if token not in search_results:
            search_results[token] = {"ceneo": list(), "allegro": list()}
        search_results[token]['ceneo'].append(ceneo_search_result)
    elif target == "allegro":
        return '', 400
    else:
        return '', 400


@search.route('/search/<token>', methods=['GET'])
def search_get(token=None):
    if token is None:
        return '', 400

    if token in search_results:
        # get result from results dict
        results = search_results[token]
        del search_results[token]

        # jsonify
        json_result = json.dumps(results, indent=4, cls=CustomEncoder, ensure_ascii=False)
        # return results
        return make_response(json_result, 200)
    else:
        return '', 404


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
