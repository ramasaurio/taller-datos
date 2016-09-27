
class Country:

    def __init__(self, values):
        code, lat, lon, name = values
        self.name = name
        self.lat = float(lat)
        self.lon = float(lon)
        self.code = code
