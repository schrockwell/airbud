"""GPS position data."""


class Position:
    """Represents the state of the GPS receiver at a point in time."""

    def __init__(self, micropy_gps):
        ordinate, cardinal = micropy_gps.latitude or (0, 0)
        self.latitude = ordinate * (1 if cardinal == 'N' else -1)

        ordinate, cardinal = micropy_gps.longitude or (0, 0)
        self.longitude = ordinate * (1 if cardinal == 'E' else -1)

        self.altitude_m = micropy_gps.altitude or 0
        self.valid = micropy_gps.valid
        self.speed_kmhr = micropy_gps.speed[2] or 0  # km/hr
        self.course = micropy_gps.course or 0
        self.satellites_in_use = micropy_gps.satellites_in_use or 0

    def to_dict(self):
        return vars(self)
