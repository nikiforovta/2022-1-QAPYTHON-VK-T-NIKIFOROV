from urllib.parse import urljoin

import requests

from utils.api import paths


class ResponseStatusCodeException(Exception):
    pass


class TMApiClient:

    def __init__(self, credentials):
        self.base_url = 'http://myapp:8081'
        self.session = requests.Session()
        self.login(credentials)

    def _request(self, method, url, headers=None, data=None, expected_status=200, params=None, json_data=None):
        response = self.session.request(method=method, url=url, headers=headers, data=data, params=params,
                                        json=json_data)
        if response.status_code != expected_status:
            raise ResponseStatusCodeException(f'Got {response.status_code} {response.reason} for URL "{url}"')
        return response

    def login(self, credentials):
        path = paths.User.login
        data = credentials
        self._request(method="POST", url=urljoin(self.base_url, path), data=data)

    def add_user(self, user_data):
        path = paths.User.add_user
        data = {"name": user_data.user_name,
                "surname": user_data.user_surname,
                "username": user_data.username,
                "middle_name": user_data.user_middle_name,
                "password": user_data.password,
                "email": user_data.email}
        return self._request(method='POST', url=urljoin(self.base_url, path), json_data=data,
                             expected_status=201)

    def add_user_workaround(self, user_data):
        data = {"name": user_data.user_name,
                "surname": user_data.user_surname,
                "username": user_data.username,
                "middle_name": user_data.user_middle_name,
                "password": user_data.password,
                "email": user_data.email}
        path = paths.User.add_user
        return self._request(method='POST', url=urljoin(self.base_url, path), json_data=data,
                             expected_status=210)

    def delete_user(self, username):
        path = paths.User.delete_user(username)
        self._request(method='DELETE', url=urljoin(self.base_url, path), expected_status=204)

    def change_password(self, username, password):
        path = paths.User.change_password(username)
        data = {'password': password}
        self._request(method='PUT', url=urljoin(self.base_url, path), json_data=data, expected_status=200)

    def block_user(self, username):
        path = paths.User.block(username)
        self._request(method='POST', url=urljoin(self.base_url, path), expected_status=200)

    def accept_user(self, username):
        path = paths.User.accept(username)
        self._request(method='POST', url=urljoin(self.base_url, path), expected_status=200)

    def get_status(self):
        path = paths.Application.status
        return self._request(method='GET', url=urljoin(self.base_url, path), expected_status=200)
