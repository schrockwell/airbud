import flask
from flask import jsonify, request, send_from_directory
import airbud.gps
import airbud.rf
from airbud.gps.position import Position
from airbud.acquisition import Acquisition

# Flask application
app = flask.Flask(
    __name__,
    static_url_path='/static',
    static_folder='../../static'
)
app.config["DEBUG"] = True

# Application state
acquisition = Acquisition()
hw_state = {}


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

    if request.json['khz']:
        airbud.rf.tune(request.json['khz'])

    return status()


@app.route('/api/start', methods=['POST'])
def start_acquisition():
    acquisition.start()
    return ''


@app.route('/api/stop', methods=['POST'])
def stop_acquisition():
    global acquisition
    prev_conditions = acquisition.conditions
    acquisition.stop()

    acquisition = Acquisition(conditions=prev_conditions)
    return ''


@airbud.gps.with_gps
def gps_state(micropy_gps):
    position = Position(micropy_gps)
    return position.to_dict()


def rf_state():
    return {
        'dbfs': airbud.rf.get_latest_power(),
        'khz': airbud.rf.khz
    }


def start():
    app.run(use_reloader=False)
