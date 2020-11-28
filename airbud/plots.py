"""Generates plots from acquisition data after the acquisition is complete.

Call this module as `__main__` to regenerate plots for all data directories."""

from pylab import *
import matplotlib.pyplot as pyplot
import os
import os.path as path
from airbud.acquisition import Acquisition
from collections import namedtuple

PlotVariant = namedtuple('PlotVariant', ['id', 'title', 'powers'])


def generate(acquisition):
    """Saves plot PNGs to disk."""

    samples = acquisition.power_samples
    powers = [sample.dbfs for sample in samples]
    adjusted_powers = [sample.dbfs + sample.fspl_db for sample in samples]

    variants = [
        PlotVariant(id='raw', title='Normalized', powers=powers),
        PlotVariant(id='fspl', title='Path-Normalized',
                    powers=adjusted_powers),
    ]

    for variant in variants:
        generate_variant(acquisition, variant)


def generate_variant(acquisition, variant):
    mhz = '%0.3f' % (acquisition.khz / 1e3)
    title = f'{acquisition.title} @ {mhz} MHz'

    az_plot_path = path.join(acquisition.data_dir, f'azimuth_{variant.id}.png')
    el_plot_path = path.join(acquisition.data_dir,
                             f'elevation_{variant.id}.png')

    # Pull out az/el values
    samples = acquisition.power_samples
    look_azs = [sample.look_az for sample in samples]
    look_els = [sample.look_el for sample in samples]

    # Normalize 0 dB to max measured power
    max_power = max(variant.powers)
    normalized_powers = [power - max_power for power in variant.powers]

    # Plot azimuth
    fig, ax = pyplot.subplots(subplot_kw={'projection': 'polar'})
    ax.set_theta_zero_location('N')
    ax.set_theta_direction(-1)
    ax.plot(deg2rad(look_azs), normalized_powers)
    ax.set_title(f'Azimuth – {title} - {variant.title}')
    savefig(az_plot_path)
    close(fig)

    # Plot elevation
    fig, ax = pyplot.subplots(subplot_kw={'projection': 'polar'})
    ax.plot(deg2rad(look_els), normalized_powers)
    ax.set_title(f'Elevation – {title} - {variant.title}')
    savefig(el_plot_path)
    close(fig)


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
