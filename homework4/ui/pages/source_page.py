import allure

from ui.locators import NewsSourceLocators
from ui.pages import BasePage


class SourcePage(BasePage):
    locators = NewsSourceLocators

    @allure.step("Выбираем \"Новости Mail.ru\" в качестве источника новостей")
    def choose_mail(self):
        self.click_for_android(self.locators.MAIL)

    @allure.step("Возврат к окну настроек")
    def back_to_settings_page(self):
        self.driver.back()
