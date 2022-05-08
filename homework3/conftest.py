import json

import pytest

from api.client import TargetApiClient
from api.fixtures import *


def pytest_addoption(parser):
    parser.addoption('--url', default='https://target.my.com')


@pytest.fixture(scope='session')
def repo_root():
    return os.path.abspath(os.path.join(__file__, os.path.pardir))


@pytest.fixture(scope='session')
def config(request):
    return {'url': request.config.getoption('--url')}


@pytest.fixture(scope='session')
def credentials():
    with open(os.path.join(os.path.dirname(__file__), 'credentials.json')) as credentials:
        credentials_json = json.load(credentials)
        user = credentials_json['EMAIL']
        password = credentials_json['PASSWORD']

    return user, password


@pytest.fixture(scope="function")
def api_client(credentials) -> TargetApiClient:
    api_client = TargetApiClient(credentials)
    return api_client
