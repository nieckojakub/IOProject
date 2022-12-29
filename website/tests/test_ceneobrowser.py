import pytest, os, re

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
            assert isinstance(product.rating, float), \
                f'[ "Search Query for "{product_name}" gives the Product '\
                    f'object of name "{product.name}" with no rating ]'
            assert product.rating >=0 and product.rating < 5, \
                f'[ "Search Query for "{product_name}" gives the Product '\
                    f'object of name "{product.name}" with invalid value '\
                    'for rating ]'

    @pytest.mark.parametrize('product_name, product_objects', products)
    def test_shop_list(self, product_name, product_objects):
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
