import json
import os

import allure
import pytest
from _pytest.fixtures import FixtureRequest

from ui.pages.base_page import BasePage
from ui.pages.login_page import LoginPage


class BaseCase:
    EMAIL = None
    PASSWORD = None

    driver = None
    logger = None

    login_page = None
    main_page = None
    base_page = None
    segment_page = None
    campaign_page = None

    @pytest.fixture(scope='function', autouse=True)
    def ui_report(self, driver, request, temp_dir):
        failed_test_count = request.session.testsfailed
        yield
        if request.session.testsfailed > failed_test_count:
            browser_logs = os.path.join(temp_dir, 'browser.log')
            with open(browser_logs, 'w') as f:
                for i in driver.get_log('browser'):
                    f.write(f"{i['level']} - {i['source']}\n{i['message']}\n")
            screenshot_path = os.path.join(temp_dir, 'failed.png')
            driver.save_screenshot(screenshot_path)
            allure.attach.file(screenshot_path, 'failed.png', allure.attachment_type.PNG)
            with open(browser_logs, 'r') as f:
                allure.attach(f.read(), 'test.log', allure.attachment_type.TEXT)

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, driver, config, logger, request: FixtureRequest):
        self.driver = driver
        self.logger = logger

        with open('../credentials.json') as credentials:
            credentials_json = json.load(credentials)
            self.EMAIL = credentials_json['EMAIL']
            self.PASSWORD = credentials_json['PASSWORD']

        self.base_page: BasePage = (request.getfixturevalue('base_page'))

        self.login_page: LoginPage = (request.getfixturevalue('login_page'))

    @pytest.fixture(scope='function')
    def login(self):
        self.login_page.login(credentials=(self.EMAIL, self.PASSWORD))
        return self.main_page

    @pytest.fixture(scope='function')
    def open_segments(self):
        self.main_page.open_menu('segments')

    @pytest.fixture(scope='function')
    def open_campaign(self):
        self.main_page.open_menu('campaign')
