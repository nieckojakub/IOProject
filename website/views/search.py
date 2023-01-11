import json
import datetime
from flask import Blueprint, request, make_response, jsonify
from flask_login import current_user, login_required
from flask_wtf import FlaskForm
from sqlalchemy import select, delete
from ..models import History, Product
from ..search_engine.product import Product
from ..search_engine.shop import Shop
from ..search_engine.json_encoder import CustomEncoder
from ..models import History, Shop as ShopModel, Product as ProductModel
from ..app import db
from ..search_engine.ceneo import CeneoBrowser

search = Blueprint('search', __name__)

search_results = dict()

# messages and HTTP status codes
SUCCESS = '', 200

TOKEN_IS_NONE = "Token is none", 400
LIST_LENGTH_ERROR = 'List length error', 400
PRODUCT_IS_NONE = "Product is none", 400
ALLEGRO_NOT_SUPPORTED = "Allegro not supported", 400
INVALID_TARGET = "Invalid target", 400

UNAUTHORIZED = "You're not logged in", 401

FORBIDDEN = "You do not have access to this resource", 403

TOKEN_NOT_FOUND = "Token not found", 404
PRODUCT_NOT_FOUND = "Product not found", 404

TOKEN_TAKEN = "This token has already been taken", 409


# delete token from search results
def delete_token(token):
    if token in search_results:
        del search_results[token]
        return True
    else:
        return False


# delete unused tokens
def delete_unused_tokens():
    for token in search_results.keys():
        if datetime.datetime.now() - search_results[token]['creation_date'] > datetime.timedelta(hours=1):
            delete_token(token)


# add token to search results
@search.route('/search/token/<token>', methods=['GET'])
def search_token_get(token=None):
    # validation
    if token is None:
        return TOKEN_IS_NONE

    length = request.args.get('length')  # number of products to search
    if length is None:
        return LIST_LENGTH_ERROR

    if token not in search_results:
        search_results[token] = {
            "ceneo": dict(),
            "amount": dict(),
            "length": length,
            "counter": 0,
            "blocked": False,
            "creation_date": datetime.datetime.now()
        }
        return SUCCESS
    else:
        return TOKEN_TAKEN


# add product to search results
@search.route('/search/add/<token>', methods=['GET'])
def search_add_get(token=None):
    # get params
    product = request.args.get('product')
    target = request.args.get('target')     # ceneo or allegro
    amount = request.args.get('amount')     # default = 1

    # simple validation
    if product is None:
        return PRODUCT_IS_NONE

    if token is None:
        return TOKEN_IS_NONE

    if amount is None:
        amount = 1

    if target == "both":
        target = None
    elif target != "allegro" and target != "ceneo":
        return INVALID_TARGET

    # get results
    ceneo_browser = CeneoBrowser()
    ceneo_search_result = ceneo_browser.search(product, target=target)
    if token in search_results:
        if search_results[token]['blocked'] is False:
            search_results[token]['ceneo'][product] = ceneo_search_result
            search_results[token]['amount'][product] = amount
        search_results[token]['counter'] += 1
        if search_results[token]['blocked'] is True:
            if int(search_results[token]['counter']) == int(search_results[token]['length']):
                delete_token(token)
    return SUCCESS


# DELETE search results with given token
@search.route("/search/<token>", methods=['DELETE'])
def search_delete(token=None):
    delete_unused_tokens()
    if delete_token(token):
        return SUCCESS
    else:
        return TOKEN_NOT_FOUND


# GET search results with given token and delete
@search.route('/search/<token>', methods=['GET'])
def search_get(token=None):
    if token is None:
        return TOKEN_IS_NONE

    if token in search_results:
        # get result from results dict
        results = search_results[token]
        if int(results['counter']) == int(results['length']):
            delete_token(token)
        else:
            search_results[token]['blocked'] = True

        results = {'ceneo': results['ceneo'], 'amount': results['amount']}

        # jsonify
        json_result = json.dumps(results, indent=4, cls=CustomEncoder, ensure_ascii=False)
        # return results
        return make_response(json_result, 200)
    else:
        return TOKEN_NOT_FOUND


