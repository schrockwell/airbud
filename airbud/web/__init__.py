import flask
from flask import jsonify, request, send_from_directory
import airbud.gps
import airbud.rf
import airbud.plots
import airbud.config as config
from airbud.gps.position import Position
from airbud.acquisition import Acquisition
import threading
import time
# Flask application
app = flask.Flask(
    __name__,
    static_url_path='',
    static_folder='../../static'
)
app.config['DEBUG'] = True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

# Application state
acquisition = Acquisition()
acquisition_thread = None


def acquisition_thread_worker():
    while not acquisition.completed:
        time.sleep(config.poll_interval)

        # This is fast since all the values are already in-memory
        acquisition.add_sample(gps_position(), airbud.rf.get_latest_power())


@app.route('/', methods=['GET'])
def root():
    return app.send_static_file('index.html')


@app.route('/api/status', methods=['GET'])
def status():
    return jsonify({
        'gps': gps_state(),
        'rf': rf_state(),
        'conditions': acquisition.conditions
    })


@app.route('/api/conditions', methods=['POST'])
def update_conditions():
    acquisition.conditions = request.json

    if 'khz' in request.json:
        airbud.rf.tune(request.json['khz'])

    if 'rf_gain' in request.json:
        airbud.rf.set_rf_gain(request.json['rf_gain'])

    return status()


@app.route('/api/start', methods=['POST'])
def start_acquisition():
    global acquisition_thread

    acquisition.start()

    acquisition_thread = threading.Thread(target=acquisition_thread_worker)
    acquisition_thread.start()

    return status()


@app.route('/api/stop', methods=['POST'])
def stop_acquisition():
    global acquisition
    global acquisition_thread

    acquisition.stop()
    acquisition_thread.join()

    # airbud.plots.generate(acquisition)

    acquisition_thread = None
    acquisition = acquisition.clone()
    return status()


def gps_state():
    position = gps_position()
    look_az, look_el, look_range = acquisition.look_angles(position)

    return {
        **position.to_dict(),
        'look_az': look_az,
        'look_el': look_el,
        'look_range': look_range,
    }


@airbud.gps.with_gps
def gps_position(micropy_gps):
    return Position(micropy_gps)


def rf_state():
    return {
        'dbfs': airbud.rf.get_latest_power(),
        'khz': airbud.rf.khz
    }


def start():
    app.run(use_reloader=False)
