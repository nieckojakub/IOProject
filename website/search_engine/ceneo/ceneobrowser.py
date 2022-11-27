from mechanicalsoup import Browser
from search_engine import Product, Shop
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
    PRODUCT_DIVS_SELECTOR = '.cat-prod-row'
    PRODUCT_MAIN_DIV_SELECTOR = '.product-top'
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
        # Product rating
        product_rating_span = product_main_html.select(
            'span[class="product-review__score"]'
        )[0]
        product_rating = round(float(product_rating_span["content"]), 2)
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
            price_value = price_span.select('span[class="value"]')[0].string
            price_penny = price_span.select('span[class="penny"]')[0].string
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

        self.search_input["value"] = search_query
        search_results_page = self.submit(self.search_form, self.url)
        if search_results_page.url == self.url:
            # Invalid query
            return
        search_result_html = search_results_page.soup
        product_divs = search_result_html.select(self.PRODUCT_DIVS_SELECTOR)
        product_count = len(product_divs)
        limit = product_count if product_count < limit else limit
        if limit == 0:
            # Product main page case
            return self.scrapProductInfo(search_results_page.url)
        # Numerous results
        product_list = list()
        for i in range(0, limit):
            product_link_regex = re.compile("/[0-9]+")
            links = product_divs[i].find_all("a")
            for link in links:
                regex_result = product_link_regex.match(link["href"])
                if regex_result is not None:
                    product_main_page_url = self.URL + link["href"]
                    product_list.append(self.scrapProductInfo(product_main_page_url))
                    break
        return product_list
