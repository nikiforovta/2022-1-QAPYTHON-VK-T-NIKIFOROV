import allure

from ui import locators
from ui.pages.base_page import BasePage


class LoginPage(BasePage):
    locators = locators.LoginPageLocators()

    @allure.step("Login")
    def login(self, credentials):
        self.click(self.locators.LOGIN_BUTTON_LOCATOR)
        self.send_keys(self.locators.CREDENTIALS_INPUT_LOCATOR('email'), credentials[0])
        self.send_keys(self.locators.CREDENTIALS_INPUT_LOCATOR('password'), credentials[1])
        self.click(self.locators.LOGIN_LOCATOR)
