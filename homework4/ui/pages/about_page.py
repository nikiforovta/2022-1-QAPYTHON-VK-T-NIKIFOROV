import allure

from ui.locators import AboutPageLocators
from ui.pages.base_page import BasePage


class AboutPage(BasePage):
    locators = AboutPageLocators

    @allure.step("Получаем версию приложения")
    def get_version(self):
        return self.find(self.locators.VERSION_INFO).get_attribute('text')

    @allure.step("Получаем трейдмарк")
    def get_copyright(self):
        return self.find(self.locators.COPYRIGHT_INFO).get_attribute('text')
