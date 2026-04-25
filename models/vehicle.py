class FleetUnit:

    def __init__(self, capacity, status, maintenance_due):
        self.capacity = capacity
        self.status = status
        self.maintenance_due = maintenance_due

    def as_tuple(self):
        return (
            self.capacity,
            self.status,
            self.maintenance_due
        )