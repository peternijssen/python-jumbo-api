class Price(object):
    def __init__(self, data):
        self.currency = data.get("currency")
        self.amount = data.get("amount")

    @property
    def format(self):
        return self.currency + " " + str(self.amount / 100)

    def __str__(self):
        return f"{self.currency} {self.amount} {self.format}"
