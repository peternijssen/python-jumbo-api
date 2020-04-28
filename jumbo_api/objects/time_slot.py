from datetime import datetime


class TimeSlot(object):
    def __init__(self, data):
        self.start_date_time = datetime.fromtimestamp(int(data.get("startDateTime")) / 1000)
        self.end_date_time = datetime.fromtimestamp(int(data.get("endDateTime")) / 1000)
        self.available = data.get("available")

    @property
    def is_available(self):
        return self.available

    def __str__(self):
        return f"{self.start_date_time} {self.end_date_time} {self.available}"
