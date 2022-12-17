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
    
    def __init__(self, url=URL):
        Browser.__init__(self)
        self.url = url
        self.ceneo_page = self.get(url)
        self.ceneo_html = self.ceneo_page.soup
        self.search_form = self.ceneo_html.select(self.FORM_SELECTOR)[0]
        self.search_input = self.search_form.select(self.FORM_INPUT_SELECTOR)[0]

    def scrapProductName(self, product_main_html):
        NAME_SELECTOR = '.product-top__product-info__name'
        product_name_h1 = product_main_html.select(NAME_SELECTOR)
        if product_name_h1:
            return product_name_h1[0].string
        else:
            return None

    def scrapProductImageUrl(self, product_main_html):
        IMAGE_DIV_SELECTOR = 'div[class="gallery-carousel__item"]'
        product_img_div = product_main_html.select(IMAGE_DIV_SELECTOR)
        if not product_img_div:
            return None
        product_img = product_img_div[0].select('img')
        if not product_img:
            return None
        product_img_src = product_img[0]['src']
        if not product_img_src:
            return None
        else:
            return 'https:' + product_img_src

    def scrapProductRating(self, product_html, is_offer=False):
        REVIEW_DIV_SELECTOR = 'div[class="product-review"]'
        SCORE_SELECTOR = 'span[class="product-review__score"]'
        OFFER_SCORE_SELECTOR = 'span[class="score-marker"]'
        if is_offer:
            # There is no Product rating in the ceneo product overview.
            # Try to extract rating from the first product offer.
            score_span = product_html.select(OFFER_SCORE_SELECTOR)
            if not score_span:
                return None
            span_style = score_span[0]['style']
            if not span_style:
                return None
            rating_procent = re.findall('([0-9]+|[0-9]+\.[0-9]+)%', span_style)
            try:
                rating_procent = float(rating_procent) / 100
            except:
                return None
            else:
                product_rating = round(rating_procent * 5, 2)
                return product_rating
        product_review_div = product_html.select(REVIEW_DIV_SELECTOR)
        if not product_review_div:
            return None
        product_score_span = product_review_div[0].select(SCORE_SELECTOR)
        if not product_score_span:
            return False
        product_rating = product_score_span[0]["content"]
        if not product_rating:
            return None
        else:
            return round(float(product_rating), 2)

    def scrapProductDescription(self, product_main_html):
        DESCRIPTION_DIV_SELECTOR = 'div[class="product-top__product-info__tags"]'
        product_description_div = product_main_html.select(DESCRIPTION_DIV_SELECTOR)
        if not product_description_div:
            return None
        product_description = product_description_div[0].string
        if not product_description:
            return None
        else:
            return product_description
            
    def scrapOfferShopName(self, product_offer):
        OPINION_LI_SELECTOR='li[class="offer-shop-opinions"]'
        PREFIX = 'Dane i opinie o '
        shop_opinon_li = product_offer.select(OPINION_LI_SELECTOR)
        if not shop_opinon_li:
            return None
        shop_opinion = shop_opinon_li[0].select("a")
        if not shop_opinion:
            return None
        shop_name = shop_opinion[0].string.split(PREFIX)[-1].strip("\n")
        if not shop_name:
            return None
        else:
            return shop_name

    def scrapOfferShopUrl(self, product_offer):
        SHOP_DIV_SELECTOR = 'div[class="product-offer__store__logo"]'
        OPINION_LI_SELECTOR='li[class="offer-shop-opinions"]'
        INFO_SUFFIX = '#tab=info'
        shop_logo_div = product_offer.select(SHOP_DIV_SELECTOR)
        if not shop_logo_div:
            return None
        shop_logo_link = shop_logo_div[0].select('a')
        if not shop_logo_link:
            shop_logo_link = shop_logo_div[0].select('img')
            if not shop_logo_link:
                return None
            else:
                shop_opinon_li = product_offer.select(OPINION_LI_SELECTOR)
                if not shop_opinon_li:
                    return None
                ceneo_shop_a_tag  = shop_opinon_li[0].select('a')
                if not ceneo_shop_a_tag:
                    return None
                else:
                    ceneo_shop_href = ceneo_shop_a_tag[0]['href']
                    ceneo_shop_link = ceneo_shop_href.split(INFO_SUFFIX)[0]
                    shop_url = self.URL + '/' + ceneo_shop_link
        else: 
            shop_url = self.URL + shop_logo_link[0]["href"]
        return shop_url

    def scrapOfferPrice(self, product_offer):
        PRICE_SPAN_SELECTOR = 'span[class="price"]'
        VALUE_SPAN_SELECTOR = 'span[class="value"]'
        PENNY_SPAN_SELECTOR = 'span[class="penny"]'
        price_span = product_offer.select(PRICE_SPAN_SELECTOR)
        if not price_span:
            return None
        value_span = price_span[0].select(VALUE_SPAN_SELECTOR)
        penny_span = price_span[0].select(PENNY_SPAN_SELECTOR)
        if not value_span or not penny_span:
            return None
        else:
            value = float(value_span[0].string.replace(' ', ''))
            penny = penny_span[0].string.replace(' ', '').strip(",")
            penny = float(penny) / 100
        product_price = value + penny
        return product_price

    def scrapOfferDeliveryPrice(self, product_offer, product_price):
        DELIVERY_SPAN_SELECTOR = 'span.product-delivery-info'
        FREE_DELIVERY_SELECTOR = '.free-delivery-label'
        delivery_price_span = product_offer.select(DELIVERY_SPAN_SELECTOR)
        if not delivery_price_span:
            return None
        if delivery_price_span[0].select(FREE_DELIVERY_SELECTOR):
            # Free delivery label found 
            return 0
        # Check if delivery is free
        delivery_price_text = delivery_price_span[0].string
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
            return delivery_price
        else:
            return None

    def scrapOfferAvailability(self, product_offer):
        AVAIL_DIV_SELECTOR = 'div[class="product-availability"]'
        product_availability_div = product_offer.select(AVAIL_DIV_SELECTOR)
        if not product_availability_div:
            return None
        product_availability_span = product_availability_div[0].select("span")
        if not product_availability_span:
            return None
        availabilty_message = product_availability_span[0].string
        product_availability = re.findall("[0-9]+", availabilty_message)
        if not product_availability:
            product_availability = 0
        else:
            product_availability = int(product_availability[0])
        return product_availability

    def scrapOfferDeliveryTime(self, product_offer):
        return None

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
        product_name = self.scrapProductName(product_main_html)
        
        # Product image url
        product_img_url = self.scrapProductImageUrl(product_main_html)
        
        # Product rating
        product_rating = self.scrapProductRating(product_main_html)

        # Product description
        product_description = self.scrapProductDescription(product_main_html)
        
        # Shop objects
        shop_list = list()

        product_offers = product_main_html.select(PRODUCT_OFFER_SELECTOR)
        if not product_rating and product_offers:
            # There is no Product rating in the ceneo product overview.
            # Try to extract rating from the first product offer.
            product_rating = self.scrapProductRating(
                                                    product_offers[0], 
                                                    is_offer=True
                                                    )
        for product_offer in product_offers:
            # Shop name
            shop_name = self.scrapOfferShopName(product_offer)
            # Shop url
            shop_url = self.scrapOfferShopUrl(product_offer)
            # Product price
            product_price = self.scrapOfferPrice(product_offer)
            # Delivery price
            delivery_price = self.scrapOfferDeliveryPrice(
                                                        product_offer, 
                                                        product_price
                                                        )
            # Product availability
            product_availability = self.scrapOfferAvailability(product_offer)
            # Product delivery time
            delivery_time = self.scrapOfferDeliveryTime(product_offer)
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

