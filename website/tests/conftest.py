import pytest
import sys
import os
import re
from website.search_engine.ceneo import CeneoBrowser


DEFAULT_PRODUCT_LIMIT_OPTION = 10
DEFAULT_PRODUCT_SORT_OPTION = "TRUE"
DEFAULT_ALLEGRO_OPTION = "FALSE"
DEFAULT_FILE_OPTION = "valid_products.txt"
ALLEGRO_TARGET = "ALLEGRO"
CENEO_TARGET = "CENEO"

# Create CeneoBrowser for product_list_fixture()
ceneo_browser = CeneoBrowser()


@pytest.fixture(scope="class")
def product_name_fixture(request):
    """Dummy fixture, which returns product name"""

    return request.param


@pytest.fixture(scope="class")
def product_limit_fixture(request):
    """Dummy fixture, which returns product limit"""

    return request.param


@pytest.fixture(scope="class")
def product_sort_fixture(request):
    """Dummy fixture, which returns product sort"""

    return request.param


@pytest.fixture(scope="class")
def product_target_fixture(request):
    """Dummy fixture, which returns search target"""

    return request.param


@pytest.fixture(scope="class")
def product_list_fixture(pytestconfig, request):
    """Dummy fixture, which returns list of Product objects"""
    target = None

    # Get the --target option
    if pytestconfig.getoption("target") is None:
        pass
    elif pytestconfig.getoption("target").upper() == ALLEGRO_TARGET:
        target = ALLEGRO_TARGET
    elif pytestconfig.getoption("target").upper() == CENEO_TARGET:
        target = CENEO_TARGET

    # Get the --limit option
    try:
        limit = int(pytestconfig.getoption("limit"))
    except ValueError:
        sys.exit("ValueError: invalid literal for --limit")

    # Get the --sort option
    if pytestconfig.getoption("sort").upper() == DEFAULT_PRODUCT_SORT_OPTION:
        sort = True
    else:
        sort = False

    # Search for the product
    return ceneo_browser.search(
        request.param,
        limit=limit,
        sort=sort,
        target=target,
    )


def pytest_addoption(parser):
    """Add command line options for the search() method inside the
    CeneoBrowser object and for the input data file.
    """

    # --file specifies the file with product search queries to test.
    parser.addoption("--file", action="store", default=DEFAULT_FILE_OPTION)

    # search() method's limit param.
    parser.addoption(
        "--limit", action="store", default=DEFAULT_PRODUCT_LIMIT_OPTION
    )

    # search() method's sort param.
    parser.addoption(
        "--sort", action="store", default=DEFAULT_PRODUCT_SORT_OPTION
    )

    # search() method's target param.
    parser.addoption("--target", action="store", default=None)


def get_product_data_tuple():
    """Used to parametrize the TestCeneoSearch object

    return: tuple of the form:
        (
            product search query,
            result of the CeneoBrowser.search(),
            product limit option,
            product sort option,
            product target option
        )
    """

    # Get the command line options.
    arg_line = " ".join(sys.argv).upper()

    # Get the --file option.
    file_option = re.findall("--FILE(?:=|\s)\S+", arg_line)
    if file_option:
        file_name = file_option[-1].split(" ")[-1].split("=")[-1].lower()
    else:
        file_name = DEFAULT_FILE_OPTION

    # Get the product limit option.
    limit_option = re.findall("--LIMIT(?:=|\s)\S+", arg_line)
    if limit_option:
        limit_option_value = limit_option[-1].split(" ")[-1].split("=")[-1]
        try:
            limit = int(limit_option_value)
        except ValueError:
            sys.exit("ValueError: invalid literal for --limit")
    else:
        limit = DEFAULT_PRODUCT_LIMIT_OPTION

    # Get the product sort option.
    sort_option_flag = re.findall("--SORT(?:=|\s)\S+", arg_line)
    if sort_option_flag:
        sort_option_flag_value = (
            sort_option_flag[-1].split(" ")[-1].split("=")[-1]
        )
        sort = True if sort_option_flag_value == "TRUE" else False
    else:
        default_sort_option_bool = (
            True if DEFAULT_PRODUCT_SORT_OPTION == "TRUE" else False
        )
        sort = default_sort_option_bool

    # Get the product target option.
    target_option_flag = re.findall("--TARGET(?:=|\s)\S+", arg_line)
    if target_option_flag:
        target_option_flag_value = (
            target_option_flag[-1].split(" ")[-1].split("=")[-1]
        )
        if target_option_flag_value == ALLEGRO_TARGET:
            target = ALLEGRO_TARGET
        elif target_option_flag_value == CENEO_TARGET:
            target = CENEO_TARGET
        else:
            target = None
    else:
        target = None

    # Open file with the product search query
    script_dir = os.path.dirname(__file__)
    path = os.path.join(script_dir, file_name)
    with open(path, "r") as f:
        product_names = f.read().split("\n")
    product_names_tuples = list()

    # Create the tuples
    for product_name in product_names:
        try:
            if product_name[0] != "#":
                product_names_tuples.append(
                    (product_name, product_name, limit, sort, target)
                )
            else:
                continue
        except:
            continue

    return product_names_tuples
