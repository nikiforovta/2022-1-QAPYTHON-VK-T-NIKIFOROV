import dataclasses

import pytest
from selenium.common.exceptions import TimeoutException

from base import BaseCase


class TestRegistration(BaseCase):
    """Registration tests"""

    @pytest.mark.UI
    def test_positive_registration(self, temp_user):
        """Testing normal registration process with all user data provided"""
        assert temp_user.username == self.main_page.get_username()

    @pytest.mark.UI
    def test_negative_registration_already_exists(self, temp_user):
        """An attempt to create already existing user profile"""
        self.main_page.logout()
        self.register(dataclasses.asdict(temp_user))
        assert self.login_page.get_flash_text() == "User already exist"

    @pytest.mark.UI
    @pytest.mark.parametrize("no_username", [0, 1], ids=["", "Missing username"])
    @pytest.mark.parametrize("no_email",
                             [0, pytest.param(1, marks=pytest.mark.xfail(reason='BUG: This field is not optional'))],
                             ids=["", "Missing email"])
    @pytest.mark.parametrize("no_firstname", [0, 1], ids=["", "Missing first name"])
    @pytest.mark.parametrize("no_password", [0, 1], ids=["", "Missing password"])
    @pytest.mark.parametrize("no_checkbox", [0, 1], ids=["", "Missing SDET checkbox"])
    def test_negative_registration_missing_fields(self, no_username, no_firstname, no_email, no_password, no_checkbox):
        """An attempt to create user profile missing some user data"""
        user = self.builder.user()
        if no_firstname or not (no_username or no_email or no_firstname or no_password or no_checkbox):
            user.user_name = ""
            self.register(dataclasses.asdict(user))
            assert self.registration_page.find(
                self.registration_page.locators.FORM_INPUT_LOCATOR("user_name")).get_attribute(
                "validationMessage") != ""
        elif no_username:
            user.username = ""
            self.register(dataclasses.asdict(user))
            assert self.registration_page.find(
                self.registration_page.locators.FORM_INPUT_LOCATOR("username")).get_attribute("validationMessage") != ""
        elif no_email:
            user.email = ""
            self.register(dataclasses.asdict(user))
            assert self.registration_page.find(
                self.registration_page.locators.FORM_INPUT_LOCATOR("email")).get_attribute("validationMessage") != ""
        elif no_password:
            user.password = ""
            self.register(dataclasses.asdict(user))
            assert self.registration_page.find(
                self.registration_page.locators.FORM_INPUT_LOCATOR("password")).get_attribute("validationMessage") != ""
        elif no_checkbox:
            self.register(dataclasses.asdict(user), False)
            assert self.registration_page.find(
                self.registration_page.locators.FORM_INPUT_LOCATOR("term")).get_attribute("validationMessage") != ""


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
        """Negative authorization test"""
        if not credentials[0]:
            credentials = (self.form_data['username'], credentials[-1])
        self.login_page.login(credentials)
        if credentials[0] == self.form_data['username']:
            assert self.login_page.find(
                self.login_page.locators.REGISTRATION_LOCATOR).is_enabled()
        else:
            assert self.login_page.get_flash_text() == "Invalid username or password"

    @pytest.mark.UI
    def test_successful_login(self, login):
        """Positive authorization test"""
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
        """Doc: 'All links must contain information about resources and work properly'
        Prerequisite: test user account
        Steps:
        - login test user
        Expected result: correct links found at the page's center
        """
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
        """Doc: 'All links must contain information about resources and work properly'
        Prerequisite: test user account
        Steps:
        - login test user
        Expected result: correct links found at the navigation bar """
        self.main_page.click_dropdown(*item)
        self.driver.switch_to.window(self.driver.window_handles[-1])
        assert self.driver.current_url == result_url

    @pytest.mark.UI
    def test_random_fact(self, login):
        """Doc: 'A random motivational fact about Python is displayed at the bottom of the page'
        Prerequisite: test user account
        Steps:
        - login test user
        Expected result: text found at the page's footer """
        assert self.main_page.find(self.main_page.locators.RANDOM_FACT_LOCATOR).is_enabled()

    @pytest.mark.UI
    def test_logout(self, login):
        """Doc: 'the Logout button should successfully log out the user'
        Prerequisite: test user account
        Steps:
        - login test user
        Expected result: test user's full name found on the page"""
        self.main_page.logout()
        assert self.login_page.find(self.login_page.locators.REGISTRATION_LOCATOR).is_enabled()

    @pytest.mark.UI
    def test_username(self, login):
        """Doc: 'information about the current user is correctly displayed in the upper right corner at any
        resolution'
        Prerequisite: test user account
        Steps:
        - login test user
        Expected result: test user's username found on the page """
        assert self.form_data['username'] == self.main_page.get_username()

    @pytest.mark.UI
    def test_fullname(self, login):
        """Doc: 'information about the current user is correctly displayed in the upper right corner at any
        resolution'
        Prerequisite: test user account
        Steps:
        - login test user
        Expected result: test user's full name found on the page """
        assert [self.form_data['name'], self.form_data['surname']] == self.main_page.get_fullname()

    @pytest.mark.UI
    def test_vk_id_ok(self, temp_user_vk):
        """Doc: 'if the user received a VK ID, then this identifier is displayed in the same way in the upper right
        corner'
        Prerequisite: temporary user account with precreated VK ID
        Steps:
        - register temporary user
        - add VK ID via vk_mock API
        - login temporary user
        Expected result: correct VK ID found on the page """
        vk_id = temp_user_vk
        assert self.main_page.get_vk_id() == vk_id

    @pytest.mark.UI
    @pytest.mark.xfail(raises=TimeoutException, reason='OK: checking missing VK ID')
    def test_vk_id_fail(self, temp_user):
        """Doc: 'if the user received a VK ID, then this identifier is displayed in the same way in the upper right
        corner'
        Prerequisite: temporary user account without VK ID
        Steps:
        - register temporary user
        - login temporary user
        Expected result: VK ID not found on the page """
        self.main_page.get_vk_id()
