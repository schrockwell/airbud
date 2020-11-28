"""Wraps up GPS access."""

from micropyGPS import MicropyGPS
import os
import threading
import airbud.config as config

micropy_gps = MicropyGPS(location_formatting='dd')
gps_thread = None
gps_lock = threading.Lock()
started = False


def find_gps_port():
    """Returns the path to the NMEA serial port.

    Raises if it cannot be found.

    Example: "/dev/serial/by-id/usb-u-blox_AG_-_www.u-blox.com_u-blox_7_-_GPS_GNSS_Receiver-if00"
    """

    paths = os.listdir('/dev/serial/by-id')
    port = next(p for p in paths if config.gps_substring in p)

    return '/dev/serial/by-id/' + port


def gps_worker():
    """Thread to read and update GPS data."""
    path = find_gps_port()
    file = open(path, 'r')
    print(f'Opened {path}')

    while started:
        sentence = file.readline()
        with gps_lock:
            for char in sentence:
                micropy_gps.update(char)

    file.close()
    print(f'Closed {path}')


def with_gps(func):
    """Decorator that controls asynchronous access to GPS data."""
    def with_gps_wrapper():
        if config.gps_enabled and not started:
            raise Exception("GPS not started")

        with gps_lock:
            result = func(micropy_gps)

        return result

    return with_gps_wrapper


def start():
    """Opens serial port and starts parsing data in a background thread."""
    global started
    global gps_thread
    if started:
        return

    if not config.gps_enabled:
        print('*** GPS is disabled in the config ***')
        return

    started = True
    gps_thread = threading.Thread(target=gps_worker)
    gps_thread.start()


def stop():
    """Closes serial port and shuts down GPS parsing thread."""
    global started
    if not started:
        return

    started = False
    gps_thread.join()
