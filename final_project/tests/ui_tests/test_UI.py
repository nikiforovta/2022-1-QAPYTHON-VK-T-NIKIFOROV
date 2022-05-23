import dataclasses

import pytest
from selenium.common.exceptions import TimeoutException

from base import BaseCase


class TestRegistration(BaseCase):
    """Registration tests"""

    @pytest.mark.UI
    def test_positive_registration(self, temp_user):
        """
        Testing normal registration process with all user data provided

        Prerequisite:
        - temporary user account

        Steps:
        1. Login

        Expected result:
        - correct username at the main page"""
        assert temp_user.username == self.main_page.get_username()

    @pytest.mark.UI
    def test_negative_registration_already_exists(self, temp_user):
        """
        An attempt to create already existing user profile

        Prerequisite:
        - temporary user account

        Steps:
        1. Logout
        2. Register with temporary user data

        Expected result:
        - registration failed with error message"""
        self.main_page.logout()
        self.register(dataclasses.asdict(temp_user))
        assert self.login_page.get_flash_text() == "User already exist"

    @pytest.mark.UI
    @pytest.mark.parametrize("no_username,no_email,no_firstname,no_password,no_checkbox",
                             [
                                 (1, 0, 0, 0, 0),
                                 (0, 1, 0, 0, 0),
                                 (0, 0, 1, 0, 0),
                                 (0, 0, 0, 1, 0),
                                 (0, 0, 0, 0, 1),
                             ],
                             ids=[
                                 "Missing username",
                                 "Missing email",
                                 "Missing first name",
                                 "Missing password",
                                 "Missing checkbox"
                             ])
    def test_negative_registration_missing_fields(self, no_username, no_firstname, no_email, no_password, no_checkbox):
        """
        An attempt to create user profile missing some user data

        Prerequisite:
        - temporary user data with missing field

        Steps:
        1. Login with the given credentials

        Expected result:
        - login failed with error message"""
        user = self.builder.user()
        if no_firstname:
            user.user_name = ""
            self.register(dataclasses.asdict(user))
            assert self.registration_page.find_validation_message(
                self.registration_page.locators.FORM_INPUT_LOCATOR("user_name")) != ""
        elif no_username:
            user.username = ""
            self.register(dataclasses.asdict(user))
            assert self.registration_page.find_validation_message(
                self.registration_page.locators.FORM_INPUT_LOCATOR("username")) != ""
        elif no_email:
            user.email = ""
            self.register(dataclasses.asdict(user))
            assert self.registration_page.get_flash_text() == "Incorrect email length"
            # assert self.registration_page.find_validation_message(
            #     self.registration_page.locators.FORM_INPUT_LOCATOR("email")) != ""
        elif no_password:
            user.password = ""
            self.register(dataclasses.asdict(user))
            assert self.registration_page.find_validation_message(
                self.registration_page.locators.FORM_INPUT_LOCATOR("password")) != ""
        elif no_checkbox:
            self.register(dataclasses.asdict(user), False)
            assert self.registration_page.find_validation_message(
                self.registration_page.locators.FORM_INPUT_LOCATOR("term")) != ""


class TestLogin(BaseCase):
    """Authorization tests"""

    @pytest.mark.UI
    @pytest.mark.parametrize(
        'credentials',
        [
            pytest.param(('log in', 'password')),
            pytest.param((None, 'password')),
        ],
        ids=[
            'Wrong username',
            'Wrong password'
        ]
    )
    def test_negative_login(self, credentials):
        """
        Negative authorization test

        Prerequisite:
        - incorrect user credentials

        Steps:
        1. Login with the given credentials

        Expected result:
        - login failed with error message"""
        if not credentials[0]:
            credentials = (self.form_data['username'], credentials[-1])
        self.login_page.login(credentials)
        if credentials[0] == self.form_data['username']:
            assert self.login_page.get_flash_text() != ""
        else:
            assert self.login_page.get_flash_text() == "Invalid username or password"

    @pytest.mark.UI
    def test_login_blocked(self, temp_user):
        """
        Blocked user cannot login

        Prerequisite:
        - temporary user account

        Steps:
        1. Block temporary user via API
        2. Login with temporary user credentials

        Expected result:
        - Warning message about blocked user account"""
        self.main_page.logout()
        self.api_client.block_user(temp_user.username)
        self.login_page.login(credentials=(temp_user.username, temp_user.password))
        assert self.login_page.get_flash_text() != ""

    @pytest.mark.UI
    def test_successful_login(self, login):
        """
        Positive authorization test

        Prerequisite:
        - test user account

        Steps:
        1. Login test user

        Expected result:
        - main page displayed
        """
        assert self.main_page.find(self.main_page.locators.LOGOUT_LOCATOR).is_displayed()


