class CargoMove:

    def __init__(self, order_ref, sender, receiver, item_desc, hub_id, status="IN_TRANSIT", ship_id=None):
        self.ship_id = ship_id
        self.order_ref = order_ref
        self.sender = sender
        self.receiver = receiver
        self.item_desc = item_desc
        self.hub_id = hub_id
        self.status = status

    def as_tuple(self):
        return (
            self.order_ref,
            self.sender,
            self.receiver,
            self.item_desc,
            self.status,
            self.hub_id
        )

    def with_id_tuple(self):
        return (
            self.ship_id,
            self.order_ref,
            self.sender,
            self.receiver,
            self.item_desc,
            self.status,
            self.hub_id
        )