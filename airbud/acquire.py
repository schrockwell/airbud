import time
import threading

import airbud.rf
import airbud.gps
import airbud.plots
import airbud.config as config

from airbud.gps.position import Position
from airbud.acquisition import Acquisition

# Acquisition state
acquisition = Acquisition()
acquisition_thread = None


@airbud.gps.with_gps
def gps_position(micropy_gps):
    """Returns the latest Position."""
    return Position(micropy_gps)


def gps_state():
    """Returns a dict payload for the latest GPS position and related fields."""
    position = gps_position()
    look_az, look_el, look_range = acquisition.look_angles(position)

    return {
        **position.to_dict(),
        'look_az': look_az,
        'look_el': look_el,
        'look_range': look_range,
    }


def rf_state():
    """Returns a dict payload of the latest SDR state."""
    return {
        'dbfs': airbud.rf.get_latest_power(),
        'khz': airbud.rf.khz
    }


def acquisition_thread_worker():
    """Background worker for appending samples to the current acquisition."""
    while not acquisition.completed:
        time.sleep(config.poll_interval)

        # This is fast since all the values are already in-memory
        acquisition.add_sample(gps_position(), airbud.rf.get_latest_power())


def update_conditions(params):
    """Updates acquisition conditions from web params."""
    acquisition.conditions = params

    if 'khz' in params:
        airbud.rf.tune(params['khz'])

    if 'rf_gain' in params:
        airbud.rf.set_rf_gain(params['rf_gain'])


def get_conditions():
    """Returns a dict payload of the current acquisition conditions."""
    return acquisition.conditions


def start():
    """Starts the currently-configured acquisition."""
    global acquisition_thread

    acquisition.start()

    acquisition_thread = threading.Thread(target=acquisition_thread_worker)
    acquisition_thread.start()


def stop():
    """Stops the current acquisition, then clones it to create the next acquisition."""
    global acquisition
    global acquisition_thread

    acquisition.stop()
    acquisition_thread.join()

    airbud.plots.generate(acquisition)

    acquisition_thread = None
    acquisition = acquisition.clone()
