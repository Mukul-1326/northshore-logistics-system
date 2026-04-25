class StoreHub:

    def __init__(self, name, location):
        self.name = name
        self.location = location

    def as_tuple(self):
        return (
            self.name,
            self.location
        )