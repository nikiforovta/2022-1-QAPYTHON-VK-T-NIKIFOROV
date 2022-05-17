import json

import pytest

from api.client import TMApiClient
from api.fixtures import *


def pytest_addoption(parser):
    parser.addoption('--url', default='https://127.0.0.1:8081')


@pytest.fixture(scope='session')
def repo_root():
    return os.path.abspath(os.path.join(__file__, os.path.pardir))


@pytest.fixture(scope='session')
def config(request):
    return {'url': request.config.getoption('--url')}


@pytest.fixture(scope='session')
def credentials():
    with open(os.path.join(os.path.dirname(__file__), '../test_user_data.json')) as creds:
        return json.load(creds)


@pytest.fixture(scope="function")
def api_client(credentials) -> TMApiClient:
    api_client = TMApiClient(credentials)
    return api_client
