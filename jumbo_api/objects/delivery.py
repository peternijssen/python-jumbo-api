from datetime import datetime

from jumbo_api.objects.price import Price


class Delivery(object):
    def __init__(self, data):
        self.id = data.get("id")
        self.status = data.get("status", "Unknown").lower()
        self.time = data.get("delivery", {}).get("time")
        self.date = data.get("delivery", {}).get("date")
        self.start_time = data.get("delivery", {}).get("startDateTime")
        self.end_time = data.get("delivery", {}).get("endDateTime")
        self.cut_off_date = data.get("orderCutOffDate")
        self.eta_start = data.get("shipping", {}).get("plannedETAStart")
        self.eta_end = data.get("shipping", {}).get("plannedETAEnd")
        self.eta_live = data.get("shipping", {}).get("liveETA")
        self.price = Price(data.get("prices", {}).get("total"))

        if self.date is not None:
            self.date = datetime.fromtimestamp(int(self.date) / 1000).strftime("%Y-%m-%d")
        if self.start_time is not None:
            self.start_time = datetime.fromtimestamp(int(self.start_time) / 1000).strftime("%H:%M")
        if self.end_time is not None:
            self.end_time = datetime.fromtimestamp(int(self.end_time) / 1000).strftime("%H:%M")
        if self.cut_off_date is not None:
            self.cut_off_date = datetime.fromtimestamp(int(self.cut_off_date) / 1000)
        if self.eta_start is not None:
            self.eta_start = datetime.fromtimestamp(int(self.eta_start) / 1000).strftime("%H:%M")
        if self.eta_end is not None:
            self.eta_end = datetime.fromtimestamp(int(self.eta_end) / 1000).strftime("%H:%M")
        if self.eta_live is not None:
            self.eta_live = datetime.fromtimestamp(int(self.eta_live) / 1000).strftime("%H:%M")

    def __str__(self):
        return f"{self.id} {self.status} {self.date} {self.time} {self.start_time} {self.end_time} {self.cut_off_date} {self.eta_start} {self.eta_end} {self.eta_live} {self.price}"
