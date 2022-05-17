import os

from flask import Flask, jsonify, request

app = Flask(__name__)

USER_ID = {}


@app.route('/vk_id/<username>', methods=['GET'])
def get_user_id(username):
    if username in USER_ID.keys():
        vk_id = USER_ID[username]
        return jsonify({'vk_id': vk_id}), 200
    else:
        return jsonify(), 404


@app.route('/vk_id/<username>', methods=['POST'])
def add_user_id(username):
    if username in USER_ID.keys():
        return jsonify('ID already exists'), 400
    else:
        USER_ID[username] = request.json['id']
        return jsonify("Successful"), 200


if __name__ == '__main__':
    host, port = os.environ.get('VK_URL', '127.0.0.1:8543').split(":")
    app.run(host, port)
