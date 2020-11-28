"""Flask web application server (duh)."""

from flask import Flask, jsonify, request, send_from_directory
import airbud.acquire as acquire


# Flask application
app = Flask(
    __name__,
    static_url_path='',
    static_folder='../static'
)
app.config['DEBUG'] = True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


@app.route('/', methods=['GET'])
def root():
    return app.send_static_file('index.html')


@app.route('/api/status', methods=['GET'])
def status():
    return jsonify({
        'gps': acquire.gps_state(),
        'rf': acquire.rf_state(),
        'conditions': acquire.get_conditions()
    })


@app.route('/api/conditions', methods=['POST'])
def update_conditions():
    acquire.update_conditions(request.json)
    return status()


@app.route('/api/start', methods=['POST'])
def start_acquisition():
    acquire.start()
    return status()


@app.route('/api/stop', methods=['POST'])
def stop_acquisition():
    acquire.stop()
    return status()


def start():
    app.run(use_reloader=False, host='0.0.0.0')
