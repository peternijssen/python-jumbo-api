from objects.price import Price


class Basket(object):
    def __init__(self, data):
        self.amount = len(data.get('items'))
        self.price = Price(data.get("prices").get('total'))

    def __str__(self):
        return f"{self.amount} {self.price}"
