import uuid

import pytest as pytest

from base import BaseCase
from ui import locators, links


class TestTarget(BaseCase):
    @pytest.mark.UI
    def test_login(self):
        assert self.find(locators.username_locator(self.EMAIL)) is not None
        assert self.find(locators.CAMPAIGN_LOCATOR) is not None
        assert '/dashboard' in self.driver.current_url

    @pytest.mark.UI
    @pytest.mark.parametrize("menu, assertions",
                             [("segments",
                               {'elements': [(locators.CREATE_LOCATOR, "Создайте"),
                                             (locators.COMMON_LOCATOR, "Общие сегменты")],
                                'url': '/segments_list'}),
                              ("billing",
                               {'elements': [(locators.PAYER_LOCATOR, BaseCase.EMAIL),
                                             (locators.AUTODEPOSIT_LOCATOR, "АВТОПОПОЛНЕНИЕ")],
                                'url': '#deposit'})])
    def test_menu(self, menu, assertions):
        self.find(locators.MENU_LOCATOR[menu]).click()
        for element in assertions['elements']:
            assert self.find(element[0]).text == element[1]
        assert assertions['url'] in self.driver.current_url

    @pytest.mark.UI
    def test_change_profile(self):
        self.open_profile()
        name = str(uuid.uuid4())
        self.change_name(name)
        assert self.wait_visible(locators.SUCCESS_LOCATOR).text == "Информация успешно сохранена"
        self.driver.refresh()
        assert self.find(locators.username_locator(name)) is not None
        self.teardown_profile()

    @pytest.mark.UI
    def test_logout(self):
        self.logout()
        assert self.find(locators.PROMOTE_LOCATOR).text == 'Рекламируйте товары и услуги в соцсетях'
        assert self.find(locators.START_PROMOTION_LOCATOR).text == 'Запустить рекламу'
        assert self.driver.current_url == links.BASE_LINK
