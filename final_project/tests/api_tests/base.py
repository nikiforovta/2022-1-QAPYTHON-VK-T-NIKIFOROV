import pytest

from utils.api.client import ResponseStatusCodeException
from utils.user_builder import Builder


class BaseApi:
    @pytest.fixture(scope='function', autouse=True)
    def setup(self, api_client):
        self.api_client = api_client
        self.builder = Builder()

    @pytest.fixture(scope='function')
    def user_data(self):
        yield self.builder.user()

    @pytest.fixture(scope='function')
    def temp_user(self, user_data):
        self.api_client.add_user_workaround(user_data)
        yield user_data
        try:
            self.api_client.delete_user(user_data.username)
        except ResponseStatusCodeException as e:
            if str(e).split(" ")[1] != '404':
                raise e
