from mechanicalsoup import Browser
from ..product import Product
from ..shop import Shop
from . import scrap_offer
from . import scrap_product
import re


class CeneoBrowser(Browser):
    """Builds a web scraper for the ceneo website.

    :param url: Set the ceneo url with access to the search bar. By default
        "https://www.ceneo.pl" is applied.
    """

    URL = "https://www.ceneo.pl"
    FORM_SELECTOR = 'form[action="/search"]'
    FORM_INPUT_SELECTOR = '#form-head-search-q'
    PRODUCT_LIMIT = 10
    
    def __init__(self, url=URL):
        Browser.__init__(self)
        self.url = url
        self.ceneo_page = self.get(url)
        self.ceneo_html = self.ceneo_page.soup
        self.search_form = self.ceneo_html.select(self.FORM_SELECTOR)[0]
        self.search_input = self.search_form.select(self.FORM_INPUT_SELECTOR)[0]

    def scrapProductInfo(self, product_main_page_url):
        """Extract information about the product.

        This method is used by the search() method.

        :param product_main_page_url: Link to ceneo page with product offer.
        :return: Product object is returned.
        """

        PRODUCT_OFFER_SELECTOR = '.product-offers__list__item'

        # Prepare html
        product_main_page = self.get(product_main_page_url)
        product_main_html = product_main_page.soup

        # Product name
        product_name = scrap_product.scrapProductName(product_main_html)
        
        # Product image url
        product_img_url = scrap_product.scrapProductImageUrl(product_main_html)
        
        # Product rating
        product_rating = scrap_product.scrapProductRating(product_main_html)

        # Product description
        product_description = scrap_product.scrapProductDescription(product_main_html)
        
        # Shop objects
        shop_list = list()

        product_offers = product_main_html.select(PRODUCT_OFFER_SELECTOR)
        if not product_rating and product_offers:
            # There is no Product rating in the ceneo product overview.
            # Try to extract rating from the first product offer.
            product_rating = scrap_product.scrapProductRating(
                                                    product_offers[0], 
                                                    is_offer=True
                                                    )
        for product_offer in product_offers:
            # Shop name
            shop_name = scrap_offer.scrapOfferShopName(product_offer)
            # Shop url
            shop_url = scrap_offer.scrapOfferShopUrl(product_offer, self.URL)
            # Product price
            product_price = scrap_offer.scrapOfferPrice(product_offer)
            # Delivery price
            delivery_price = scrap_offer.scrapOfferDeliveryPrice(
                                                        product_offer, 
                                                        product_price
                                                        )
            # Product availability
            product_availability = scrap_offer.scrapOfferAvailability(
                                                            product_offer
                                                            )
            # Product delivery time
            delivery_time = scrap_offer.scrapOfferDeliveryTime(
                                                            product_offer
                                                            )
            # Create Shop object and append it to the list
            shop_list.append(
                Shop(
                    shop_name,
                    shop_url,
                    product_price,
                    delivery_price,
                    product_availability,
                    delivery_time
                )
            )
        # Return product object
        return Product(
            product_name,
            self.URL,
            product_img_url,
            shop_list,
            product_description,
            product_rating,
        )

    def search(self, search_query: str, limit=PRODUCT_LIMIT, sort=True):
        """Search for the given product.

        :param product_name: User-specified product name
        :param limit: Specifies the maximum size of returned list. By default
            PRODUCT_LIMIT of 10 is used.
        :return: If several products match the search criteria, a list of
        Product objects (with a maximum length limited by the limit variable)
        is returned. Otherwise only one Product object is returned.
        """
        # Sort by price url prefix
        SORT_PREFIX = ';0112-0.htm'
        # Row layout
        PRODUCT_LIST_LAYOUT_SELECTOR = '.cat-prod-row'
        # Grid layout
        PRODUCT_GRID_LAYOUT_SELECTOR = '.grid-row'
        # Another Grid layout
        PRODUCT_GRID_LAYOUT_SELECTOR_2 = '.cat-prod-box__body'
        # Product main page
        PRODUCT_MAIN_LAYOUT_SELECTOR = '.product-top__wrapper'

        # Fill in the search form with the given search query
        self.search_input["value"] = search_query
        # Submit the form and access the result page
        search_results_page = self.submit(self.search_form, self.url)
        # Check if the url has changed 
        # - if not, something is wrong with the form
        
        if search_results_page.url == self.url:
            # Throwing an error expected here
            return
        # Sort products
        if sort:
            sorted_results_page_url = search_results_page.url + SORT_PREFIX
            search_results_page = self.get(sorted_results_page_url)
        # Retrive html code
        search_result_html = search_results_page.soup
        
        # Now we need to check what kind of results page we got
        # There are three types of results page layout:
        # 1 The list-like layout - every item has its own row
        # 2 The grid-like layout - every item has its own row and column
        # 3 The main layout - The query was specific and the
        #   results page is actually product main page
        
        # Check if the main layout selector appears on the results page
        product_main_container = search_result_html.select(
            PRODUCT_MAIN_LAYOUT_SELECTOR)
        if product_main_container:
            # We got the main layout
            return [ self.scrapProductInfo(search_results_page.url) ]

        # Check if the list layout selector appears on the results page
        product_list_containers = search_result_html.select(
            PRODUCT_LIST_LAYOUT_SELECTOR)
        # Check if the grid layout selector appears on the results page
        product_grid_containers = search_result_html.select(
            PRODUCT_GRID_LAYOUT_SELECTOR)
        # Check if the another grid layout selector appears on the results page
        product_grid_2_containers = search_result_html.select(
            PRODUCT_GRID_LAYOUT_SELECTOR_2)
        if product_list_containers:
            # We got the list-like layout
            product_containers = product_list_containers
        elif product_grid_containers:
            # We got the grid-like layout
            product_containers = product_grid_containers
        elif product_grid_2_containers:
            # We got the another grid-like layout
            product_containers = product_grid_2_containers
        else:
            # Error ??
            return

        # Count the products
        product_count = len(product_containers)
        # Adjust the limit if we got less products than the LIMIT variable
        limit = product_count if product_count < limit else limit

        # List of products to return
        product_list = list()
        
        # Iterate over the product containers and scrap url to the main page
        # of each product. Then invoke scrapProductInfo() method with each url  
        # to create Product object. When its done simply return the list of 
        # Product objects.
        for i in range(0,limit):
            # Prepare the regex to match the product main page link
            product_link_regex = re.compile("/[0-9]+")
            # Get every <a> tag associated with the product container
            a_tags = product_containers[i].find_all("a")
            # Iterate over <a> tags and find the one that matches the regex
            for a_tag in a_tags:
                regex_result = product_link_regex.match(a_tag["href"])
                if regex_result is not None:
                    # Create the full product main page url
                    product_main_page_url = self.URL + a_tag["href"]
                    product_list.append(self.scrapProductInfo(product_main_page_url))
                    break
    
        return product_list

