import logging
import os
import threading

from flask import Flask, jsonify, request

import settings

app = Flask(__name__)

SURNAME_DATA = {}


@app.before_first_request
def set_log():
    for handler in app.logger.handlers:
        app.logger.removeHandler(handler)

    logdir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'logs')
    if not os.path.exists(logdir):
        os.mkdir(logdir)
    log_file = os.path.join(logdir, 'mock_request.log')
    handler = logging.FileHandler(log_file, mode='w+')
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)

    app.logger.setLevel(logging.INFO)


@app.before_request
def log_request():
    app.logger.info(f'Request Headers:\n{request.headers}')
    app.logger.info(f'Request Body:\n{request.data.decode()}\n')


@app.after_request
def log_response(response):
    app.logger.info(f'Status code: {response.status_code}')
    app.logger.info(f'Response Headers:\n{response.headers}')
    app.logger.info(f'Response Body:\n{response.response}')
    app.logger.info('______')
    return response


@app.route('/update_surname/<name>', methods=['PUT'])
def update_user_surname(name):
    old_surname = SURNAME_DATA.get(name)
    new_surname = request.json.get('surname')
    if new_surname:
        SURNAME_DATA[name] = new_surname
        return jsonify(f'Surname update for "{name}": "{old_surname}" -> "{new_surname}"'), 200
    else:
        return jsonify('New surname was not provided'), 400


@app.route('/delete_surname/<name>', methods=['DELETE'])
def delete_user_surname(name):
    try:
        removed_surname = SURNAME_DATA.pop(name)
        return jsonify(f'Surname for user "{name}" ("{removed_surname}") has been removed'), 200
    except KeyError:
        return jsonify(f'Surname for user "{name}" not found'), 404


@app.route('/get_surname/<name>', methods=['GET'])
def get_user_surname(name):
    surname = SURNAME_DATA.get(name)
    if surname:
        return jsonify(surname), 200
    else:
        return jsonify(f'Surname for user "{name}" not found'), 404


def shutdown_stub():
    terminate_func = request.environ.get('werkzeug.server.shutdown')
    if terminate_func:
        terminate_func()


@app.route('/shutdown', methods=['GET'])
def shutdown():
    shutdown_stub()
    return jsonify('Ok, exiting'), 200


def run_mock():
    server = threading.Thread(target=app.run, kwargs={
        'host': settings.MOCK_HOST,
        'port': settings.MOCK_PORT
    })

    server.start()
    return server
