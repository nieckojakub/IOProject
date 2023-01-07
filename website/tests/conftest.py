import pytest
import sys 
import os
from website.search_engine.ceneo import CeneoBrowser


DEFAULT_PRODUCT_LIMIT_OPTION = 10
DEFAULT_PRODUCT_SORT_OPTION = 'TRUE'
DEFAULT_ALLEGRO_OPTION = 'FALSE'
DEFAULT_FILE_OPTION = "valid_products.txt"


ceneo_browser = CeneoBrowser()
@pytest.fixture(scope="class")
def product_name_fixture(request):
    return request.param


@pytest.fixture(scope="class")
def product_list_fixture(pytestconfig, request):
    if pytestconfig.getoption('allegro').upper() == DEFAULT_ALLEGRO_OPTION:
        is_allegro_specific = True
    else:
        is_allegro_specific = False

    try:
        limit = pytestconfig.getoption('limit')
    except ValueError:
        sys.exit('ValueError: invalid literal for --limit')

    if pytestconfig.getoption('sort').upper() == DEFAULT_PRODUCT_SORT_OPTION:
        sort = True
    else:
        sort = False
    return ceneo_browser.search(request.param)

def pytest_addoption(parser):
    parser.addoption("--file", action="store", default=DEFAULT_FILE_OPTION)
    parser.addoption("--limit", action="store", default=DEFAULT_PRODUCT_LIMIT_OPTION)
    parser.addoption("--sort", action="store", default=DEFAULT_PRODUCT_SORT_OPTION)
    parser.addoption("--allegro", action="store", default=DEFAULT_ALLEGRO_OPTION)

def get_product_names_tuple():
    script_dir = os.path.dirname(__file__)
    path = os.path.join(script_dir, DEFAULT_FILE_OPTION) 
    with open(path, 'r') as f:
        product_names = f.read().split('\n')
    product_names_tuples = list() 
    for product_name in product_names:
        try:
            if product_name[0] != '#':
                product_names_tuples.append((product_name, product_name))
            else:
                continue
        except:
            continue
    return product_names_tuples