from rtlsdr import *
from pylab import *
import matplotlib.pyplot as pyplot
import math
import os
import airbud.config as config

# Initialized in start()
sdr = None


def set_rf_gain(gain):
    sdr.gain = float(gain)


def start():
    global sdr
    print('Initializing RTL-SDR...')
    sdr = RtlSdr()

    # Configure the device
    sdr.set_direct_sampling(False)
    sdr.sample_rate = config.sdr_sample_rate
    sdr.center_freq = 14.100e6 + config.sdr_if
    sdr.gain = 0.0


def stop():
    global sdr
    print('Closing RTL-SDR...')
    sdr.close()
    sdr = None


def get_peak_power_dbfs(freq):
    nfft = config.sdr_nfft

    # Offset the center freq
    fc_offset = config.sdr_fc_offset * config.sdr_sample_rate
    rf_fc = freq + fc_offset
    if_fc = rf_fc + config.sdr_if
    sdr.center_freq = if_fc

    # Perform the acquisition
    samples = sdr.read_samples(config.sdr_averaging * nfft)

    # Remove DC component (the big spike in the middle of the spectrum)
    # by subtracting out the mean
    mean = sum(samples) / len(samples)
    samples = samples - mean

    if max([abs(s) for s in samples]) == 1:
        print('Clipping!')

    # Plot it! Note that we use `rf_fc` here to represent
    # the RF sampled BEFORE the upconverter

    fig, ax = pyplot.subplots()

    fig.set_facecolor('#00000000')
    ax.set_facecolor((17 / 255, 24 / 255, 39 / 255))  # Tailwind bg-gray-800
    for spine in ax.spines.values():
        spine.set_edgecolor('white')

    psd_result = ax.psd(samples,
                        NFFT=nfft,
                        Fs=sdr.sample_rate / 1e6,
                        Fc=rf_fc / 1e6)

    # Determine the bin where the peak power should occur
    hz_per_bin = sdr.sample_rate / nfft
    target_bin = int((nfft / 2) - fc_offset / hz_per_bin) - 1

    # Search for the peak power +/- the expected bin
    peak_bins = 8
    search_bins = psd_result[0][(
        target_bin - peak_bins):(target_bin + peak_bins)]
    peak_power = max(search_bins)
    peak_power_db = 10 * math.log10(peak_power)

    # Finish plotting it!
    ax.tick_params(colors='white')
    ax.set_ylim(-50, 30)
    ax.set_yticks([-50, -40, -30, -20, -10, 0, 10, 20, 30])
    ax.set_xlabel('Frequency (MHz)', color='white')
    ax.set_ylabel('Relative power (dB)', color='white')

    ax.plot(freq / 1e6, peak_power_db, 'r+', markersize=12)
    fig.savefig('static/images/psd_temp.png')
    close(fig)
    os.rename('static/images/psd_temp.png', 'static/images/psd.png')

    return peak_power_db
