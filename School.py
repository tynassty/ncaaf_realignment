class School:

    def __init__(self, name: str, latitude: float, longitude: float, rivals=None):
        if rivals is None:
            rivals = []
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.rivals = rivals

    def get_name(self):
        return self.name

    def get_latitude(self):
        return self.latitude

    def get_longitude(self):
        return self.longitude

    def is_rival(self, other):
        return other.get_name() in self.rivals

    def get_rivals(self):
        return self.rivals

    def add_rival(self, other):
        self.rivals.append(other.get_name())

    def __str__(self):
        return self.name

