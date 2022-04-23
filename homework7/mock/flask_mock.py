import threading

from flask import Flask, jsonify, request

import settings

app = Flask(__name__)

SURNAME_DATA = {}


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
    return jsonify(f'Ok, exiting'), 200


def run_mock():
    server = threading.Thread(target=app.run, kwargs={
        'host': settings.MOCK_HOST,
        'port': settings.MOCK_PORT
    })

    server.start()
    return server
