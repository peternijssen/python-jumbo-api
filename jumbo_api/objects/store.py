class Store(object):
    def __init__(self, data):
        self.id = data.get("id")
        self.complex_number = data.get("complexNumber")
        self.longitude = data.get("longitude")
        self.latitude = data.get("latitude")

    def __str__(self):
        return f"{self.id} {self.complex_number} {self.longitude} {self.latitude}"
