import allure

from ui import locators
from ui.pages.base_page import BasePage


class MainPage(BasePage):
    locators = locators.MainPageLocators()

    @allure.step("Open {1} menu")
    def open_menu(self, menu):
        self.click(self.locators.MENU_LOCATOR(menu))
