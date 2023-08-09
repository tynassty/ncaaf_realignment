from __future__ import annotations


class School:

    def __init__(self, name: str, latitude: float, longitude: float, rivals=None):
        if rivals is None:
            rivals = {}
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.rivals = rivals
        self.details = {}

    def get_name(self):
        return self.name

    def get_latitude(self):
        return self.latitude

    def get_longitude(self):
        return self.longitude

    def is_rival(self, other: School):
        return other.get_name() in self.rivals

    def get_rival_weight(self, other: School):
        if not self.is_rival(other):
            return 0
        else:
            return self.rivals.get(other.get_name())

    def get_rivals(self):
        return self.rivals.keys()

    def add_rival(self, other, weight=1):
        self.rivals.update({other.get_name(): weight})

    def add_detail(self, detail_name, detail):
        self.details.update({detail_name: detail})

    def get_detail(self, detail_name):
        return self.details.get(detail_name)

    def __str__(self):
        return self.name

