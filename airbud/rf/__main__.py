import airbud.rf.sdr as sdr
import time

while True:
    print(sdr.get_peak_power_dbfs(14.020e6))
