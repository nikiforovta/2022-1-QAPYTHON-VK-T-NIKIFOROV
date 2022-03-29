import uuid

import pytest as pytest

from base import BaseCase
from ui import locators


class TestTarget(BaseCase):
    @pytest.mark.UI
    def test_login(self):
        assert self.check_name()

    @pytest.mark.UI
    @pytest.mark.parametrize("menu, assertion",
                             [("segments",
                               locators.CREATE_LOCATOR),
                              ("billing",
                               locators.PAYER_LOCATOR)])
    def test_menu(self, menu, assertion):
        self.find(locators.MENU_LOCATOR(menu)).click()
        assert self.find(assertion).is_displayed()

    @pytest.mark.UI
    def test_change_profile(self):
        self.open_profile()
        name = str(uuid.uuid4())
        self.change_name(name)
        self.driver.refresh()
        assert self.check_name()

    @pytest.mark.UI
    def test_logout(self):
        self.logout()
        assert self.find(locators.START_PROMOTION_LOCATOR).text == 'Запустить рекламу'
