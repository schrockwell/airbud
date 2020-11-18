import time

import airbud.gps as gps
from airbud.gps import with_gps
from airbud.gps.position import Position

gps.start()


@with_gps
def get_position(gps):
    position = Position(gps)
    return position


# For testing
while True:
    try:
        position = get_position()
        print((position.latitude, position.longitude))
        time.sleep(1.0)
    except KeyboardInterrupt:
        gps.stop()
        break
