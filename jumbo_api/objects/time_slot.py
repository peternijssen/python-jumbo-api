from datetime import datetime

from jumbo_api.objects.price import Price


class TimeSlot(object):
    def __init__(self, data):
        self.type = data.get("type").lower()
        self.start_date_time = datetime.fromtimestamp(int(data.get("startDateTime")) / 1000)
        self.end_date_time = datetime.fromtimestamp(int(data.get("endDateTime")) / 1000)
        self.available = data.get("available")
        self.price = None

        if self.is_available:
            self.price = Price(data.get("price"))

    @property
    def is_available(self):
        return self.available

    def __str__(self):
        return f"{self.type} {self.start_date_time} {self.end_date_time} {self.available} {self.price}"
