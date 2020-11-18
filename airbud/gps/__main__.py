import time

import airbud.gps as gps
from airbud.gps.position import Position

gps.start()

# For testing
while True:
    try:
        position = gps.with_gps(lambda gps: Position(gps))
        print((position.latitude, position.longitude))
        time.sleep(1.0)
    except KeyboardInterrupt:
        gps.stop()
        break
