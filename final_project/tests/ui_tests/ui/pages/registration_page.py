import allure

from ui import locators
from ui.pages.base_page import BasePage


class RegistrationPage(BasePage):
    locators = locators.RegistrationPageLocators()

    @allure.step("Registration")
    def registration(self, form_data: dict):
        for k, v in form_data.items():
            if k == 'id':
                continue
            self.send_keys(self.locators.FORM_INPUT_LOCATOR(k), v)
        self.send_keys(self.locators.FORM_INPUT_LOCATOR('confirm'), form_data['password'])
        self.click(self.locators.FORM_INPUT_LOCATOR('term'))
        self.click(self.locators.FORM_INPUT_LOCATOR('submit'))

    @allure.step("Go to login page from registration page")
    def to_login(self):
        self.click(self.locators.LOGIN_LOCATOR)
