from mechanicalsoup import Browser
from ..product import Product
from ..shop import Shop
from . import scrap_offer
from . import scrap_allegro_offer
from . import scrap_product
from typing import List, Optional
import re


class CeneoBrowser(Browser):
    """Builds a web scraper for the ceneo website.

    :param url: Set the ceneo url with access to the search bar. By default
        "https://www.ceneo.pl" is applied.
    """

    URL = "https://www.ceneo.pl"
    FORM_SELECTOR = 'form[action="/search"]'
    FORM_INPUT_SELECTOR = "#form-head-search-q"
    PRODUCT_LIMIT = 10

    def __init__(self, url: str = URL) -> None:
        Browser.__init__(self)
        self.url = url
        self.ceneo_page = self.get(url)
        self.ceneo_html = self.ceneo_page.soup
        self.search_form = self.ceneo_html.select(self.FORM_SELECTOR)[0]
        self.search_input = self.search_form.select(self.FORM_INPUT_SELECTOR)[0]

    def scrapProductInfo(
        self, product_main_page_url: str, is_allegro_specific: bool = False
    ) -> Product:
        """Extract information about the product.

        This method is used by the search() method.

        :param product_main_page_url: Link to ceneo page with product offer.
        :return: Product object is returned.
        """
        ALLEGRO_SHIPPING_SUFFIX = "#shipping-info"
        SHOP_OFFER_SELECTOR = ".product-offers__list__item"

        # Prepare html
        product_main_page = self.get(product_main_page_url)
        product_main_html = product_main_page.soup
        
        # Shop objects
        shop_list = list()

        shop_offers_html = product_main_html.select(SHOP_OFFER_SELECTOR)
        # if not product_rating and shop_offers_html:
        #     # There is no Product rating in the ceneo product overview.
        #     # Try to extract rating from the first shop offer.
        #     product_rating = scrap_product.scrapProductRating(
        #         shop_offers_html[0], is_shop_offer=True
        #     )

        for shop_offer_html in shop_offers_html:
            # Shop name
            shop_name = scrap_offer.scrapOfferShopName(shop_offer_html)
            # Shop url
            shop_url = scrap_offer.scrapOfferShopUrl(shop_offer_html, self.URL)
            # Product price
            product_price = scrap_offer.scrapOfferPrice(shop_offer_html)
            # Product availability
            product_availability = scrap_offer.scrapOfferAvailability(
                shop_offer_html
            )
            if is_allegro_specific and shop_name == 'allegro.pl':
                # Prepare html
                product_allegro_page = self.get(shop_url + ALLEGRO_SHIPPING_SUFFIX)
                product_allegro_html = product_allegro_page.soup
                # Allegro delivery price
                delivery_price = scrap_allegro_offer.scrapOfferDeliveryPrice(
                    product_allegro_html
                )
                # Allegro product delivery time
                delivery_time = scrap_allegro_offer.scrapOfferDeliveryTime(product_allegro_html)
                # Create Shop object and append it to the list
            elif shop_name == 'allegro.pl':
                continue
            else:
                # Delivery price
                delivery_price = scrap_offer.scrapOfferDeliveryPrice(
                    shop_offer_html, product_price
                )
                # Product delivery time
                delivery_time = scrap_offer.scrapOfferDeliveryTime(shop_offer_html)
                # Create Shop object and append it to the list

            shop_list.append(
                Shop(
                    shop_name,
                    shop_url,
                    product_price,
                    delivery_price,
                    product_availability,
                    delivery_time,
                )
            )
        if len(shop_list) == 0:
            return None
        # Product name
        product_name = scrap_product.scrapProductName(product_main_html)

        # Product image url
        product_img_url = scrap_product.scrapProductImageUrl(product_main_html)

        # Product rating
        product_rating = scrap_product.scrapProductRating(product_main_html)

        # Product description
        product_description = scrap_product.scrapProductDescription(
            product_main_html
        )



        # Return product object
        return Product(
            product_name,
            product_main_page_url,
            product_img_url,
            shop_list,
            product_description,
            product_rating,
        )

    def search(
        self,
        search_query: str,
        limit: int = PRODUCT_LIMIT,
        sort: bool = True,
        is_allegro_specific: bool = False,
    ) -> List[Product]:
        """Search for the given product.

        :param product_name: User-specified product name
        :param limit: Specifies the maximum size of returned list. By default
            PRODUCT_LIMIT of 10 is used.
        :return: If several products match the search criteria, a list of
        Product objects (with a maximum length limited by the limit variable)
        is returned. Otherwise only one Product object is returned.
        """
        # Sort by price url prefix
        SORT_SUFFIX = ";0112-0.htm"
        # Row layout
        PRODUCT_LIST_LAYOUT_SELECTOR = ".cat-prod-row"
        # Grid layout
        PRODUCT_GRID_LAYOUT_SELECTOR = ".grid-row"
        # Another Grid layout
        PRODUCT_GRID_LAYOUT_SELECTOR_2 = ".cat-prod-box__body"
        # Product main page
        PRODUCT_MAIN_LAYOUT_SELECTOR = ".product-top__wrapper"

        # Fill in the search form with the given search query
        self.search_input["value"] = search_query
        # Submit the form and access the result page
        search_results_page = self.submit(self.search_form, self.url)
        # Check if the url has changed
        # - if not, something is wrong with the form

        if search_results_page.url == self.url:
            # Throwing an error expected here
            return []
        # Sort products
        if sort:
            sorted_results_page_url = search_results_page.url + SORT_SUFFIX
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
            PRODUCT_MAIN_LAYOUT_SELECTOR
        )
        if product_main_container:
            # We got the main layout
            return [self.scrapProductInfo(search_results_page.url)]

        # Check if the list layout selector appears on the results page
        product_list_containers = search_result_html.select(
            PRODUCT_LIST_LAYOUT_SELECTOR
        )
        # Check if the grid layout selector appears on the results page
        product_grid_containers = search_result_html.select(
            PRODUCT_GRID_LAYOUT_SELECTOR
        )
        # Check if the another grid layout selector appears on the results page
        product_grid_2_containers = search_result_html.select(
            PRODUCT_GRID_LAYOUT_SELECTOR_2
        )
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
            return []

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
        # for i in range(0, limit):
        for product_container in product_containers:
            # Prepare the regex to match the product main page link
            product_link_regex = re.compile("/[0-9]+")
            # Get every <a> tag associated with the product container
            a_tags = product_container.find_all("a")
            # Iterate over <a> tags and find the one that matches the regex
            for a_tag in a_tags:
                regex_result = product_link_regex.match(a_tag["href"])
                if regex_result is not None:
                    # Create the full product main page url
                    product_main_page_url = self.URL + a_tag["href"]
                    product_obj = self.scrapProductInfo(product_main_page_url, is_allegro_specific)
                    if product_obj is None:
                        # Product with no shop list
                        limit -= 1
                    else:
                        product_list.append(
                            self.scrapProductInfo(
                                product_main_page_url, is_allegro_specific
                            )
                        )
                        break
            if len(product_list) == limit:
                break

        return product_list
