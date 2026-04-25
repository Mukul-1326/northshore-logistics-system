class StockItem:

    def __init__(self, name, qty, reorder_point, hub_id):
        self.name = name
        self.qty = qty
        self.reorder_point = reorder_point
        self.hub_id = hub_id

    def as_tuple(self):
        return (
            self.name,
            self.qty,
            self.reorder_point,
            self.hub_id
        )