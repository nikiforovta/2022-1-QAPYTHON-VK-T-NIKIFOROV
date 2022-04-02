import allure
from selenium.common.exceptions import TimeoutException

from ui.locators import MainPageLocators
from ui.pages.base_page import BasePage


class MainPage(BasePage):
    locators = MainPageLocators()

    @allure.step("Открываем окно настроек")
    def open_settings(self):
        self.click_for_android(self.locators.SETTINGS_BUTTON)

    @allure.step("Отправляем поисковый запрос")
    def send_request(self, query, first=True):
        if first:
            self.click_for_android(self.locators.KEYBOARD_INPUT)
        self.find(self.locators.REQUEST_FIELD).send_keys(query)
        self.click_for_android(self.locators.SEND_REQUEST_BUTTON)
        self.driver.back()

    @allure.step("Отправляем поисковый запрос, который может пройти не с первого раза")
    def send_complicated_request(self, query):
        first = True
        while True:
            try:
                self.send_request(query, first)
                first = False
                if self.find(self.locators.REPLY).is_enabled():
                    return
            except TimeoutException:
                pass

    @allure.step("Выбор предлагаемого поискового запроса")
    def choose_suggestion(self, locator):
        for i in range(self.ACTION_RETRY):
            try:
                self.swipe_element_lo_left(self.locators.SUGGESTIONS)
                self.find(locator)
                self.click_for_android(locator)
                return
            except TimeoutException:
                if i == self.ACTION_RETRY - 1:
                    raise

    @allure.step("Управление воспроизведением")
    def playback(self):
        return self.click_for_android(self.locators.PAUSE)

    @allure.step("Перемотать на один трек назад")
    def backward_track(self):
        return self.click_for_android(self.locators.BACKWARD)

    @allure.step("Смотрим имя трека")
    def get_track_name(self):
        return self.find(self.locators.TRACK).get_attribute('text')

    @allure.step("Ищем первый трек в плейлисте")
    def get_first_track_name(self):
        self.playback()
        self.backward_track()
        track = self.get_track_name()
        while True:
            self.backward_track()
            previous_track = self.get_track_name()
            if track == previous_track:
                return track
            else:
                track = previous_track
