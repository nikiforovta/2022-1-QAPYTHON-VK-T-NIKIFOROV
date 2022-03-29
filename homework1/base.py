import time

import pytest
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from ui import links, locators


class BaseCase:
    EMAIL = 'timofey.nikiforov@gmail.com'
    PASSWORD = 'TaeixfnpL76YRkh'
    username = EMAIL
    LOGOUT_RETRY = 5

    driver = None

    def login(self):
        login_button = self.find(locators.LOGIN_BUTTON_LOCATOR)
        login_button.click()
        login_form = self.find(locators.CREDENTIALS_INPUT_LOCATOR('email'))
        login_form.send_keys(self.EMAIL)
        password_form = self.find(locators.CREDENTIALS_INPUT_LOCATOR('password'))
        password_form.send_keys(self.PASSWORD)
        login_button = self.find(locators.LOGIN_LOCATOR)
        login_button.click()

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, open_my_target):
        self.driver = open_my_target
        self.login()
        yield
        if self.driver.current_url == links.PROFILE_LINK:
            self.change_name(self.EMAIL)

    def find(self, locator):
        return self.driver.find_element(*locator)

    def open_profile(self):
        self.driver.get(links.PROFILE_LINK)

    def change_name(self, name):
        name_input = self.find(locators.CHANGE_NAME_LOCATOR)
        name_input.click()
        name_input.clear()
        name_input.send_keys(name)
        self.find(locators.SAVE_CHANGES).click()
        self.username = name

    def wait_visible(self, locator):
        return WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(locator))

    def wait_clickable(self, locator):
        return WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(locator))

    def logout(self):
        for i in range(self.LOGOUT_RETRY):
            try:
                self.wait_clickable(locators.PROFILE_LOCATOR).click()
                self.wait_visible(locators.DROPDOWN_PROFILE_LOCATOR)
                self.wait_clickable(locators.LOGOUT_LOCATOR).click()
                return
            except:
                if i == self.LOGOUT_RETRY - 1:
                    raise
                else:
                    time.sleep(1)

    def check_name(self):
        return self.find(locators.USERNAME_LOCATOR(self.username)).get_attribute("title") == self.username
