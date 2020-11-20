from pylab import *
import matplotlib.pyplot as pyplot
import os
import os.path as path
from airbud.acquisition import Acquisition


def generate(acquisition):
    """Saves plot PNGs to disk."""

    samples = acquisition.power_samples
    az_plot_path = path.join(acquisition.data_dir, 'azimuth.png')
    el_plot_path = path.join(acquisition.data_dir, 'elevation.png')

    mhz = '%0.3f' % (acquisition.khz / 1e3)
    title = f'{acquisition.title} @ {mhz} MHz'

    powers = [sample.dbfs for sample in samples]
    look_azs = [sample.look_az for sample in samples]
    look_els = [sample.look_el for sample in samples]

    # Normalize 0 dB to max measured power
    max_power = max(powers)
    normalized_powers = [power - max_power for power in powers]

    clf()
    _fig, ax = pyplot.subplots(subplot_kw={'projection': 'polar'})
    ax.plot(deg2rad(look_azs), normalized_powers)
    ax.set_title(f'Azimuth – {title}')
    savefig(az_plot_path)

    clf()
    _fig, ax = pyplot.subplots(subplot_kw={'projection': 'polar'})
    ax.plot(deg2rad(look_els), normalized_powers)
    ax.set_title(f'Elevation – {title}')
    savefig(el_plot_path)


if __name__ == '__main__':
    data_dirs = [x[0] for x in os.walk('data')]
    count = 0

    for data_dir in data_dirs:
        acq = Acquisition.load(data_dir)
        if not acq:
            continue

        generate(acq)
        count += 1

    print(f'Generated plots for {count} acquisitions')
