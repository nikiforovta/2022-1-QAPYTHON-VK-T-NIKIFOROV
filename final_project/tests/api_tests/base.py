import allure
import pytest

from utils.api.client import ResponseStatusCodeException
from utils.db.models import UsersModel
from utils.user_builder import Builder


class BaseApi:
    @pytest.fixture(scope='function', autouse=True)
    def setup(self, api_client, mysql_client):
        self.api_client = api_client
        self.db_client = mysql_client
        self.builder = Builder()

    @pytest.fixture(scope='function')
    def user_data(self):
        yield self.builder.user()

    @allure.step("Create temporary user with data: {1}")
    @pytest.fixture(scope='function')
    def temp_user(self, user_data):
        self.api_client.add_user_workaround(user_data)
        yield user_data
        try:
            self.api_client.delete_user(user_data.username)
        except ResponseStatusCodeException as e:
            if str(e).split(" ")[1] != '404':
                raise e

    def get_user(self, **filters):
        self.db_client.session.commit()
        res = self.db_client.session.query(UsersModel).filter_by(**filters)
        return res.first()
