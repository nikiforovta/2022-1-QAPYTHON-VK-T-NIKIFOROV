import pytest

from base import BaseApi
from utils.api.client import ResponseStatusCodeException


class TestUser(BaseApi):
    """User interaction via application's API"""

    @pytest.mark.xfail(raises=ResponseStatusCodeException, reason='BUG: checking wrong response code for user creation')
    def test_add_user(self, user_data):
        """
        Prerequisite: temporary user data
        Steps:
        - add temporary user
        Expected result: user added (201) """
        self.api_client.add_user(user_data)
        assert len(self.get_users(username=user_data.username)) == 1

    @pytest.mark.xfail(raises=ResponseStatusCodeException, reason='BUG: checking wrong response code for user deletion')
    def test_delete_user(self, temp_user):
        """
        Prerequisite: temporary user account
        Steps:
        - delete temporary user
        Expected result: user deleted (204) """
        self.api_client.delete_user(temp_user.username)
        assert len(self.get_users(username=temp_user.username)) == 0

    @pytest.mark.xfail(raises=ResponseStatusCodeException,
                       reason='BUG: checking wrong response code for correct password change')
    def test_change_password_ok(self, temp_user):
        """Doc: 'If successful, the user's password is changed'
        Prerequisite: temporary user account
        Steps:
        - change temporary user's password with the reversed value
        Expected result: password changed (200) """
        new_password = temp_user.password[:-1:-1]
        self.api_client.change_password(temp_user.username, new_password)
        assert self.get_users(username=temp_user.username).password == new_password

        # проверка на то, что пароль изменился?

    @pytest.mark.xfail(raises=ResponseStatusCodeException,
                       reason='BUG: checking wrong response code for incorrect password change')
    def test_change_password_fail(self, temp_user):
        """Doc: 'The new password should not match the password from the database'
        Prerequisite: temporary user account
        Steps:
        - change temporary user's password with the same value
        Expected results:   - Bad request (400) """
        self.api_client.change_password(temp_user.username, temp_user.password)
        assert self.get_users(username=temp_user.username).password == temp_user.password


class TestApplication(BaseApi):
    """Application interaction via API"""

    def test_status(self):
        """Doc: 'Indicates that the application has started and is ready to go'
        Prerequisite: running appliction
        Steps:
        - get application status
        Expected result: status OK """
        response = self.api_client.get_status()
        assert response.json()['status'] == 'ok'
