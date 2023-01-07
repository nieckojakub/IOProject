import pytest, os, re, decimal
from .conftest import get_product_names_tuple


@pytest.mark.parametrize(
    'product_name_fixture, product_list_fixture',
    get_product_names_tuple(),
    indirect=True,
)
class TestCeneoSearch:

    def test_product_name(self, product_name_fixture, product_list_fixture):
        for product in product_list_fixture: 
            assert product.name is not None, \
                f'[ "Search Query for "{product_name_fixture}" gives the Product '\
                'object with no name ]'

    def test_product_url(self, product_name_fixture, product_list_fixture):
        for product in product_list_fixture: 
            assert product.url is not None, \
                f'[ "Search Query for "{product_name_fixture}" gives the Product '\
                f'object of name "{product.name}" with no ceneo offer'\
                ' url ]'
            assert re.match('https://www.ceneo.pl/[0-9]+', product.url),\
                f'[ "Search Query for "{product_name_fixture}" gives the Product '\
                f'object of name "{product.name}" with invalid ceneo '\
                'offer url ]'

    def test_product_rating(self, product_name_fixture, product_list_fixture):
        for product in product_list_fixture: 
            if product.rating is None:
                assert True
            else:
                assert product.rating >=0 and product.rating <= 5,\
                    f'[ "Search Query for "{product_name_fixture}" gives the Product '\
                    f'object of name "{product.name}" with invalid value '\
                    'for rating ]'

    def test_product_img_url(self, product_name_fixture, product_list_fixture):
        for product in product_list_fixture: 
            assert product.img is not None,\
                f'[ "Search Query for "{product_name_fixture}" gives the Product '\
                f'object of name "{product.name}" with no ceneo img url ]'
            assert re.match(
                        'https://image.ceneostatic.pl/data/products/[0-9]+/.*', 
                        product.img
                        ),\
                f'[ "Search Query for "{product_name_fixture}" gives the Product '\
                f'object of name "{product.name}" with invalid ceneo '\
                'img url ]'

    def test_product_description(self, product_name_fixture, product_list_fixture):
        for product in product_list_fixture: 
            assert isinstance(product.description, str), \
                f'[ "Search Query for "{product_name_fixture}" gives the Product '\
                f'object of name "{product.name}" with invalid product '\
                'description ]'

    def test_product_shop_list(self, product_name_fixture, product_list_fixture):
        for product in product_list_fixture:
            assert product.shop_list, \
                f'[ "Search Query for "{product_name_fixture}" gives the Product '\
                f'object of name "{product.name}" with no shop list ]'

    def test_shop_names(self, product_name_fixture, product_list_fixture):
        for product in product_list_fixture:
            for shop in product.shop_list:
                assert shop.name is not None, \
                    f'[ "Search Query for "{product_name_fixture}" gives the Product '\
                    f'object of name "{product.name}" with shop of no name ]'

    def test_shop_price(self, product_name_fixture, product_list_fixture):
        for product in product_list_fixture:
            for shop in product.shop_list:
                assert shop.price is not None, \
                    f'[ "Search Query for "{product_name_fixture}" gives the Product '\
                    f'object of name "{product.name}" with shop offer of'\
                    f' "{shop.name}" with no price ]'
                assert shop.price > 0, \
                    f'[ "Search Query for "{product_name_fixture}" gives the Product '\
                    f'object of name "{product.name}" with shop offer of'\
                    f' "{shop.name}" with nonpositive price ]'
                decimal_position = decimal.Decimal(
                                                str(shop.price)
                                                ).as_tuple().exponent
                assert decimal_position == -1 or decimal_position == -2,\
                    f'[ "Search Query for "{product_name_fixture}" gives the Product '\
                    f'object of name "{product.name}" with shop offer of'\
                    f' "{shop.name}" with invalid price format ]'

    def test_shop_url(self, product_name_fixture, product_list_fixture):
        for product in product_list_fixture:
            for shop in product.shop_list:
                assert re.match('https://www.ceneo.pl/.*', shop.url), \
                    f'[ "Search Query for "{product_name_fixture}" gives the Product '\
                    f'object of name "{product.name}" with shop offer of'\
                    f' "{shop.name}" with invalid url ]'

    def test_shop_delivery_price(self, product_name_fixture, product_list_fixture):
        for product in product_list_fixture:
            for shop in product.shop_list:
                assert shop.delivery_price is not None, \
                    f'[ "Search Query for "{product_name_fixture}" gives the Product '\
                    f'object of name "{product.name}" with shop offer of'\
                    f' "{shop.name}" with no delivery price ]'

    def test_shop_availability(self, product_name_fixture, product_list_fixture):
        for product in product_list_fixture:
            for shop in product.shop_list:
                assert shop.availability is not None, \
                    f'[ "Search Query for "{product_name_fixture}" gives the Product '\
                    f'object of name "{product.name}" with shop offer of'\
                    f' "{shop.name}" with no availability info ]'

    def test_shop_delivery_time(self, product_name_fixture, product_list_fixture):
        for product in product_list_fixture:
            for shop in product.shop_list:
                assert shop.delivery_time is not None, \
                    f'[ "Search Query for "{product_name_fixture}" gives the Product '\
                    f'object of name "{product.name}" with shop offer of'\
                    f' "{shop.name}" with no delivery time info ]'

    def test_price_sort(self, product_name_fixture, product_list_fixture):
        prev_offer_price = 0
        for product in product_list_fixture:
            next_offer_price = min(shop.price for shop in product.shop_list)
            assert prev_offer_price <= next_offer_price, \
                f'[ "Search Query for "{product_name_fixture}" gives the Product '\
                f'object of name "{product.name}" with not working price '\
                'sorting ]'
            prev_offer_price = next_offer_price