# POST (add) history to database
@search.route('/history', methods=['POST'])
def history_post():
    # check if user is logged in
    if not current_user.is_authenticated:
        return UNAUTHORIZED

    # add to history
    products_dict = request.form['products']
    products_dict = json.loads(products_dict)
    history = History(user_id=current_user.id)
    db.session.add(history)
    db.session.commit()
    for key in products_dict.keys():
        product_json = products_dict[key]
        amount = product_json['amount']
        del product_json['amount']
        product_object = Product(**product_json)
        product = ProductModel(history_id=history.id, inaccurate_name=key, name=product_object.name, url=product_object.url,
                               img=product_object.img, description=product_object.description,
                               rating=product_object.rating, amount=amount)
        db.session.add(product)
        db.session.commit()
        for shopJSON in product_object.shop_list:
            shop_object = Shop(**shopJSON)
            shop = ShopModel(product_id=product.id, name=shop_object.name, url=shop_object.url,
                             price=shop_object.price, delivery_price=shop_object.delivery_price,
                             availability=shop_object.availability, delivery_time=shop_object.delivery_time)
            db.session.add(shop)
        db.session.commit()
    return SUCCESS


# TODO: not tested, might not work
# GET all history entries from logged user
@search.route('/history', methods=['GET'])
def history_get():
    # check if user is logged in
    if not current_user.is_authenticated:
        return UNAUTHORIZED

    # logged user id
    user_id = current_user.get_id()

    # search every history entry from logged user
    stmt = select(History).where(History.user_id == user_id)
    history_entries = db.session.execute(stmt)

    result = list()

    # loop for every history entry
    for entry in history_entries:
        entry = entry[0]
        products_list = list()

        # get all products from history entries
        stmt = select(ProductModel).where(ProductModel.history_id == entry.id)
        products = db.session.execute(stmt)

        for product in products:
            product = product[0]
            products_list.append(product.name)

        # add result
        result.append({
            "history_id": entry.id,
            "search_date": entry.search_date,
            "products_list": products_list
        })

    # return
    return jsonify(result), 200


# GET history and connected products with given history ID
@search.route('/history/<int:history_id>', methods=['GET'])
# @login_required
def history_get_id(history_id):
    # get history entry
    history = History.query.get_or_404(history_id)

    # search list ini
    results = {"ceneo": dict(), "amount": dict()}

    # get all products and shops
    stmt = select(ProductModel).where(ProductModel.history_id == history.id)
    products_models = db.session.execute(stmt)

    for product_model in products_models:
        product_model = product_model[0]
        product_object = Product(product_model.name, product_model.url, product_model.img,
                                 list(), product_model.description, product_model.rating)
        stmt = select(ShopModel).where(ShopModel.product_id == product_model.id)
        shops_models = db.session.execute(stmt)
        for shop_model in shops_models:
            shop_model = shop_model[0]
            shop_object = Shop(shop_model.name, shop_model.url, shop_model.price,
                               shop_model.delivery_price, shop_model.availability,
                               shop_model.delivery_time)
            product_object.shop_list.append(shop_object)
        results['ceneo'][product_model.inaccurate_name] = [product_object]
        results['amount'][product_model.inaccurate_name] = product_model.amount
    # jsonify
    json_result = json.dumps(results, indent=4, cls=CustomEncoder, ensure_ascii=False)
    return json_result, 200


# DELETE history and connected products with given history ID
@search.route('/history/<int:history_id>', methods=['DELETE'])
@login_required
def history_delete(history_id):
    # get history entry
    history = History.query.get_or_404(history_id)

    # check if logged user is history entry owner
    if history.user_id != current_user.id:
        return FORBIDDEN

    # get all products to delete shops connected with history entry
    stmt = select(ProductModel).where(ProductModel.history_id == history.id)
    products_models = db.session.execute(stmt)

    for product_model in products_models:
        product_model = product_model[0]

        stmt = delete(ShopModel).where(ShopModel.product_id == product_model.id)
        db.session.execute(stmt)

    # delete all products connected with history entry
    stmt = delete(ProductModel).where(ProductModel.history_id == history.id)
    db.session.execute(stmt)

    # delete history entry
    stmt = delete(History).where(History.id == history_id)
    db.session.execute(stmt)

    db.session.commit()

    return SUCCESS
