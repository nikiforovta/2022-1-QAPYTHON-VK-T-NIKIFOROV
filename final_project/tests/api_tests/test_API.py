import pytest

from base import BaseApi
from utils.api.client import ResponseStatusCodeException


class TestUser(BaseApi):
    """User interaction via application's API"""

    @pytest.mark.xfail(raises=ResponseStatusCodeException, reason='BUG: checking wrong response code for user creation')
    def test_add_user(self, user_data):
        """
        Prerequisite:
        - temporary user data

        Steps:
        1. Add temporary user

        Expected result:
        - user added (201) """
        self.api_client.add_user(user_data)
        assert len(self.get_user(username=user_data.username)) == 1

    @pytest.mark.xfail(raises=ResponseStatusCodeException,
                       reason='FLAKY: checking wrong response code for user deletion')
    def test_delete_user(self, temp_user):
        """
        Prerequisite:
        - temporary user account

        Steps:
        1. Delete temporary user

        Expected result:
        - user deleted (204) """
        self.api_client.delete_user(temp_user.username)
        assert self.get_user(username=temp_user.username) is None

    @pytest.mark.xfail(raises=ResponseStatusCodeException,
                       reason='BUG: checking wrong response code for correct password change')
    def test_change_password_ok(self, temp_user):
        """Doc:
        'If successful, the user's password is changed'

        Prerequisite:
        - temporary user account

        Steps:
        1. Change temporary user's password with the reversed value

        Expected result:
        - password changed (200) """
        new_password = temp_user.password[:-1:-1]
        self.api_client.change_password(temp_user.username, new_password)
        assert self.get_user(username=temp_user.username).password == new_password

    @pytest.mark.xfail(raises=ResponseStatusCodeException,
                       reason='OK: checking correct response code for incorrect password change')
    def test_change_password_fail(self, temp_user):
        """Doc:
        'New password should not match the password from the database'

        Prerequisite:
        - temporary user account

        Steps:
        1. Change temporary user's password with the same value

        Expected result:
        - bad request (400) """
        self.api_client.change_password(temp_user.username, temp_user.password)
        assert self.get_user(username=temp_user.username).password == temp_user.password

    def test_block_user_ok(self, temp_user):
        """Doc:
        'If successful, the user is assigned access = 0 in the database'

        Prerequisite:
        - temporary user account

        Steps:
        1. Block temporary user

        Expected results:
        - OK (200)
        - user.access == 0"""
        self.api_client.block_user(temp_user.username)
        assert self.get_user(username=temp_user.username).access == 0

    @pytest.mark.xfail(raises=ResponseStatusCodeException,
                       reason='OK: checking correct response code for incorrect user block')
    def test_block_blocked_user(self, temp_user):
        """
        Prerequisite:
        - blocked temporary user account

        Steps:
        1. Block blocked temporary user

        Expected results:
        - OK (200)
        - user.access == 0"""
        self.api_client.block_user(temp_user.username)
        self.api_client.block_user(temp_user.username)
        assert self.get_user(username=temp_user.username).access == 0

    @pytest.mark.xfail(raises=ResponseStatusCodeException,
                       reason="OK: checking correct response code for incorrect user block")
    def test_block_non_existing_user(self, user_data):
        """
        Prerequisite:
        - temporary user data

        Steps:
        1. Block non-existing user

        Expected result:
        - not found (404) """
        self.api_client.block_user(user_data.username)

    def test_accept_user_ok(self, temp_user):
        """Doc:
        'If successful, the user is assigned access = 1 in the database'

        Prerequisite:
        - blocked temporary user account

        Steps:
        1. Accept temporary user

        Expected results:
        - OK (200)
        - user.access == 1"""
        self.api_client.block_user(temp_user.username)
        self.api_client.accept_user(temp_user.username)
        assert self.get_user(username=temp_user.username).access == 1

    @pytest.mark.xfail(raises=ResponseStatusCodeException,
                       reason='OK: checking correct response code for incorrect user accept')
    def test_accept_accepted_user(self, temp_user):
        """
        Prerequisite:
        - temporary user account

        Steps:
        1. Accept temporary user

        Expected results:
        - bad request (400)
        - user.access == 1"""
        self.api_client.accept_user(temp_user.username)
        assert self.get_user(username=temp_user.username).access == 1

    @pytest.mark.xfail(raises=ResponseStatusCodeException,
                       reason="OK: checking correct response code for incorrect user accept")
    def test_accept_non_existing_user(self, user_data):
        """
        Prerequisite:
        - temporary user data

        Steps:
        1. Accept non-existing user

        Expected result:
        - not found (404) """
        self.api_client.accept_user(user_data.username)


class TestApplication(BaseApi):
    """Application interaction via API"""

    def test_status(self):
        """Doc:
        'Indicates that the application has started and is ready to go'

        Prerequisite:
        - running application

        Steps:
        1. Get application status

        Expected results:
        - OK (200)
        - status OK """
        response = self.api_client.get_status()
        assert response.json()['status'] == 'ok'
