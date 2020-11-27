from datetime import date, datetime, timezone

csv_columns = [
    'timestamp',
    'latitude',
    'longitude',
    'altitude_m',
    'dbfs',
    'look_az',
    'look_el',
    'look_range',
    'rx_antenna_gain',
    'fspl_db'
]


class PowerSample:
    @staticmethod
    def header_row():
        return csv_columns

    def __init__(self):
        self.timestamp = datetime.now(timezone.utc).isoformat()
        self.latitude = 0
        self.longitude = 0
        self.altitude_m = 0
        self.dbfs = 0
        self.look_az = 0
        self.look_el = 0
        self.look_range = 0
        self.rx_antenna_gain = 0
        self.fspl_db = 0

    def to_row(self):
        return list(map(lambda col: vars(self)[col], csv_columns))

    @staticmethod
    def from_dict(row):
        sample = PowerSample()
        sample.timestamp = datetime.fromisoformat(row['timestamp'])
        sample.latitude = float(row['latitude'])
        sample.longitude = float(row['longitude'])
        sample.altitude_m = float(row['altitude_m'])
        sample.dbfs = float(row['dbfs'])
        sample.look_az = float(row['look_az'])
        sample.look_el = float(row['look_el'])
        sample.look_range = float(row['look_range'])
        sample.rx_antenna_gain = float(row['rx_antenna_gain'])
        sample.fspl_db = float(row['fspl_db'])
        return sample
