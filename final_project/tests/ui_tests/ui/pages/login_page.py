import allure

from ui import locators
from ui.pages.base_page import BasePage


class LoginPage(BasePage):
    locators = locators.LoginPageLocators()

    @allure.step("Login")
    def login(self, credentials):
        self.send_keys(self.locators.CREDENTIALS_INPUT_LOCATOR('username'), credentials[0])
        self.send_keys(self.locators.CREDENTIALS_INPUT_LOCATOR('password'), credentials[1])
        self.click(self.locators.CREDENTIALS_INPUT_LOCATOR('submit'))

    @allure.step("Go to registration page from login page")
    def to_registration(self):
        self.click(self.locators.REGISTRATION_LOCATOR)
