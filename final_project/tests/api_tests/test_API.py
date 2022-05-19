import pytest

from utils.api_client import ResponseStatusCodeException
from base import BaseApi


class TestUser(BaseApi):
    @pytest.mark.xfail(raises=ResponseStatusCodeException)
    def test_add_user(self, user_data):
        self.api_client.add_user(user_data)

    def test_delete_user(self, temp_user):
        self.api_client.delete_user(temp_user.username)

    @pytest.mark.xfail(raises=ResponseStatusCodeException)
    def test_change_password_ok(self, temp_user):
        new_password = temp_user.password[:-1:-1]
        self.api_client.change_password(temp_user.username, new_password)

    def test_change_password_fail(self, temp_user):
        with pytest.raises(ResponseStatusCodeException):
            self.api_client.change_password(temp_user.username, temp_user.password)
            pytest.fail(
                reason=f'Got 400 BAD REQUEST for URL "{self.api_client.base_url}/api/user/{temp_user.username}/change-password')


class TestApplication(BaseApi):
    def test_status(self):
        response = self.api_client.get_status()
        assert response.json()['status'] == 'ok'
