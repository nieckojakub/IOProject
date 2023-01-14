import pytest, os, re, decimal
from .conftest import get_product_data_tuple, ALLEGRO_TARGET, CENEO_TARGET


@pytest.mark.parametrize(
    "product_name_fixture, "
    + "product_list_fixture,"
    + "product_limit_fixture, "
    + "product_sort_fixture, "
    + "product_target_fixture",
    get_product_data_tuple(),
    indirect=True,
)
class TestCeneoSearch:
    def test_product_name(
        self,
        product_name_fixture,
        product_list_fixture,
        product_limit_fixture,
        product_sort_fixture,
        product_target_fixture,
    ):
        print(product_list_fixture)
        for product in product_list_fixture:
            assert (
                product.name is not None
            ), f'[ "QUERY: "{product_name_fixture}" ]'

    def test_product_url(
        self,
        product_name_fixture,
        product_list_fixture,
        product_limit_fixture,
        product_sort_fixture,
        product_target_fixture,
    ):
        for product in product_list_fixture:
            assert product.url is not None, (
                f'[ "QUERY: "{product_name_fixture}",'
                f' PRODUCT: "{product.name}" ]'
            )
            assert re.match(
                "https://www.ceneo.pl/(Zabawki/)?[0-9]+", product.url
            ), (
                f'[ "QUERY: "{product_name_fixture}",'
                f' PRODUCT: "{product.name}" ]'
            )

    def test_product_rating(
        self,
        product_name_fixture,
        product_list_fixture,
        product_limit_fixture,
        product_sort_fixture,
        product_target_fixture,
    ):
        for product in product_list_fixture:
            if product.rating is None:
                assert True
            else:
                assert product.rating >= 0 and product.rating <= 5, (
                    f'[ "QUERY: "{product_name_fixture}",'
                    f' PRODUCT: "{product.name}" ]'
                )

    def test_product_img_url(
        self,
        product_name_fixture,
        product_list_fixture,
        product_limit_fixture,
        product_sort_fixture,
        product_target_fixture,
    ):
        for product in product_list_fixture:
            assert product.img is not None, (
                f'[ "QUERY: "{product_name_fixture}",'
                f' PRODUCT: "{product.name}" ]'
            )
            assert re.match(
                "https://image.ceneostatic.pl/data/products/[0-9]+/.*",
                product.img,
            ), (
                f'[ "QUERY: "{product_name_fixture}",'
                f' PRODUCT: "{product.name}" ]'
            )

    def test_product_description(
        self,
        product_name_fixture,
        product_list_fixture,
        product_limit_fixture,
        product_sort_fixture,
        product_target_fixture,
    ):
        for product in product_list_fixture:
            assert isinstance(product.description, str), (
                f'[ "QUERY: "{product_name_fixture}",'
                f' PRODUCT: "{product.name}" ]'
            )

    def test_product_shop_list(
        self,
        product_name_fixture,
        product_list_fixture,
        product_limit_fixture,
        product_sort_fixture,
        product_target_fixture,
    ):
        for product in product_list_fixture:
            assert product.shop_list, (
                f'[ "QUERY: "{product_name_fixture}",'
                f' PRODUCT: "{product.name}" ]'
            )

    def test_shop_name(
        self,
        product_name_fixture,
        product_list_fixture,
        product_limit_fixture,
        product_sort_fixture,
        product_target_fixture,
    ):
        for product in product_list_fixture:
            for shop in product.shop_list:
                assert shop.name is not None, (
                    f'[ "QUERY: "{product_name_fixture}",'
                    f' PRODUCT: "{product.name}" ]'
                )

    def test_shop_price(
        self,
        product_name_fixture,
        product_list_fixture,
        product_limit_fixture,
        product_sort_fixture,
        product_target_fixture,
    ):
        for product in product_list_fixture:
            for shop in product.shop_list:
                assert shop.price is not None, (
                    f'[ "QUERY: "{product_name_fixture}",'
                    f' PRODUCT: "{product.name}",'
                    f' SHOP: "{shop.name}" ]'
                )
                assert shop.price > 0, (
                    f'[ "QUERY: "{product_name_fixture}",'
                    f' PRODUCT: "{product.name}",'
                    f' SHOP: "{shop.name}" ]'
                )
                decimal_position = (
                    decimal.Decimal(str(shop.price)).as_tuple().exponent
                )
                assert decimal_position == -1 or decimal_position == -2, (
                    f'[ "QUERY: "{product_name_fixture}",'
                    f' PRODUCT: "{product.name}",'
                    f' SHOP: "{shop.name}" ]'
                )

    def test_shop_url(
        self,
        product_name_fixture,
        product_list_fixture,
        product_limit_fixture,
        product_sort_fixture,
        product_target_fixture,
    ):
        for product in product_list_fixture:
            for shop in product.shop_list:
                assert re.match("https://www.ceneo.pl/.*", shop.url), (
                    f'[ "QUERY: "{product_name_fixture}",'
                    f' PRODUCT: "{product.name}",'
                    f' SHOP: "{shop.name}" ]'
                )

    def test_shop_delivery_price(
        self,
        product_name_fixture,
        product_list_fixture,
        product_limit_fixture,
        product_sort_fixture,
        product_target_fixture,
    ):
        for product in product_list_fixture:
            for shop in product.shop_list:
                assert shop.delivery_price is not None, (
                    f'[ "QUERY: "{product_name_fixture}",'
                    f' PRODUCT: "{product.name}",'
                    f' SHOP: "{shop.name}" ]'
                )

    def test_shop_availability(
        self,
        product_name_fixture,
        product_list_fixture,
        product_limit_fixture,
        product_sort_fixture,
        product_target_fixture,
    ):
        for product in product_list_fixture:
            for shop in product.shop_list:
                assert shop.availability is not None, (
                    f'[ "QUERY: "{product_name_fixture}",'
                    f' PRODUCT: "{product.name}",'
                    f' SHOP: "{shop.name}" ]'
                )

    def test_shop_delivery_time(
        self,
        product_name_fixture,
        product_list_fixture,
        product_limit_fixture,
        product_sort_fixture,
        product_target_fixture,
    ):
        for product in product_list_fixture:
            for shop in product.shop_list:
                assert shop.delivery_time is None, (
                    f'[ "QUERY: "{product_name_fixture}",'
                    f' PRODUCT: "{product.name}",'
                    f' SHOP: "{shop.name}" ]'
                )

    def test_price_sort(
        self,
        product_name_fixture,
        product_list_fixture,
        product_limit_fixture,
        product_sort_fixture,
        product_target_fixture,
    ):
        prev_offer_price = 0
        for product in product_list_fixture:
            next_offer_price = min(shop.price for shop in product.shop_list)
            assert prev_offer_price <= next_offer_price, (
                f'[ "QUERY: "{product_name_fixture}",'
                f' PRODUCT: "{product.name}" ]'
            )
            prev_offer_price = next_offer_price

    def test_allegro_filter(
        self,
        product_name_fixture,
        product_list_fixture,
        product_limit_fixture,
        product_sort_fixture,
        product_target_fixture,
    ):
        print(product_list_fixture)
        target = product_target_fixture
        for product in product_list_fixture:
            for shop in product.shop_list:
                if target == ALLEGRO_TARGET:
                    assert shop.name == "allegro.pl", (
                        f'[ "QUERY: "{product_name_fixture}",'
                        f' PRODUCT: "{product.name}",'
                        f" TARGET: {target} ]"
                    )
                elif target == CENEO_TARGET:
                    assert shop.name != "allegro.pl", (
                        f'[ "QUERY: "{product_name_fixture}",'
                        f' PRODUCT: "{product.name}",'
                        f" TARGET: {target} ]"
                    )
                else:
                    assert True
