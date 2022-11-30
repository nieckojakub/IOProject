from mechanicalsoup import Browser
from ..product import Product
from ..shop import Shop
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
    PRODUCT_OFFER_SELECTOR = '.product-offers__list__item'

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
        # Prepare html
        product_main_page = self.get(product_main_page_url)
        product_main_html = product_main_page.soup
        product_offers = product_main_html.select(self.PRODUCT_OFFER_SELECTOR)
        # Product name
        product_name_h1 = product_main_html.select(".product-top__product-info__name")[
            0
        ]
        product_name = product_name_h1.string
        # Product image url
        product_img_div = product_main_html.select(
            'div[class="gallery-carousel__item"]'
        )[0]
        product_img = product_img_div.select(
            'img[class="js_gallery-media gallery-carousel__media"]'
        )[0]
        product_img = "https:" + product_img["src"]
        # # Product rating
        # product_rating_span = product_main_html.select(
        #     'span[class="product-review__score"]'
        # )[0]
        # product_rating = round(float(product_rating_span["content"]), 2)
        product_rating = None
        # Product description
        product_description_div = product_main_html.select(
            'div[class="product-top__product-info__tags"]'
        )[0]
        product_description = product_description_div.string
        # Shop objects
        shop_list = list()
        for product_offer in product_offers:
            # Shop name
            shop_opinon_li = product_offer.select('li[class="offer-shop-opinions"]')[0]
            shop_opinion = shop_opinon_li.select("a")[0]
            shop_name = shop_opinion.string.split("Dane i opinie o ")[-1].strip("\n")
            # Shop url
            shop_logo_div = product_offer.select('div[class="product-offer__store"]')[0]
            shop_logo_link = shop_logo_div.select("a")[0]
            shop_url = self.URL + shop_logo_link["href"]
            # Product price
            price_span = product_offer.select('span[class="price"]')[0]
            price_value = price_span.select('span[class="value"]')[0].string.replace(' ', '')
            price_penny = price_span.select('span[class="penny"]')[0].string.replace(' ', '')
            product_price = float(price_value) + float(price_penny.strip(",")) / 100
            # Delivery price
            delivery_price_div = product_offer.select(
                'div[class="product-offer__product__delivery-section"]'
            )[0]
            delivery_price_span = delivery_price_div.select("span")[0]
            # Check if delivery is free
            delivery_price_text = delivery_price_span.string
            if delivery_price_text:
                delivery_price = re.findall("[0-9]+,[0-9]{1,2}", delivery_price_text)
                # Check whether the price pattern has been found
                # if not, it is the allegro offer
                if delivery_price:
                    delivery_price = (
                        float(delivery_price[0].split(",")[0])
                        + float(delivery_price[0].split(",")[1]) / 100
                    )
                    delivery_price = round(delivery_price - product_price, 2)
                else:
                    # Allegro offer - price not displayed
                    delivery_price = None
            else:
                delivery_price = 0
            # Product availability
            product_availability_div = product_offer.select(
                'div[class="product-availability"]'
            )[0]
            product_availability_text = product_availability_div.select("span")[
                0
            ].string
            product_availability = re.findall("[0-9]+", product_availability_text)
            if not product_availability:
                product_availability = 0
            else:
                product_availability = int(product_availability[0])
            # Product delivery time
            delivery_time = None
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
        # Return product object
        return Product(
            product_name,
            self.URL,
            product_img,
            shop_list,
            product_description,
            product_rating,
        )

    def search(self, search_query: str, limit=PRODUCT_LIMIT):
        """Search for the given product.

        :param product_name: User-specified product name
        :param limit: Specifies the maximum size of returned list. By default
            PRODUCT_LIMIT of 10 is used.
        :return: If several products match the search criteria, a list of
        Product objects (with a maximum length limited by the limit variable)
        is returned. Otherwise only one Product object is returned.
        """
        # Row layout
        PRODUCT_LIST_LAYOUT_SELECTOR = '.cat-prod-row'
        # Grid layout
        PRODUCT_GRID_LAYOUT_SELECTOR = '.grid-row'
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
        # Success - we are now on the results page
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
        if product_list_containers:
            # We got the list-like layout
            product_containers = product_list_containers
        elif product_grid_containers:
            # We got the grid-like layout
            product_containers = product_grid_containers
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
        # of each product. Then invoke scrapProductInfo() with each url method 
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

