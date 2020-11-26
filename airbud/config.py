#
# RTL-SDR
#
sdr_enabled = True

# Sample rate
sdr_sample_rate = 0.240e6

# Number of samples per period
sdr_nfft = 1024

# The number of periods to sample for
sdr_averaging = 64

# Move the Fc away from the target frequency by this percentage
sdr_fc_offset = 0  # -1/4

# When using an upconverter (e.g. Ham It Up), all the frequencies
# are offset by this amount
sdr_if = 125e6

# RF gain (these values are dBs in tenths, so e.g. for 37 specify gain of 3.7)
# [0, 9, 14, 27, 37, 77, 87, 125, 144, 157, 166, 197, 207, 229, 254, 280, 297, 328, 338, 364, 372, 386, 402, 421, 434, 439, 445, 480, 496]
sdr_gain = 3.7

#
# GPS
#
gps_enabled = True

# Look for a serial device with this identifier in it somewhere
gps_substring = 'GPS_GNSS'
