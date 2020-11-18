from micropyGPS import MicropyGPS
import os
import threading

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
    port = next(p for p in paths if 'GPS_GNSS' in p)
    
    return '/dev/serial/by-id/' + port

def gps_worker():
    """Thread to read and update GPS data."""
    path = find_gps_port()
    file = open(path, 'r')
    print(f"Opened {path}")

    while started:
        sentence = file.readline()
        gps_lock.acquire()
        for char in sentence:
            micropy_gps.update(char)
        gps_lock.release()

    file.close()
    print(f"Closed {path}")

def with_gps(fun):
    """Controls asynchronous access to GPS data."""
    if not started:
        raise Exception("GPS not started")

    gps_lock.acquire()
    result = fun(micropy_gps)
    gps_lock.release()
    return result

def start():
    """Opens serial port and starts parsing data in a background thread."""
    global started
    if started:
        return

    started = True
    gps_thread = threading.Thread(target=gps_worker)
    gps_thread.start()

def stop():
    """Closes serial port and shuts down GPS parsing thread."""
    if not started:
        return

    started = False
    gps_thread.join()

