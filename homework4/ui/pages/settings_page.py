import allure

from ui.locators import SettingsPageLocators
from ui.pages import BasePage


class SettingsPage(BasePage):
    locators = SettingsPageLocators

    @allure.step("Открываем источники новостей")
    def open_sources(self):
        self.click_for_android(self.locators.SOURCE_BUTTON)

    @allure.step("Открываем окно \"О приложении\"")
    def open_about(self):
        self.click_for_android(self.locators.ABOUT_BUTTON)

    @allure.step("Возврат к основному окну приложения")
    def back_to_main_page(self):
        self.driver.back()
