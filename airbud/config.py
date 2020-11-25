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
sdr_fc_offset = -1/4

# When using an upconverter (e.g. Ham It Up), all the frequencies
# are offset by this amount
sdr_if = 125e6

# RF gain (there is a list of supported values for each SDR)
sdr_gain = 49.6

#
# GPS
#
gps_enabled = True

# Look for a serial device with this identifier in it somewhere
gps_substring = 'GPS_GNSS'
