
class Country:

    def __init__(self, values):
        code, lat, lon, name = values
        self.name = name
        self.lat = lat
        self.lon = lon
        self.code = code
