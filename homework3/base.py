import os

import pytest

from utils.builder import Builder


class BaseApi:
    @pytest.fixture(scope='function', autouse=True)
    def setup(self, api_client):
        self.api_client = api_client
        self.builder = Builder()

    @pytest.fixture(scope='function')
    def segment(self):
        segment_data = self.builder.segment()
        result = self.api_client.post_create_segment(name=segment_data.name)
        segment_id = result.json()['id']
        segment_data.id = int(segment_id)
        yield segment_data
        self.api_client.post_delete_segment(segment_id)

    @pytest.fixture(scope='function')
    def segment_to_delete(self):
        segment_data = self.builder.segment()

        result = self.api_client.post_create_segment(name=segment_data.name)
        segment_id = result.json()['id']
        segment_data.id = int(segment_id)
        yield segment_data

    @pytest.fixture(scope='function')
    def campaign(self, repo_root):
        campaign_data = self.builder.campaign()
        result = self.api_client.post_create_campaign(campaign_data, os.path.join(repo_root, 'campaign.jpg'))
        campaign_id = result.json()['id']
        print(campaign_id)
        campaign_data.id = int(campaign_id)
        yield campaign_data
        self.api_client.post_delete_campaign(campaign_id)
