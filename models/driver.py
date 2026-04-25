class CrewDriver:

    def __init__(self, name, license_no, shift_info):
        self.name = name
        self.license_no = license_no
        self.shift_info = shift_info

    def as_tuple(self):
        return (
            self.name,
            self.license_no,
            self.shift_info
        )