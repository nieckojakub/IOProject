import re
from typing import Union, Any


def scrapOfferShopName(shop_offer_html: Any) -> Union[str, None]:
    """Scrap the shop name from the product shop offer.

    shop_offer_html: bs4.element containing shop offer html code.
    return: On any error, the return value is None.
        Otherwise, a string containing the shop name.
    """

    # CSS selector constants.
    OPINION_LI_SELECTOR = 'li[class="offer-shop-opinions"]'
    PREFIX = "Dane i opinie o "

    # The html code inside the shop opinion <li> contains <a> tag with the
    # shop name.
    shop_opinon_li = shop_offer_html.select(OPINION_LI_SELECTOR)

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


def scrapOfferShopUrl(shop_offer_html: Any, ceneo_url: str) -> Union[str, None]:
    """Scrap the shop url from the product shop offer.

    shop_offer_html: bs4.element containing shop offer html code.
    ceneo_url: The part of the url that is added to the begining of the
        scrapped shop url.
    return: On any error, the return value is None.
        Otherwise, a string containing the shop url.
    """

    # CSS selector constants
    SHOP_DIV_SELECTOR = 'div[class="product-offer__store__logo"]'
    OPINION_LI_SELECTOR = 'li[class="offer-shop-opinions"]'
    INFO_SUFFIX = "#tab=info"

    # The html code inside the shop logo <div> contains <a> tag with the shop
    # url suffix.
    shop_logo_div = shop_offer_html.select(SHOP_DIV_SELECTOR)
    if not shop_logo_div:
        return None

    # Extract the <a> tags.
    shop_logo_link = shop_logo_div[0].select("a")

    if not shop_logo_link:
        # The <a> tags not present in the logo <div>. Try with the <img>.
        shop_logo_link = shop_logo_div[0].select("img")
        if not shop_logo_link:
            return None
        else:
            shop_opinon_li = shop_offer_html.select(OPINION_LI_SELECTOR)
            if not shop_opinon_li:
                return None
            ceneo_shop_a_tag = shop_opinon_li[0].select("a")
            if not ceneo_shop_a_tag:
                return None
            else:
                ceneo_shop_href = ceneo_shop_a_tag[0]["href"]
                ceneo_shop_link = ceneo_shop_href.split(INFO_SUFFIX)[0]
                shop_url = ceneo_url + "/" + ceneo_shop_link
    else:
        shop_url = ceneo_url + shop_logo_link[0]["href"]

    return shop_url


def scrapOfferPrice(shop_offer_html: Any) -> Union[float, None]:
    """Scrap the shop price from the product shop offer.

    shop_offer_html: bs4.element containing shop offer html code.
    return: On any error, the return value is None.
        Otherwise, a float containing the product price.
    """

    # CSS selector constants
    PRICE_SPAN_SELECTOR = 'span[class="price"]'
    VALUE_SPAN_SELECTOR = 'span[class="value"]'
    PENNY_SPAN_SELECTOR = 'span[class="penny"]'

    # The html code inside the price <span> contains another <span> tags,
    # which add up to the total product price.
    price_span = shop_offer_html.select(PRICE_SPAN_SELECTOR)

    if not price_span:
        return None
    value_span = price_span[0].select(VALUE_SPAN_SELECTOR)
    penny_span = price_span[0].select(PENNY_SPAN_SELECTOR)

    if not value_span or not penny_span:
        return None
    else:
        # Format the price
        value = float(value_span[0].string.replace(" ", ""))
        penny = penny_span[0].string.replace(" ", "").strip(",")
        penny = float(penny) / 100
    product_price = value + penny

    return round(product_price, 2)


def scrapOfferDeliveryPrice(
    shop_offer_html: Any, product_price: Union[float, None]
) -> Union[float, None]:
    """Scrap the shop delivery price from the product shop offer.

    shop_offer_html: bs4.element containing shop offer html code.
    product_price: Product price. If not found the None is expected.
        This param is required since the Ceneo shows us the delivery price
        in the form: delivery_price + product_price.
    return: On any error, the return value is None.
        Otherwise, a float containing the product delivery price.
    """

    # CSS selector constants.
    DELIVERY_SPAN_SELECTOR = "span.product-delivery-info"
    FREE_DELIVERY_SELECTOR = ".free-delivery-label"

    # The html code inside the delivery price <span> contains another <span> tag with the
    # total of: "Some string" + delivery_price + product_price.
    delivery_price_span = shop_offer_html.select(DELIVERY_SPAN_SELECTOR)

    if not delivery_price_span:
        return None

    # Check if the delivery is free.
    if delivery_price_span[0].select(FREE_DELIVERY_SELECTOR):
        # Free delivery label found.
        return 0

    # Product price is None. There is no point to continue.
    if product_price is None:
        return None

    # Extract the text inside the <span> tag.
    delivery_price_text = delivery_price_span[0].string

    if delivery_price_text:
        delivery_price: Any = re.findall(
            "[0-9]+,[0-9]{1,2}", delivery_price_text
        )
        # Check whether the price pattern has been found, if not,
        # the shop offer does not directly display the delivery price.
        if delivery_price:
            # Format the price
            delivery_price = (
                float(delivery_price[0].split(",")[0])
                + float(delivery_price[0].split(",")[1]) / 100
            )
            delivery_price = round(delivery_price - product_price, 2)
        else:
            # The delivery price is not displayed.
            delivery_price = None
        return delivery_price
    else:
        return None


def scrapOfferAvailability(shop_offer_html: Any) -> Union[int, None]:
    """Scrap the product availability from the product shop offer.

    shop_offer_html: bs4.element containing shop offer html code.
    return: On any error, the return value is None.
        Otherwise, an int which specifies how many days we have to wait
        for the product to become avaiable.
    """
    # CSS selector constants.
    AVAIL_DIV_SELECTOR = 'div[class="product-availability"]'

    # The html code inside the product availability <div> contains <span> tag
    # with the product availabilty info.
    product_availability_div = shop_offer_html.select(AVAIL_DIV_SELECTOR)

    if not product_availability_div:
        return None

    # Extract the code with the <span> tag.
    product_availability_span = product_availability_div[0].select("span")

    if not product_availability_span:
        return None

    # Extract the text inside the <span> tag.
    availabilty_message = product_availability_span[0].string
    # Find the pattern with the number of days.
    product_availability: Any = re.findall("[0-9]+", availabilty_message)

    if not product_availability:
        # Pattern not found, which means that the product is in stock.
        product_availability = 0
    else:
        # Format the product_availability.
        product_availability = int(product_availability[0])

    return product_availability


def scrapOfferDeliveryTime(shop_offer_html: Any) -> Union[int, None]:
    """Scrap the product delivery time from the product shop offer.

    shop_offer_html: bs4.element containing shop offer html code.
    return: On any error, the return value is None.
        Otherwise, an int which specifies how many days we have to wait
        for the product to arrive.
    """
    # Currently Ceneo does not show the product delivery time.
    return None
