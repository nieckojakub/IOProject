import pytest, os, re, decimal

script_dir = os.path.dirname(__file__)
path = os.path.join(script_dir,'valid_products.txt') 

from website.search_engine.ceneo import CeneoBrowser
with open(path, 'r') as f:
    product_names = f.read().split('\n')

browser = CeneoBrowser()
products = list()
for product_name in product_names:
    if product_name.strip()[0] == '#':
        continue
    products.append((
                    product_name, 
                    browser.search(product_name)
                    ))
    
class TestCeneoSearch:

    @pytest.mark.parametrize('product_name, product_objects', products)
    def test_product_name(self, product_name, product_objects):
        for product in product_objects: 
            assert product.name is not None, \
                f'[ "Search Query for "{product_name}" gives the Product '\
                'object with no name ]'

    @pytest.mark.parametrize('product_name, product_objects', products)
    def test_product_url(self, product_name, product_objects):
        for product in product_objects: 
            assert product.url is not None, \
                f'[ "Search Query for "{product_name}" gives the Product '\
                f'object of name "{product.name}" with no ceneo offer'\
                ' url ]'
            assert re.match('https://www.ceneo.pl/[0-9]+', product.url),\
                f'[ "Search Query for "{product_name}" gives the Product '\
                f'object of name "{product.name}" with invalid ceneo '\
                'offer url ]'

    @pytest.mark.parametrize('product_name, product_objects', products)
    def test_product_rating(self, product_name, product_objects):
        for product in product_objects: 
            if product.rating is None:
                assert True
            else:
                assert product.rating >=0 and product.rating < 5,\
                    f'[ "Search Query for "{product_name}" gives the Product '\
                    f'object of name "{product.name}" with invalid value '\
                    'for rating ]'

    @pytest.mark.parametrize('product_name, product_objects', products)
    def test_product_img_url(self, product_name, product_objects):
        for product in product_objects: 
            assert product.img is not None,\
                f'[ "Search Query for "{product_name}" gives the Product '\
                f'object of name "{product.name}" with no ceneo img url ]'
            assert re.match(
                        'https://image.ceneostatic.pl/data/products/[0-9]+/.*', 
                        product.img
                        ),\
                f'[ "Search Query for "{product_name}" gives the Product '\
                f'object of name "{product.name}" with invalid ceneo '\
                'img url ]'

    @pytest.mark.parametrize('product_name, product_objects', products)
    def test_product_description(self, product_name, product_objects):
        for product in product_objects: 
            assert isinstance(product.description, str), \
                f'[ "Search Query for "{product_name}" gives the Product '\
                f'object of name "{product.name}" with invalid product '\
                'description ]'

    @pytest.mark.parametrize('product_name, product_objects', products)
    def test_product_shop_list(self, product_name, product_objects):
        for product in product_objects:
            assert product.shop_list, \
                f'[ "Search Query for "{product_name}" gives the Product '\
                f'object of name "{product.name}" with no shop list ]'

    @pytest.mark.parametrize('product_name, product_objects', products)
    def test_shop_names(self, product_name, product_objects):
        for product in product_objects:
            for shop in product.shop_list:
                assert shop.name is not None, \
                    f'[ "Search Query for "{product_name}" gives the Product '\
                    f'object of name "{product.name}" with shop of no name ]'

    @pytest.mark.parametrize('product_name, product_objects', products)
    def test_shop_price(self, product_name, product_objects):
        for product in product_objects:
            for shop in product.shop_list:
                assert shop.price is not None, \
                    f'[ "Search Query for "{product_name}" gives the Product '\
                    f'object of name "{product.name}" with shop offer of'\
                    f' "{shop.name}" with no price ]'
                assert shop.price > 0, \
                    f'[ "Search Query for "{product_name}" gives the Product '\
                    f'object of name "{product.name}" with shop offer of'\
                    f' "{shop.name}" with nonpositive price ]'
                decimal_position = decimal.Decimal(
                                                str(shop.price)
                                                ).as_tuple().exponent
                assert decimal_position == -1 or decimal_position == -2,\
                    f'[ "Search Query for "{product_name}" gives the Product '\
                    f'object of name "{product.name}" with shop offer of'\
                    f' "{shop.name}" with invalid price format ]'

    @pytest.mark.parametrize('product_name, product_objects', products)
    def test_shop_url(self, product_name, product_objects):
        for product in product_objects:
            for shop in product.shop_list:
                assert re.match('https://www.ceneo.pl/.*', shop.url), \
                    f'[ "Search Query for "{product_name}" gives the Product '\
                    f'object of name "{product.name}" with shop offer of'\
                    f' "{shop.name}" with invalid url ]'

    @pytest.mark.parametrize('product_name, product_objects', products)
    def test_shop_delivery_price(self, product_name, product_objects):
        for product in product_objects:
            for shop in product.shop_list:
                assert shop.delivery_price is not None, \
                    f'[ "Search Query for "{product_name}" gives the Product '\
                    f'object of name "{product.name}" with shop offer of'\
                    f' "{shop.name}" with no delivery price ]'

    @pytest.mark.parametrize('product_name, product_objects', products)
    def test_shop_availability(self, product_name, product_objects):
        for product in product_objects:
            for shop in product.shop_list:
                assert shop.availability is not None, \
                    f'[ "Search Query for "{product_name}" gives the Product '\
                    f'object of name "{product.name}" with shop offer of'\
                    f' "{shop.name}" with no availability info ]'

    @pytest.mark.parametrize('product_name, product_objects', products)
    def test_shop_delivery_time(self, product_name, product_objects):
        for product in product_objects:
            for shop in product.shop_list:
                assert shop.delivery_time is not None, \
                    f'[ "Search Query for "{product_name}" gives the Product '\
                    f'object of name "{product.name}" with shop offer of'\
                    f' "{shop.name}" with no delivery time info ]'

    @pytest.mark.parametrize('product_name, product_objects', products)
    def test_price_sort(self, product_name, product_objects):
        prev_offer_price = 0
        for product in product_objects:
            next_offer_price = min(shop.price for shop in product.shop_list)
            assert prev_offer_price <= next_offer_price, \
                f'[ "Search Query for "{product_name}" gives the Product '\
                f'object of name "{product.name}" with not working price '\
                'sorting ]'
            prev_offer_price = next_offer_price