import dataclasses
import json
import os
import random

import allure
import pytest
import requests
from _pytest.fixtures import FixtureRequest

from ui.pages.base_page import BasePage
from ui.pages.login_page import LoginPage
from ui.pages.main_page import MainPage
from ui.pages.registration_page import RegistrationPage
from utils.api.client import TMApiClient
from utils.user_builder import Builder


class BaseCase:
    form_data = dict()

    driver = None
    logger = None
    builder = None
    api_client = None

    login_page = None
    main_page = None
    base_page = None
    registration_page = None

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
    def setup(self, repo_root, driver, config, logger, request: FixtureRequest):
        self.driver = driver
        self.logger = logger
        self.builder = Builder()

        with open(os.path.join(repo_root, '../test_user_data.json')) as credentials:
            self.form_data = json.loads(credentials.read())

        self.api_client = TMApiClient(self.form_data)

        self.base_page: BasePage = (request.getfixturevalue('base_page'))

        self.login_page: LoginPage = (request.getfixturevalue('login_page'))

        self.main_page: MainPage = (request.getfixturevalue('main_page'))

        self.registration_page: RegistrationPage = (request.getfixturevalue('registration_page'))

    @allure.step("Registration of user with data {1}")
    def register(self, form_data, checkbox=True):
        self.login_page.to_registration()
        self.registration_page.registration(form_data, checkbox)
        return self.main_page

    @allure.step("Login of precreated test user")
    @pytest.fixture(scope='function')
    def login(self, credentials=None):
        if credentials is None:
            self.login_page.login(credentials=(self.form_data['username'], self.form_data['password']))
        else:
            self.login_page.login(credentials=(credentials['username'], credentials['password']))
        yield self.main_page

    @allure.step("Create temporary user with VK ID")
    @pytest.fixture(scope='function')
    def temp_user_vk(self):
        user_data = self.builder.user()
        self.register(dataclasses.asdict(user_data))
        vk_id = str(random.randint(1, 100))
        requests.post(url=f'http://vk_api:8543/vk_id/{user_data.username}', json={'id': vk_id})
        self.driver.refresh()
        yield vk_id
        self.api_client.delete_user(user_data.username)

    @allure.step("Create temporary user without VK ID")
    @pytest.fixture(scope='function')
    def temp_user(self):
        user_data = self.builder.user()
        self.register(dataclasses.asdict(user_data))
        yield user_data
        self.api_client.delete_user(user_data.username)
