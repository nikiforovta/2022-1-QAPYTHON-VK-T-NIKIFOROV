import os

import allure
import pytest
from _pytest.fixtures import FixtureRequest

from ui.pages.base_page import BasePage
from ui.pages.campaign_page import CampaignPage
from ui.pages.login_page import LoginPage
from ui.pages.main_page import MainPage
from ui.pages.segment_page import SegmentPage


class BaseCase:
    EMAIL = 'timofey.nikiforov@gmail.com'
    PASSWORD = 'TaeixfnpL76YRkh'

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

        self.base_page: BasePage = (request.getfixturevalue('base_page'))

        self.login_page: LoginPage = (request.getfixturevalue('login_page'))

        self.main_page: MainPage = (request.getfixturevalue('main_page'))

        self.campaign_page: CampaignPage = (request.getfixturevalue('campaign_page'))

        self.segment_page: SegmentPage = (request.getfixturevalue('segment_page'))

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
