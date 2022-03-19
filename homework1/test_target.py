import uuid

import pytest as pytest

from base import BaseCase
from ui import locators


class TestTarget(BaseCase):
    @pytest.mark.UI
    def test_login(self):
        assert self.find(locators.USERNAME_LOCATOR(self.EMAIL)).get_attribute("title") == self.EMAIL

    @pytest.mark.UI
    @pytest.mark.parametrize("menu, assertions",
                             [("segments",
                               (locators.CREATE_LOCATOR, "Создайте")),
                              ("billing",
                               (locators.PAYER_LOCATOR, BaseCase.EMAIL))])
    def test_menu(self, menu, assertions):
        self.find(locators.MENU_LOCATOR(menu)).click()
        assert self.find(assertions[0]).text == assertions[1]

    @pytest.mark.UI
    @pytest.mark.usefixtures("teardown_profile")
    def test_change_profile(self):
        self.open_profile()
        name = str(uuid.uuid4())
        self.change_name(name)
        self.driver.refresh()
        assert self.find(locators.USERNAME_LOCATOR(name)).get_attribute("title") == name

    @pytest.mark.UI
    def test_logout(self):
        self.logout()
        assert self.find(locators.START_PROMOTION_LOCATOR).text == 'Запустить рекламу'
