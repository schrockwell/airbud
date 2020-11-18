class Position:
    def __init__(self, micropy_gps):
        ordinate, cardinal = micropy_gps.latitude
        self.latitude = ordinate * (1 if cardinal == 'N' else -1)

        ordinate, cardinal = micropy_gps.longitude
        self.longitude = ordinate * (1 if cardinal == 'E' else -1)

        self.altitude = micropy_gps.altitude
        self.valid = micropy_gps.valid
        self.speed = micropy_gps.speed[2]  # km/hr
        self.course = micropy_gps.course
        self.satellites_in_use = micropy_gps.satellites_in_use

    def to_dict(self):
        return vars(self)
