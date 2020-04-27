from datetime import datetime


class Delivery(object):
    def __init__(self, data):
        self.id = data.get("id")
        self.status = data.get("status")
        self.delivery_date = datetime.fromtimestamp(int(data.get("delivery").get("date")) / 1000)
        self.delivery_time = data.get("delivery").get("time")
