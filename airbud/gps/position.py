class Position:
    def __init__(self, micropy_gps):
        ordinate, cardinal = micropy_gps.latitude
        self.latitude = ordinate * (1 if cardinal == 'N' else -1)

        ordinate, cardinal = micropy_gps.longitude
        self.longitude = ordinate * (1 if cardinal == 'E' else -1)