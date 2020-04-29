class Price(object):
    def __init__(self, data):
        self.price_currency = data.get("currency")
        self.price_amount = data.get("amount")

    @property
    def price(self):
        return self.price_currency + " " + str(self.price_amount / 100)

    def __str__(self):
        return f"{self.price_currency} {self.price_amount} {self.price}"
