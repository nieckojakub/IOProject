import re 

def scrapOfferShopName(product_offer):
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

def scrapOfferShopUrl(product_offer, ceneo_url):
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
                shop_url = ceneo_url + '/' + ceneo_shop_link
    else: 
        shop_url = ceneo_url + shop_logo_link[0]["href"]
    return shop_url

def scrapOfferPrice(product_offer):
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
    return round(product_price, 2)

def scrapOfferDeliveryPrice(product_offer, product_price):
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

def scrapOfferAvailability(product_offer):
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

def scrapOfferDeliveryTime(product_offer):
    return None