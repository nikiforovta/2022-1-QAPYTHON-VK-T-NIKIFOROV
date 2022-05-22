import random
from dataclasses import dataclass

import faker

fake = faker.Faker('ru-RU')


class Builder:

    @staticmethod
    def user(name=None, surname=None, middle_name=None, username=None, password=None, email=None):
        @dataclass
        class User:
            user_name: str = ''
            user_surname: str = ''
            user_middle_name: str = ''
            username: str = ''
            password: str = ''
            email: str = ''
            id: int = 0

        user = fake.simple_profile()

        if name is None:
            name = user['name'].split(" ")[0]
        if surname is None:
            surname = user['name'].split(" ")[1]
        if middle_name is None:
            middle_name = fake.middle_name() if random.random() >= 0.5 else ""
        if username is None:
            while len(user['username']) < 6:
                user['username'] = fake.simple_profile()['username']
            username = user['username']
        if password is None:
            password = fake.password()
        if email is None:
            email = user['mail']

        return User(user_name=name, user_surname=surname, user_middle_name=middle_name, username=username,
                    password=password,
                    email=email)
