import pytest

from api.client import ResponseStatusCodeException
from base import BaseApi


class TestSegment(BaseApi):
    @pytest.mark.API
    def test_segment_creation(self, segment):
        result = self.api_client.get_segment(segment.id)
        assert result['id'] == segment.id and result['name'] == segment.name

    @pytest.mark.API
    def test_segment_removal(self, segment_to_delete):
        self.api_client.post_delete_segment(segment_to_delete.id)
        with pytest.raises(ResponseStatusCodeException):
            self.api_client.post_delete_segment(segment_id=segment_to_delete.id)


class TestCampaign(BaseApi):
    @pytest.mark.API
    def test_campaign_creation(self, campaign):
        response = self.api_client.get_campaign(campaign.id)
        assert response['id'] == campaign.id and response['name'] == campaign.name
