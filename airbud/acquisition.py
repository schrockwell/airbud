from datetime import date, datetime, timezone
import os
import os.path
import json
import csv
import pymap3d
import pymap3d.ellipsoid

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


def default_json_format(object):
    """Formats datetime objects into ISO 8601 for JSON export."""
    if isinstance(object, (date, datetime)):
        return object.isoformat()


class Acquisition:
    def __init__(self):
        self.scan = 'azimuth'
        self.khz = 14313
        self.started_at = None
        self.antenna_coordinate = [0.0, 0.0]
        self.antenna_height_msl = 30
        self.antenna_azimuth_deg = 0
        self.title = 'Airbud'
        self.notes = ''
        self.rx_antenna = 'isotropic'
        self.completed = False

    def start(self):
        """Start the acquisition by initializing the data directory."""
        if self.completed:
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
            writer.writerow([
                'Timestamp',
                'Latitude',
                'Longitude',
                'Altitude',
                'dBFS',
                'Look Azimuth',
                'Look Elevation',
                'Look Range',
                'RX Ant Gain'
            ])

    def add_sample(self, position, dbfs):
        """Append a location/power sample to the log."""
        with open(self.data_csv_path, 'a', newline='') as f:
            look_az, look_el, look_range = self.look_angles(position)

            writer = csv.writer(f)
            writer.writerow([
                datetime.now(timezone.utc).isoformat(),
                position.latitude,
                position.longitude,
                position.altitude,
                dbfs,
                look_az,
                look_el,
                look_range,
                self.rx_antenna_gain_db(look_az, look_el)
            ])

    def look_angles(self, position):
        """Returns (az, el, range) from antenna to UAV in degrees and meters."""
        return pymap3d.geodetic2aer(
            position.latitude,
            position.longitude,
            position.altitude,
            self.antenna_coordinate[0],
            self.antenna_coordinate[1],
            self.antenna_height_msl,
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
        keys = [
            'scan',
            'khz',
            'started_at',
            'antenna_coordinate',
            'antenna_height_msl',
            'antenna_azimuth_deg',
            'rx_antenna',
            'title',
            'notes'
        ]

        # https://stackoverflow.com/a/3420156
        return {key: vars(self)[key] for key in keys}
