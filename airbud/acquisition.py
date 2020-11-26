from datetime import date, datetime, timezone
import os
import os.path
import json
import csv
import pymap3d
import pymap3d.ellipsoid
from airbud.power_sample import PowerSample

# GPS models the Earth with WGS84
ellipsoid = pymap3d.ellipsoid.Ellipsoid("wgs84")

# Potential ways to sweep across the antenna pattern
scan_types = {
    'azimuth': 'AZ',
    'elevation': 'EL',
    'volume': 'VOL',
}

# Potential receive antenna types
rx_antenna_types = {
    'isotropic': 'Isotropic'
}

public_keys = [
    'scan',
    'khz',
    'started_at',
    'antenna_latitude',
    'antenna_longitude',
    'antenna_altitude_m',
    'antenna_azimuth_deg',
    'rx_antenna',
    'title',
    'notes'
]


def default_json_format(object):
    """Formats datetime objects into ISO 8601 for JSON export."""
    if isinstance(object, (date, datetime)):
        return object.isoformat()


class Acquisition:
    @staticmethod
    def load(data_dir):
        json_path = os.path.join(data_dir, 'conditions.json')
        if not os.path.exists(json_path):
            return None

        with open(json_path, 'r') as f:
            conditions = json.load(f)

        acq = Acquisition()
        acq.conditions = conditions
        return acq

    def __init__(self):
        self.scan = 'azimuth'
        self.khz = 14313
        self.started_at = None
        self.antenna_latitude = 0.0
        self.antenna_longitude = 0.0
        self.antenna_altitude_m = 0.0
        self.antenna_azimuth_deg = 0
        self.title = 'Airbud'
        self.notes = ''
        self.rx_antenna = 'isotropic'
        self.completed = False

    def clone(self):
        result = Acquisition()
        result.conditions = self.conditions
        result.started_at = None
        return result

    def start(self):
        """Start the acquisition by initializing the data directory."""
        if self.started_at or self.completed:
            raise Exception(
                'This acquisition has been completed and cannot be restarted.'
            )

        self.started_at = datetime.now(timezone.utc)

        # Must be called after setting started_at
        os.makedirs(self.data_dir)

        # Create conditions.json
        with open(self.conditions_json_path, 'w') as f:
            json.dump(self.conditions, f, indent=4,
                      default=default_json_format)

        # Create data CSV and write header row
        with open(self.data_csv_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(PowerSample.header_row())

    def add_sample(self, position, dbfs):
        """Append a location/power sample to the log."""
        with open(self.data_csv_path, 'a', newline='') as f:
            look_az, look_el, look_range = self.look_angles(position)

            sample = PowerSample()
            sample.timestamp = datetime.now(timezone.utc).isoformat()
            sample.latitude = position.latitude
            sample.longitude = position.longitude
            sample.altitude_m = position.altitude_m
            sample.dbfs = dbfs
            sample.look_az = look_az
            sample.look_el = look_el
            sample.look_range = look_range
            sample.rx_antenna_gain = self.rx_antenna_gain_db(look_az, look_el)

            writer = csv.writer(f)
            writer.writerow(sample.to_row())

    def look_angles(self, position):
        """Returns (az, el, range) from antenna to UAV in degrees and meters."""
        return pymap3d.geodetic2aer(
            position.latitude,
            position.longitude,
            position.altitude_m,
            self.antenna_latitude or 0,
            self.antenna_longitude or 0,
            self.antenna_altitude_m or 0,
            ellipsoid,
            True  # degrees (instead of radians)
        )

    def rx_antenna_gain_db(self, look_az, look_el):
        """Returns the relative gain of the receive antenna for a signal incoming from a given direction."""
        if self.rx_antenna == 'isotropic':
            return 0.0
        else:
            raise Exception(f'Unknown antenna type: {self.rx_antenna}')

    def stop(self):
        """Complete the acquisiton once and for all. It cannot be restarted."""
        self.completed = True

    @property
    def data_dir(self):
        """Returns the directory for this acquisition after it's been started."""
        date_dir = self.started_at.strftime('%Y-%m-%d')

        time = self.started_at.strftime('%H-%M-%S')
        scan = scan_types[self.scan]
        khz = '%06d' % self.khz
        acq_dir = f'{time}_{scan}_{khz}'

        return os.path.join('data', date_dir, acq_dir)

    @property
    def conditions_json_path(self):
        return os.path.join(self.data_dir, 'conditions.json')

    @property
    def data_csv_path(self):
        return os.path.join(self.data_dir, 'data.csv')

    @property
    def plot_png_path(self):
        return os.path.join(self.data_dir, 'plot.png')

    @property
    def conditions(self):
        # https://stackoverflow.com/a/3420156
        return {key: vars(self)[key] for key in public_keys}

    @conditions.setter
    def conditions(self, values_dict):
        for key in values_dict:
            if key in public_keys:
                setattr(self, key, values_dict[key])

        if isinstance(self.started_at, str):
            self.started_at = datetime.fromisoformat(self.started_at)

    @property
    def power_samples(self):
        samples = []

        with open(self.data_csv_path, 'r') as f:
            reader = csv.DictReader(f)
            samples = list(map(lambda row: PowerSample.from_dict(row), reader))

        return samples
