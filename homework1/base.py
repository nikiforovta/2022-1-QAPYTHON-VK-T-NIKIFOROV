import pytest
from selenium.common.exceptions import ElementClickInterceptedException, StaleElementReferenceException, \
    TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from ui import links, locators


class BaseCase:
    EMAIL = 'timofey.nikiforov@gmail.com'
    PASSWORD = 'TaeixfnpL76YRkh'

    driver = None

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, open_my_target):
        self.driver = open_my_target
        login_button = self.find(locators.LOGIN_BUTTON_LOCATOR)
        login_button.click()
        login_form = self.find(locators.EMAIL_INPUT_LOCATOR)
        login_form.send_keys(self.EMAIL)
        password_form = self.find(locators.PASSWORD_INPUT_LOCATOR)
        password_form.send_keys(self.PASSWORD)
        login_button = self.find(locators.LOGIN_LOCATOR)
        login_button.click()

    def find(self, locator):
        return self.driver.find_element(*locator)

    def open_profile(self):
        self.driver.get(links.PROFILE_LINK)

    def teardown_profile(self):
        self.change_name(self.EMAIL)
        self.driver.refresh()

    def change_name(self, name):
        name_input = self.find(locators.CHANGE_NAME_LOCATOR)
        name_input.click()
        name_input.clear()
        name_input.send_keys(name)
        self.find(locators.SAVE_CHANGES).click()

    def wait_visible(self, locator):
        return WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(locator))

    def wait_clickable(self, locator):
        return WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(locator))

    LOGOUT_RETRY = 5

    def logout(self):
        for i in range(self.LOGOUT_RETRY):
            try:
                self.wait_clickable(locators.PROFILE_LOCATOR).click()
                self.wait_visible(locators.DROPDOWN_PROFILE_LOCATOR)
                self.wait_clickable(locators.LOGOUT_LOCATOR).click()
                return
            except ElementClickInterceptedException or StaleElementReferenceException or TimeoutException:
                if i == self.LOGOUT_RETRY - 1:
                    raise
