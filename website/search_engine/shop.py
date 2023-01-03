from typing import Union


class Shop:
    def __init__(
        self,
        name: Union[str, None],
        url: Union[str, None],
        price: Union[float, None],
        delivery_price: Union[float, None],
        availability: Union[int, None],
        delivery_time: Union[float, None],
    ):
        # shop name
        self.name = name

        # shop link
        self.url = url

        # product price
        self.price = price

        # delivery price
        self.delivery_price = delivery_price

        # availability in shop 0 - available, 1 - in one day etc.
        self.availability = availability

        # delivery time
        self.delivery_time = delivery_time

    def __str__(self):
        descr = "\tSHOP: {} PRICE: {}ZŁ\n".format(self.name, self.price)
        descr += "\tDELIVERY PRICE: {}".format(self.delivery_price)
        descr += "\tAVAILABILIT WITHIN {} DAYS\n".format(self.availability)
        descr += "\tDELIVERY TIME: {}\n".format(self.delivery_time)
        return descr
