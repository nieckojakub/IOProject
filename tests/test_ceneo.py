import pytest
import os
script_dir = os.path.dirname(__file__)
path = os.path.join(script_dir,'valid_products.txt') 

from website.search_engine.ceneo import CeneoBrowser
with open(path, 'r') as f:
    product_names = f.read().split('\n')
browser = CeneoBrowser()
products = list()
for product_name in product_names:
    products.append((
                    product_name, 
                    browser.search(product_name)
                    ))

class TestCenoSearch:

    @pytest.mark.parametrize('product_name, product_objects', products)
    def test_name(self, product_name, product_objects):
        for product in product_objects: 
            assert product.name is not None

    @pytest.mark.parametrize('product_name, product_objects', products)
    def test_price(self, product_name, product_objects):
        for product in product_objects: 
            assert isinstance(product.rating, float)