import pytest

from base import BaseCase


class TestLogin(BaseCase):
    """Authorization tests"""

    @pytest.mark.UI
    @pytest.mark.parametrize(
        'credentials',
        [
            pytest.param(
                ('login', 'password')
            ),
            pytest.param(
                (None, 'password')
            ),
        ],
        ids=[
            'Wrong username',
            'Wrong password'
        ]
    )
    def test_negative_login(self, credentials):
        """Negative authorization test"""
        if not credentials[0]:
            credentials = (self.EMAIL, credentials[-1])
        self.login_page.login(credentials)
        if credentials[0] == self.EMAIL:
            assert self.login_page.find(self.login_page.locators.WRONG_DATA_LOCATOR).is_enabled()
        else:
            assert self.login_page.find(self.login_page.locators.ERROR_LOCATOR).is_enabled()

    @pytest.mark.UI
    def test_successful_login(self, login):
        """Positive authorization test"""
        assert self.main_page.find(self.main_page.locators.CREATE_BUTTON_LOCATOR).is_displayed()


@pytest.mark.usefixtures("login", "open_campaign")
class TestCampaignPage(BaseCase):
    """Tests for \"Campaigns\" page"""

    @pytest.mark.UI
    def test_start_campaign(self):
        name = self.campaign_page.create_campaign()
        assert self.campaign_page.find(self.campaign_page.locators.CAMPAIGN_LOCATOR(name)).text == name


@pytest.mark.usefixtures("login", "open_segments")
class TestSegmentPage(BaseCase):
    """Tests for \"Segments\" page"""

    @pytest.mark.UI
    def test_create_segment(self):
        """Segment creation test"""
        name = self.segment_page.add_segment()
        assert self.segment_page.find(self.segment_page.locators.SEGMENT_LOCATOR(name)).text == name
        self.segment_page.remove_segment(name)

    @pytest.mark.UI
    def test_delete_segment(self):
        """Segment removal test"""
        removed = self.segment_page.remove_segment(self.segment_page.add_segment())
        self.segment_page.send_keys(self.segment_page.locators.SEARCH_LOCATOR, removed)
        assert self.segment_page.find(self.segment_page.locators.NO_RESULTS_LOCATOR).is_displayed()
