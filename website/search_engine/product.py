class Product:
    def __init__(self, name: str,  url: str, img: str, shop_list: list, description: str, rating: float):
        # product name
        self.name = name

        # ceneo/allegro search url
        self.url = url

        # img link
        self.img = img

        # shop list
        self.shop_list = shop_list

        # description
        self.description = description

        # rating <0; 5>
        self.rating = rating

    def __str__(self):
        descr = "NAME: {} RATING: {}\n". format(self.name, self.rating)
        descr += "{}\n".format(self.description)
        for shop in self.shop_list:
            descr += str(shop)
        return descr + '\n'
        
