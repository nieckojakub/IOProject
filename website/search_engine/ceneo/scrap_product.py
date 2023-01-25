import re
from typing import Optional, Union, Any


def scrapProductName(product_main_html: Any) -> Union[str, None]:
    """Scrap the product name from the product main page.

    product_main_html: bs4.element containing the product main page html code.
    return: On any error, the return value is None,
        otherwise, a string containing the product name.
    """

    # CSS selector constants
    NAME_SELECTOR = ".product-top__product-info__name"

    # The <h1> tag containing the product name
    product_name_h1 = product_main_html.select(NAME_SELECTOR)
    
    if product_name_h1:
        return product_name_h1[0].string
    else:
        return None


def scrapProductImageUrl(product_main_html: Any) -> Union[str, None]:
    """Scrap the product image url from the product main page.

    product_main_html: bs4.element containing the product main page html code.
    return: On any error, the return value is None,
        otherwise, a string containing the product image url.
    """

    # CSS selector constants.
    IMAGE_DIV_SELECTOR = 'div[class="gallery-carousel__item"]'

    # The html code inside the product image <div> contains <img> tag.
    product_img_div = product_main_html.select(IMAGE_DIV_SELECTOR)
    
    if not product_img_div:
        return None

    # Select the <img> tag.
    product_img = product_img_div[0].select("img")
    
    if not product_img:
        return None

    # Extract the value of the "src" attribute.
    product_img_src = product_img[0]["src"]
    
    if not product_img_src:
        return None
    else:
        return "https:" + product_img_src


def scrapProductRating(
    product_html: Any, is_shop_offer: bool = False
) -> Union[float, None]:
    """Scrap the product rating from the product main page.

    product_html: bs4.element containing the product main page html or shop 
        html code depending on the value of is_shop_offer.
    is_shop_offer: If set to True we have to find rating in the shop offer, 
        otherwise the product main page is used.
    return: On any error, the return value is None,
        otherwise, a float containing the product rating.
    """

    # CSS selector constants.
    REVIEW_DIV_SELECTOR = 'div[class="product-review"]'
    SCORE_SELECTOR = 'span[class="product-review__score"]'
    OFFER_SCORE_SELECTOR = 'span[class="score-marker"]'

    if is_shop_offer:
        # There is no Product rating in the ceneo product overview.
        # Try to extract rating from the first product offer.

        # The html code inside the score <span> contains "style" attribute 
        # with the rating value.
        score_span = product_html.select(OFFER_SCORE_SELECTOR)

        if not score_span:
            return None
        # Extract the value of the "style" attribute.
        span_style = score_span[0]["style"]

        if not span_style:
            return None
        
        # Find rating pattern in %
        rating_procent = re.findall("([0-9]+|[0-9]+\.[0-9]+)%", span_style)

        try:
            # Try to format rating value
            rating_procent = float(rating_procent) / 100
        except:
            return None
        else:
            # Round the rating
            product_rating = round(rating_procent * 5, 2)

            return product_rating
    
    # Product main page
    # The html code inside the product review <div> contains <span> tag with 
    # the product rating. 
    product_review_div = product_html.select(REVIEW_DIV_SELECTOR)
    
    if not product_review_div:
        return None
    
    # Select <span>
    product_score_span = product_review_div[0].select(SCORE_SELECTOR)
    
    if not product_score_span:
        return False
    
    # Extract the value of the "content" attribute.
    product_rating = product_score_span[0]["content"]
    
    if not product_rating:
        return None
    else:
        # Round the rating
        return round(float(product_rating), 2)


def scrapProductDescription(product_main_html: Any) -> str:
    """Scrap the product description from the product main page.

    product_main_html: bs4.element containing the product main page html code.
    return: If not found, the return value is the NO_DESCRIPTION constant,
        otherwise, a string containing the product description.
    """

    # CSS selector constants.
    DESCRIPTION_DIV_SELECTOR = 'div[class="product-top__product-info__tags"]'

    # No description constant
    NO_DESCRIPTION = "No description found"
    
    # The html code inside the product description <div> contains description 
    # text. 
    product_description_div = product_main_html.select(DESCRIPTION_DIV_SELECTOR)
    
    if not product_description_div:
        return NO_DESCRIPTION

    # Extract the description inside the <div> tag.    
    product_description = product_description_div[0].string

    if not product_description:
        return NO_DESCRIPTION
    else:
        return product_description
