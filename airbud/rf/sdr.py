from rtlsdr import *
from pylab import *
import math
import os

# Initialized in start()
sdr = None

# Constant sample rate
sample_rate = 0.240e6

# Make sure Fc is away from the desired frequency to measure,
# to avoid the DC spike
fc_offset = -(sample_rate / 4)

# Number of sample periods per acquisition
averaging = 64

# The range of bins to search for peak power
peak_bins = 8


def start():
    global sdr
    print('Initializing RTL-SDR...')
    sdr = RtlSdr()

    # Required for HF reception – see http://radio-quaderno.blogspot.com/2019/10/fixing-problem-with-hf-reception-on.html
    sdr.set_direct_sampling('q')

    # Configure the device
    sdr.sample_rate = sample_rate
    sdr.center_freq = 14.020e6
    sdr.gain = 49.6


def stop():
    global sdr
    print('Closing RTL-SDR...')
    sdr.close()
    sdr = None


def get_peak_power_dbfs(freq, nfft=1024):
    # Offset the center freq
    sdr.center_freq = freq + fc_offset

    # Perform the acquisition
    samples = sdr.read_samples(averaging * nfft)

    # Remove DC component by subtracting out the mean
    mean = sum(samples) / len(samples)
    samples = samples - mean

    # Plot it!
    clf()
    psd_result = psd(samples, NFFT=1024, Fs=sdr.sample_rate /
                     1e6, Fc=sdr.center_freq/1e6)

    # Determine the bin where the peak power should occur
    hz_per_bin = sdr.sample_rate / nfft
    target_bin = int((nfft / 2) - fc_offset / hz_per_bin) - 1

    # Search for the peak power +/- the expected bin
    search_bins = psd_result[0][(
        target_bin - peak_bins):(target_bin + peak_bins)]
    peak_power = max(search_bins)
    peak_power_db = 10 * math.log10(peak_power)

    # Finish plotting it!
    ylim(-60, 0)
    yticks([-60, -50, -40, -30, -20, -10, 0])
    xlabel('Frequency (MHz)')
    ylabel('Relative power (dB)')

    plot(freq / 1e6, peak_power_db, 'r+', markersize=12)
    savefig('static/psd_temp.png')
    os.rename('static/psd_temp.png', 'static/psd.png')

    return peak_power_db
