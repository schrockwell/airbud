import airbud.config as config
import airbud.rf.sdr as sdr
import threading
import time

sdr_thread = None
khz = 14313
power = 0.0
started = False


def tune(new_khz):
    global khz
    khz = new_khz


def start():
    global started
    global sdr_thread

    if started:
        return

    if not config.sdr_enabled:
        print('*** SDR is disabled in the config ***')
        return

    sdr_thread = threading.Thread(target=sdr_worker)
    sdr_thread.start()

    started = True


def stop():
    global started
    global sdr_thread

    if started:
        started = False
        sdr_thread.join()
        sdr_thread = None


def get_latest_power():
    return power


def sdr_worker():
    """Thread to read latest peak power from SDR."""
    global power
    global khz
    sdr.start()

    while started:
        start_time = time.time()

        # This is slow
        power = sdr.get_peak_power_dbfs(khz * 1e3)

        # Update once per second if possible
        duration = time.time() - start_time
        if duration < 1.0:
            time.sleep(1.0 - duration)

    sdr.stop()
