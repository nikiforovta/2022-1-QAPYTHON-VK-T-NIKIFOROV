import pytest
import requests
from faker import Faker

import settings
from client.socket_client import SocketClient


@pytest.fixture(scope='function')
def socket_client():
    sc = SocketClient()
    yield sc
    sc.close()


@pytest.fixture(scope='function')
def test_user():
    username = Faker().first_name()
    yield username
    url = f'http://{settings.APP_HOST}:{settings.APP_PORT}'
    requests.delete(f'{url}/delete_user', json={'name': username})
