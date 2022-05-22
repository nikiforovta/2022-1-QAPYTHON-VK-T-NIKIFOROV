import allure
from selenium.webdriver import ActionChains

from ui import locators
from ui.pages.base_page import BasePage


class MainPage(BasePage):
    locators = locators.MainPageLocators()

    def get_fullname(self):
        return self.find(self.locators.USER_LOCATOR).text.split(" ")[-2:]

    def get_username(self):
        return self.find(self.locators.USERNAME_LOCATOR).text.split(" ")[-1]

    def get_vk_id(self):
        return self.find(self.locators.VK_ID_LOCATOR).text.split(" ")[-1]

    @allure.step("Logout from main page")
    def logout(self):
        self.click(self.locators.LOGOUT_LOCATOR)

    def click_dropdown(self, i, j):
        if j == 1:
            self.click(self.locators.NAVBAR_LOCATOR(i))
        else:
            menu = self.find(self.locators.NAVBAR_LOCATOR(i))
            submenu = self.find(self.locators.NAVBAR_SUB_LOCATOR(i, j))
            ActionChains(self.driver).move_to_element(menu).click(submenu).perform()