class TestMainPage(BaseCase):
    """Tests for main page"""

    @pytest.mark.UI
    @pytest.mark.parametrize("item,result_url", [(1, "https://en.wikipedia.org/wiki/API"),
                                                 (2,
                                                  "https://www.popularmechanics.com/technology/infrastructure"
                                                  "/a29666802/future-of-the-internet/"),
                                                 (3, "https://ru.wikipedia.org/wiki/SMTP")],
                             ids=['What is an API?', 'Future of internet', 'Lets talk about SMTP?'])
    def test_center_content(self, item, result_url, login):
        """
        Doc:
        'All links must contain information about resources and work properly'

        Prerequisite:
        - test user account

        Steps:
        1. Login test user

        Expected result:
        - correct links found at the page's center"""
        self.main_page.click(self.main_page.locators.CENTER_CONTENT_LOCATOR(item))
        self.driver.switch_to.window(self.driver.window_handles[-1])
        assert self.driver.current_url == result_url

    @pytest.mark.UI
    @pytest.mark.parametrize("item,result_url", [pytest.param([1, 1], "http://myapp:8081/welcome/"),
                                                 pytest.param([2, 1], "https://www.python.org/"),
                                                 pytest.param([2, 2],
                                                              "https://en.wikipedia.org/wiki/History_of_Python"),
                                                 pytest.param([2, 3], "https://flask.palletsprojects.com/en/1.1.x/#"),
                                                 pytest.param([3, 1], "https://www.kernel.org/",
                                                              marks=pytest.mark.xfail(
                                                                  reason='MINOR BUG: incorrect URL')),
                                                 pytest.param([3, 2], "https://www.centos.org/download/",
                                                              marks=pytest.mark.xfail(
                                                                  reason='MINOR BUG: incorrect URL')),
                                                 pytest.param([4, 1], "https://en.wikipedia.org/wiki/Computer_network",
                                                              marks=pytest.mark.xfail(
                                                                  reason='MINOR BUG: incorrect URL')),
                                                 pytest.param([4, 2], "https://www.wireshark.org/news/"),
                                                 pytest.param([4, 3], "https://www.wireshark.org/#download"),
                                                 pytest.param([4, 4], "https://hackertarget.com/tcpdump-examples/")],
                             ids=['HOME', 'Python', 'Python history', 'About Flask', 'Linux', 'Download Centos7',
                                  'Network', 'WIRESHARK - NEWS', 'WIRESHARK - DOWNLOAD', 'TCPDUMP - EXAMPLES'])
    def test_navigation_bar(self, item, result_url, login):
        """
        Doc:
        'All links must contain information about resources and work properly'

        Prerequisite:
        - test user account

        Steps:
        1. Login test user

        Expected result:
        - correct links found at the navigation bar"""
        self.main_page.click_dropdown(*item)
        self.driver.switch_to.window(self.driver.window_handles[-1])
        assert self.driver.current_url == result_url

    @pytest.mark.UI
    def test_random_fact(self, login):
        """
        Doc: 'A random motivational fact about Python is displayed at the bottom of the page'

        Prerequisite: test user account

        Steps:
        1. Login test user

        Expected result: text found at the page's footer """
        assert self.main_page.find(self.main_page.locators.RANDOM_FACT_LOCATOR).is_enabled()

    @pytest.mark.UI
    def test_logout(self, login):
        """
        Doc:
        'Logout button should successfully log out the user'

        Prerequisite:
        - test user account

        Steps:
        1. Login test user

        Expected result:
        - test user's full name found on the page"""
        self.main_page.logout()
        assert self.login_page.find(self.login_page.locators.REGISTRATION_LOCATOR).is_enabled()

    @pytest.mark.UI
    def test_username(self, login):
        """
        Doc:
        'Information about the current user is correctly displayed in the upper right corner at any resolution'

        Prerequisite:
        - test user account

        Steps:
        1. Login test user

        Expected result:
        - test user's username found on the page"""
        assert self.form_data['username'] == self.main_page.get_username()

    @pytest.mark.UI
    def test_fullname(self, login):
        """
        Doc:
        'Information about the current user is correctly displayed in the upper right corner at any resolution'

        Prerequisite:
        - test user account

        Steps:
        1. Login test user

        Expected result:
        - test user's full name found on the page"""
        assert [self.form_data['name'], self.form_data['surname']] == self.main_page.get_fullname()

    @pytest.mark.UI
    def test_vk_id_ok(self, temp_user_vk):
        """
        Doc:
        'If the user received a VK ID, then this identifier is displayed in the same way in the upper right corner'

        Prerequisite:
        - temporary user account with precreated VK ID

        Steps:
        1. Register temporary user
        2. Add VK ID via vk_mock API
        3. Login temporary user

        Expected result:
        - correct VK ID found on the page"""
        vk_id = temp_user_vk
        assert self.main_page.get_vk_id() == vk_id

    @pytest.mark.UI
    @pytest.mark.xfail(raises=TimeoutException, reason='OK: checking missing VK ID')
    def test_vk_id_fail(self, temp_user):
        """
        Doc:
        'If the user received a VK ID, then this identifier is displayed in the same way in the upper right corner'

        Prerequisite:
        - temporary user account without VK ID

        Steps:
        1. Register temporary user
        2. Login temporary user

        Expected result:
        - VK ID not found on the page """
        self.main_page.get_vk_id()
