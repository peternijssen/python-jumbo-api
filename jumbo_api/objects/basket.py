class Basket(object):
    def __init__(self, data):
        self.amount = len(data.get('items'))
        self.price_currency = data.get("prices").get("total").get("currency")
        self.price_amount = data.get("prices").get("total").get("amount")

    @property
    def price(self):
        return self.price_currency + " " + str(self.price_amount / 100)
