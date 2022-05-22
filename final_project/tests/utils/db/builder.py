import json
import sys

from models import UsersModel

sys.path.append('../..')

from utils import user_builder


class MysqlBuilder:
    def __init__(self, client):
        self.client = client
        self.builder = user_builder.Builder()

    def add_test_user(self):
        with open('../../test_user_data.json') as file:
            user_data = json.load(file)
            self.client.session.add(
                UsersModel(name=user_data['name'], surname=user_data['surname'], username=user_data['username'],
                           password=user_data['password'], email=user_data['email'], access=1, active=0))
            self.client.session.commit()

    def add_random_users(self, quantity=10):
        for _ in range(quantity):
            user_data = self.builder.user()
            self.client.session.add(
                UsersModel(name=user_data.user_name, surname=user_data.user_surname,
                           middle_name=user_data.middle_name,
                           username=user_data.username, password=user_data.password, email=user_data.email,
                           access=1,
                           active=0))
