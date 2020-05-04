from jumbo_api.objects.store import Store


class Profile(object):
    def __init__(self, data):
        self.id = data.get("identifier")
        self.store = Store(data.get("store"))

    def __str__(self):
        return f"{self.id} {self.store}"
