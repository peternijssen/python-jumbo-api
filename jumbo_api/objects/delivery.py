from datetime import datetime

from jumbo_api.objects.price import Price


class Delivery(object):
    def __init__(self, data):
        delivery_date = datetime.fromtimestamp(int(data.get("delivery").get("date")) / 1000)

        self.id = data.get("id")
        self.status = data.get("status")
        self.delivery_date = delivery_date.strftime("%Y-%m-%d")
        self.delivery_time = data.get("delivery").get("time")
        self.delivery_start_time = datetime.fromtimestamp(int(data.get("delivery").get("startDateTime")) / 1000)
        self.delivery_end_time = datetime.fromtimestamp(int(data.get("delivery").get("endDateTime")) / 1000)
        self.price = Price(data.get("prices").get("total"))

    def __str__(self):
        return f"{self.id} {self.status} {self.delivery_date} {self.delivery_time} {self.delivery_start_time} {self.delivery_end_time} {self.price}"
