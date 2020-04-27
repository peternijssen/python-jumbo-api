from datetime import datetime


class Delivery(object):
    def __init__(self, data):
        delivery_date = datetime.fromtimestamp(int(data.get("delivery").get("date")) / 1000)

        self.id = data.get("id")
        self.status = data.get("status")
        self.delivery_date = delivery_date.strftime("%Y-%m-%d")
        self.delivery_time = data.get("delivery").get("time")
        self.delivery_start_time = datetime.fromtimestamp(int(data.get("delivery").get("startDateTime")) / 1000)
        self.delivery_end_time = datetime.fromtimestamp(int(data.get("delivery").get("endDateTime")) / 1000)
        self.price_currency = data.get("prices").get("total").get("currency")
        self.price_amount = data.get("prices").get("total").get("amount")

    @property
    def price(self):
        return self.price_currency + " " + str(self.price_amount / 100)
