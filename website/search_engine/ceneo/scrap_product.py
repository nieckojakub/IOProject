import re

def scrapProductName(product_main_html):
    NAME_SELECTOR = '.product-top__product-info__name'
    product_name_h1 = product_main_html.select(NAME_SELECTOR)
    if product_name_h1:
        return product_name_h1[0].string
    else:
        return None

def scrapProductImageUrl(product_main_html):
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

def scrapProductRating(product_html, is_offer=False):
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

def scrapProductDescription(product_main_html):
    DESCRIPTION_DIV_SELECTOR = 'div[class="product-top__product-info__tags"]'
    product_description_div = product_main_html.select(DESCRIPTION_DIV_SELECTOR)
    if not product_description_div:
        return "No description found"
    product_description = product_description_div[0].string
    if not product_description:
        return "No description found"
    else:
        return product_description