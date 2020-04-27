class Basket(object):
    def __init__(self, data):
        self.amount = len(data.get('items'))
