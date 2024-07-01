class Product:
    def __init__(self,id, barcode, name, quantity, category, expiration, notifexp, notifquan):
        self.id = id
        self.barcode = barcode
        self.name = name
        self.quantity = quantity
        self.category = category
        self.expiration = expiration
        self.notifexp = notifexp
        self.notifquan = notifquan

    def to_json(self):
        return {
            "id": self.id,
            "barcode": self.barcode,
            "name": self.name,
            "quantity": self.quantity,
            "category": self.category,
            "expiration": self.expiration,
            "notifexp": self.notifexp,
            "notifquan": self.notifquan
        }