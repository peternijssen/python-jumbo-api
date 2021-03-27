from datetime import datetime

from jumbo_api.objects.price import Price


class PickUp(object):
    def __init__(self, data, details):
        self.id = data.get("id")
        self.status = data.get("status", "Unknown").lower()
        self.time = data.get("pickup", {}).get("time")
        self.date = data.get("pickup", {}).get("date")
        self.start_time = data.get("pickup", {}).get("startDateTime")
        self.end_time = data.get("pickup", {}).get("endDateTime")
        self.cut_off_date = details.get("orderCutOffDate")
        self.price = Price(data.get("prices", {}).get("total"))

        if self.date is not None:
            self.date = datetime.fromtimestamp(int(self.date) / 1000).strftime("%Y-%m-%d")
        if self.start_time is not None:
            self.start_time = datetime.fromtimestamp(int(self.start_time) / 1000).strftime("%H:%M")
        if self.end_time is not None:
            self.end_time = datetime.fromtimestamp(int(self.end_time) / 1000).strftime("%H:%M")
        if self.cut_off_date is not None:
            self.cut_off_date = datetime.fromtimestamp(int(self.cut_off_date) / 1000)

    def __str__(self):
        return f"{self.id} {self.status} {self.date} {self.time} {self.start_time} {self.end_time} {self.cut_off_date} {self.price}"
