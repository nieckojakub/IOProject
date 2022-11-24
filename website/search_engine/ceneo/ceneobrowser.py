from mechanicalsoup import Browser
from search_engine import Product
import re

class CeneoBrowser(Browser):
    """ Builds a web scraper for the ceneo website.

    :param url: Set the ceneo url with access to the search bar. By default
        "https://www.ceneo.pl" is applied.
    """
    URL="https://www.ceneo.pl"
    FORM_SELECTOR='form[action="/search"]'
    FORM_INPUT_SELECTOR='#form-head-search-q'
    PRODUCT_LIMIT=10

    def __init__(self, url=URL):
        Browser.__init__(self)
        self.url = url
        self.ceneo_page = self.get(url)
        self.ceneo_html = self.ceneo_page.soup
        self.search_form = self.ceneo_html.select(self.FORM_SELECTOR)[0]
        self.search_input = self.search_form.select(self.FORM_INPUT_SELECTOR)[0]

    def _isValidSearch(self, result_url: str):
        if result_url == self.url:
            return False
        else:
            return True

    def search(self, search_query: str, limit=PRODUCT_LIMIT):
        """ Search for the given product.

        :param product_name: User-specified product name
        :param limit: Specifies the maximum size of returned list. By default
            PRODUCT_LIMIT of 10 is used.
        :return: If several products match the search criteria, a list of 
        Product objects (with a maximum length limited by the limit variable) 
        is returned. Otherwise only one Product object is returned.
        """
        # Product class attributes
        product_ = str
        ceneo_result_url = str
        img_src_attribute = str
        product_description = str
        product_rating = float
        shop_list = list()
   
        self.search_input['value'] = search_query
        search_results_page = self.submit(self.search_form, self.url)
        if self._isValidSearch(search_results_page.url):
            print(search_results_page.url)





