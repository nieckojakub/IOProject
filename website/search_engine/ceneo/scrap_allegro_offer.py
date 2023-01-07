from typing import Union, Any
from calendar import monthrange
from datetime import datetime
import re


def scrapOfferDeliveryPrice(shop_offer_html: Any) -> Union[float, None]:
    DELIVERY_PRICE_DIV_SELECTOR = (
        'div[class="mgn2_13 mqu1_16 mgmw_3z _603a1_KtCRP"]'
    )
    delivery_price_divs = shop_offer_html.select(DELIVERY_PRICE_DIV_SELECTOR)
    if not delivery_price_divs:
        return None
    delivery_price_list = list()
    for delivery_price_div in delivery_price_divs:
        delivery_price_text = delivery_price_div.string
        delivery_price: Any = re.findall(
            "[0-9]+,[0-9]{1,2}", delivery_price_text
        )
        delivery_price = (
            float(delivery_price[0].split(",")[0])
            + float(delivery_price[0].split(",")[1]) / 100
        )
        delivery_price = round(delivery_price, 2)
        delivery_price_list.append(delivery_price)
    if min(delivery_price_list):
        return min(delivery_price_list)
    else:
        return None


def scrapOfferDeliveryTime(shop_offer_html: Any) -> Union[int, None]:
    DELIVERY_TIME_SPAN_SELECTOR = 'span[class="_603a1_vJYrV"]'
    delivery_time_spans = shop_offer_html.select(DELIVERY_TIME_SPAN_SELECTOR)
    if not delivery_time_spans:
        return None
    current_month_days_count = monthrange(
        datetime.now().year, datetime.now().month
    )
    delivery_time_list = list()
    for delivery_time_span in delivery_time_spans:
        delivery_day_text = delivery_time_span.string
        delivery_day_str_list: Any = re.findall("[1-9][0-9]", delivery_day_text)
        for delivery_day_str in delivery_day_str_list:
            delivery_day = int(delivery_day_str)
            if delivery_day <= current_month_days_count:
                delivery_time = current_month_days_count - delivery_day
            else:
                delivery_time = (
                    current_month_days_count - datetime.now().day + delivery_day
                )
            delivery_time_list.append(delivery_time)

    if min(delivery_time_list):
        return min(delivery_time_list)
    else:
        return None
