import time

import allure
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class BasePage(object):
    locators = None

    def __init__(self, driver):
        self.driver = driver

    def wait(self, timeout=None):
        if timeout is None:
            timeout = 30
        return WebDriverWait(self.driver, timeout=timeout)

    def find(self, locator, timeout=None):
        return self.wait(timeout).until(EC.presence_of_element_located(locator))

    @allure.step('Click')
    def click(self, locator, timeout=None):
        self.find(locator, timeout=timeout)
        element = self.wait(timeout).until(EC.element_to_be_clickable(locator))
        element.click()
        return element

    @allure.step('Send keys')
    def send_keys(self, locator, keys, timeout=None, clear=True):
        element = self.click(locator, timeout=timeout) if clear else self.find(locator, timeout=timeout)
        if clear:
            element.clear()
        element.send_keys(keys)

    @allure.step('Check alert message')
    def find_validation_message(self, locator):
        return self.find(locator).get_attribute("validationMessage")

    @allure.step('Check warning message')
    def get_flash_text(self):
        for _ in range(self.MAX_RETRIES):
            flash_text = self.find(self.locators.ERROR_LOCATOR)
            if flash_text.text != "":
                return flash_text.text
            time.sleep(1)
        return flash_text.text
