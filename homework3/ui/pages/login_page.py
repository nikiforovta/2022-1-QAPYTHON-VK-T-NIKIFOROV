import allure

from ui import locators
from ui.pages.base_page import BasePage


class LoginPage(BasePage):
    locators = locators.LoginPageLocators()

    @allure.step("Login")
    def login(self, credentials):
        self.click(self.locators.LOGIN_BUTTON_LOCATOR)
        login_form = self.find(self.locators.CREDENTIALS_INPUT_LOCATOR('email'))
        login_form.send_keys(credentials[0])
        password_form = self.find(self.locators.CREDENTIALS_INPUT_LOCATOR('password'))
        password_form.send_keys(credentials[1])
        self.click(self.locators.LOGIN_LOCATOR)
