import logging
import os

import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

app_data = {}
user_id_seq = 1


@app.before_first_request
def set_log():
    for handler in app.logger.handlers:
        app.logger.removeHandler(handler)

    logdir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'logs')
    if not os.path.exists(logdir):
        os.mkdir(logdir)
    log_file = os.path.join(logdir, 'request.log')
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


@app.route('/add_user', methods=['POST'])
def create_user():
    global user_id_seq

    user_name = request.json['name']
    if user_name not in app_data:
        app_data[user_name] = user_id_seq
        user_id_seq += 1
        return jsonify({'user_id': app_data[user_name]}), 201

    else:
        return jsonify(f'User_name {user_name} already exists with id {app_data[user_name]}'), 400


@app.route('/delete_user', methods=['DELETE'])
def delete_user():
    user_name = request.json['name']
    if user_name not in app_data:
        return jsonify(f'User {user_name} not found'), 404
    else:
        app_data.pop(user_name)
        return jsonify(f'User {user_name} has been removed'), 200


@app.route('/update_surname/<name>', methods=['PUT'])
def update_surname(name):
    surname_host = os.environ['SURNAME_HOST']
    surname_port = os.environ['SURNAME_PORT']
    resp = requests.put(f'http://{surname_host}:{surname_port}/update_surname/{name}', json=request.get_json())
    return jsonify(resp.content.decode()), resp.status_code


@app.route('/delete_surname/<name>', methods=['DELETE'])
def delete_surname(name):
    surname_host = os.environ['SURNAME_HOST']
    surname_port = os.environ['SURNAME_PORT']
    resp = requests.delete(f'http://{surname_host}:{surname_port}/delete_surname/{name}')
    return jsonify(resp.content.decode()), resp.status_code


@app.route('/get_user/<name>', methods=['GET'])
def get_user_id_by_name(name):
    user_id = app_data.get(name)
    if user_id:
        age_host = os.environ['AGE_HOST']
        age_port = os.environ['AGE_PORT']

        # get age from external system 1
        age = None
        try:
            age = requests.get(f'http://{age_host}:{age_port}/get_age/{name}').json()
        except Exception as e:
            print(f'Unable to get age from external system 1:\n{e}')

        # get surname from external system 2
        surname_host = os.environ['SURNAME_HOST']
        surname_port = os.environ['SURNAME_PORT']

        surname = None
        try:
            response = requests.get(f'http://{surname_host}:{surname_port}/get_surname/{name}')
            if response.status_code == 200:
                surname = response.json()
            else:
                print(f'No surname found for user {name}')
        except Exception as e:
            print(f'Unable to get surname from external system 2:\n{e}')

        data = {'user_id': user_id,
                'age': age,
                'surname': surname
                }
        return jsonify(data), 200
    else:
        return jsonify(f'User_name {name} not found'), 404


if __name__ == '__main__':
    host = os.environ.get('APP_HOST', '127.0.0.1')
    port = os.environ.get('APP_PORT', '4444')

    app.run(host, port)
