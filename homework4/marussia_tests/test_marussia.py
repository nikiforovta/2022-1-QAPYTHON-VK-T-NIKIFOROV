import pytest

from marussia_tests.base import BaseCase


class TestMarussia(BaseCase):

    @pytest.mark.Android
    def test_russia(self):
        self.main_page.send_complicated_request("Russia")
        self.main_page.choose_suggestion(self.main_page.locators.POPULATION_REQUEST)
        assert self.main_page.find(self.main_page.locators.TEXT_VIEW('146 млн.')).is_enabled()

    @pytest.mark.Android
    @pytest.mark.parametrize("expression,result",
                             [("2+2", "4"),
                              ("2*(2+2)", "6"),
                              ('два умножить на два плюс два', "6")],
                             ids=["Simple expression",
                                  "Harder expression",
                                  "Hard expression"])
    def test_calculations(self, expression, result):
        self.main_page.send_request(expression)
        assert self.main_page.find(self.main_page.locators.TEXT_VIEW(result))

    @pytest.mark.Android
    def test_source(self):
        self.main_page.open_settings()
        self.settings_page.swipe_to_element(self.settings_page.locators.SOURCE_BUTTON, max_swipes=2, direction='down')
        self.settings_page.open_sources()
        self.source_page.click_for_android(self.source_page.locators.MAIL)
        self.source_page.back_to_settings_page()
        self.settings_page.back_to_main_page()
        self.main_page.send_request("News")
        assert 'Новости Mail.ru' in self.main_page.get_first_track_name()

    @pytest.mark.Android
    def test_settings(self, app_version):
        self.main_page.open_settings()
        self.settings_page.swipe_to_element(self.settings_page.locators.ABOUT_BUTTON, max_swipes=2, direction='down')
        self.settings_page.click_for_android(self.settings_page.locators.ABOUT_BUTTON)
        assert self.about_page.get_version().split(' ')[-1] == app_version
        assert self.about_page.get_copyright() == 'Mail.ru Group © 1998–2021. Все права защищены.'
