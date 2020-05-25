from datetime import datetime

from jumbo_api.objects.price import Price


class PickUp(object):
    def __init__(self, data, details):
        delivery_date = datetime.fromtimestamp(int(data.get("pickup").get("date")) / 1000)

        self.id = data.get("id")
        self.status = data.get("status").lower()
        self.date = delivery_date.strftime("%Y-%m-%d")
        self.time = data.get("pickup").get("time")
        self.start_time = datetime.fromtimestamp(int(data.get("pickup").get("startDateTime")) / 1000)
        self.end_time = datetime.fromtimestamp(int(data.get("pickup").get("endDateTime")) / 1000)
        self.cut_off_date = datetime.fromtimestamp(int(details.get("orderCutOffDate")) / 1000)
        self.price = Price(data.get("prices").get("total"))

    def __str__(self):
        return f"{self.id} {self.status} {self.date} {self.time} {self.start_time} {self.end_time} {self.cut_off_date} {self.price}"
