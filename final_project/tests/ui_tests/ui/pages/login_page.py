import time

import allure

from ui import locators
from ui.pages.base_page import BasePage


class LoginPage(BasePage):
    MAX_RETRIES = 5
    locators = locators.LoginPageLocators()

    @allure.step("Login")
    def login(self, credentials):
        self.send_keys(self.locators.CREDENTIALS_INPUT_LOCATOR('username'), credentials[0])
        self.send_keys(self.locators.CREDENTIALS_INPUT_LOCATOR('password'), credentials[1])
        self.click(self.locators.CREDENTIALS_INPUT_LOCATOR('submit'))

    @allure.step("Go to registration page from login page")
    def to_registration(self):
        self.click(self.locators.REGISTRATION_LOCATOR)

    def get_flash_text(self):
        for _ in range(self.MAX_RETRIES):
            flash_text = self.find(self.locators.ERROR_LOCATOR)
            if flash_text.text != "":
                return flash_text.text
            time.sleep(1)
        return flash_text.text
