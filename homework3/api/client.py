import json
from urllib.parse import urljoin

import requests

from api import paths, payloads


class InvalidLoginException(Exception):
    pass


class ResponseStatusCodeException(Exception):
    pass


class TargetApiClient:

    def __init__(self, credentials):
        self.base_url = 'https://target.my.com'
        self.session = requests.Session()
        self.login(credentials)
        self.csrftoken = self.get_token()
        self.session.cookies.update({'csrftoken': self.csrftoken})
        self.request_headers = {'X-CSRFToken': self.csrftoken}

    def _request(self, method, url, headers=None, data=None, expected_status=200, params=None, file=None):
        response = self.session.request(method=method, url=url, headers=headers, data=data, params=params, files=file)
        if response.status_code != expected_status:
            raise ResponseStatusCodeException(f'Got {response.status_code} {response.reason} for URL "{url}"')
        return response

    def login(self, credentials):
        url = paths.LOGIN
        data = payloads.LOGIN(credentials)
        headers = {'Referer': 'https://target.my.com/'}
        self._request(method="POST", url=url, headers=headers, data=data)

    def get_token(self):
        response = self._request(method='GET', url=urljoin(self.base_url, 'csrf/'))
        cookies = response.headers['Set-Cookie'].split(';')
        token = [h for h in cookies if 'csrftoken' in h]
        return token[0].split('=')[-1]

    def set_cookies(self, cookies):
        for cookie in cookies:
            new_cookie = {cookie['name']: cookie['value']}
            self.session.cookies.update(new_cookie)

    def get_segments(self):
        path = paths.GET_SEGMENTS
        response = self._request(method='GET', url=urljoin(self.base_url, path))
        return response.json()['items']

    def get_segment(self, segment_id):
        path = paths.GET_SEGMENTS
        items = self._request(method='GET', url=urljoin(self.base_url, path)).json()['items']
        for item in items:
            if item['id'] == segment_id:
                return item
        return None

    def post_create_segment(self, name):
        path = paths.CREATE_SEGMENT
        data = payloads.SEGMENT(name)
        return self._request(method='POST', url=urljoin(self.base_url, path), data=json.dumps(data),
                             headers=self.request_headers)

    def post_delete_segment(self, segment_id):
        path = paths.GET_SEGMENT(segment_id)
        return self._request(method='DELETE', url=urljoin(self.base_url, path), expected_status=204,
                             headers=self.request_headers)

    def get_campaigns(self):
        path = paths.GET_CAMPAIGNS
        response = self._request(method='GET', url=urljoin(self.base_url, path))
        return response.json()['items']

    def get_campaign(self, campaign_id):
        path = paths.GET_CAMPAIGN(campaign_id)
        response = self._request(method='GET', url=urljoin(self.base_url, path))
        return response.json()['items'][0]

    def get_url_id(self, url='https://target.my.com/campaign/new'):
        return self._request(method='GET', url=urljoin(self.base_url, paths.URLS_ID), params={'url': url}).json()['id']

    def get_content_id(self, content):
        path = paths.CONTENT_ID
        files = [('file', ('campaign.jpg', open(content, 'rb'), 'image/jpeg'))]
        resp = self._request(method='POST', url=urljoin(self.base_url, path), file=files, headers=self.request_headers)
        return resp.json()['id']

    def post_create_campaign(self, campaign, content):
        path = paths.CREATE_CAMPAIGN
        url_id = self.get_url_id()
        content_id = self.get_content_id(content)
        data = payloads.CAMPAIGN(campaign.name, url_id, content_id)
        return self._request(method='POST', url=urljoin(self.base_url, path), data=json.dumps(data),
                             headers=self.request_headers)

    def post_delete_campaign(self, campaign_id):
        path = paths.DELETE_CAMPAIGN
        data = [{'id': campaign_id, 'status': 'deleted'}]
        return self._request(method='POST', url=urljoin(self.base_url, path), data=json.dumps(data),
                             headers=self.request_headers, expected_status=204)
