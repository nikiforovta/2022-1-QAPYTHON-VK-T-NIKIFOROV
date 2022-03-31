import json
import logging
from urllib.parse import urljoin

import requests

logger = logging.getLogger('test')


class InvalidLoginException(Exception):
    pass


class ResponseStatusCodeException(Exception):
    pass


class TargetApiClient:

    def __init__(self, cookies):
        self.base_url = 'https://target.my.com'

        self.session = requests.Session()
        self.set_cookies(cookies)
        self.csrfroken = self.get_token()
        self.session.cookies.update({'csrftoken': self.csrfroken})
        self.request_headers = {'X-CSRFToken': self.csrfroken}

    def _request(self, method, url, headers=None, data=None, expected_status=200, params=None):
        response = self.session.request(method=method, url=url, headers=headers, data=data, params=params)
        if response.status_code != expected_status:
            raise ResponseStatusCodeException(f'Got {response.status_code} {response.reason} for URL "{url}"')
        return response

    def get_token(self):
        response = self._request(method='GET', url=urljoin(self.base_url, 'csrf/'))
        cookies = response.headers['Set-Cookie'].split(';')

        token = [h for h in cookies if 'csrftoken' in h]
        if not token:
            raise Exception('No csrftoken found in main page headers')
        return token[0].split('=')[-1]

    def set_cookies(self, cookies):
        for cookie in cookies:
            new_cookie = {cookie['name']: cookie['value']}
            self.session.cookies.update(new_cookie)

    def get_segments(self):
        path = 'api/v2/remarketing/segments.json?fields=id,name&limit=500'
        response = self._request(method='GET', url=urljoin(self.base_url, path))
        return response.json()['items']

    def get_segment(self, segment_id):
        path = f'api/v2/remarketing/segments.json?fields=id,name&limit=500'
        items = self._request(method='GET', url=urljoin(self.base_url, path)).json()['items']
        for item in items:
            if item['id'] == segment_id:
                return item
        return None

    def post_create_segment(self, name):
        data = {
            'logicType': 'or',
            'name': name,
            'pass_condition': 1,
            'relations': [{'object_type': 'remarketing_app_category',
                           'params': {'install_type': 'now',
                                      'right': 0,
                                      'left': 365,
                                      'type': 'positive',
                                      'apps_count': 1,
                                      'source_id': 14595}}]
        }
        path = 'api/v2/remarketing/segments.json?fields=relations__object_type,relations__object_id,' \
               'relations__params,relations__params__score,relations__id,relations_count,id,name,pass_condition,' \
               'created,campaign_ids,users,flags'
        return self._request(method='POST', url=urljoin(self.base_url, path), data=json.dumps(data),
                             headers=self.request_headers)

    def post_delete_segment(self, segment_id):

        return self._request(method='DELETE',
                             url=urljoin(self.base_url, f'api/v2/remarketing/segments/{segment_id}.json'),
                             expected_status=204, headers=self.request_headers)

    def get_campaigns(self):
        path = 'api/v2/campaigns.json?fields=id,name&sorting=-id&limit=250'
        response = self._request(method='GET', url=urljoin(self.base_url, path))
        return response.json()['items']

    def get_campaign(self, campaign_id):
        path = f'api/v2/campaigns.json?fields=id,name&limit=1&_q={campaign_id}'
        response = self._request(method='GET', url=urljoin(self.base_url, path))
        return response.json()['items'][0]

    def post_create_campaign(self, campaign):
        path = 'api/v2/campaigns.json'
        data = {"name": campaign.name, "read_only": False, "conversion_funnel_id": None, "objective": "traffic",
                "enable_offline_goals": False,
                "targetings": {"split_audience": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], "sex": ["male", "female"], "age": {
                    "age_list": [0, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32,
                                 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54,
                                 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75],
                    "expand": True}, "geo": {"regions": [188]}, "interests_soc_dem": [], "segments": [],
                               "interests": [], "fulltime": {"flags": ["use_holidays_moving", "cross_timezone"],
                                                             "mon": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14,
                                                                     15, 16, 17, 18, 19, 20, 21, 22, 23],
                                                             "tue": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14,
                                                                     15, 16, 17, 18, 19, 20, 21, 22, 23],
                                                             "wed": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14,
                                                                     15, 16, 17, 18, 19, 20, 21, 22, 23],
                                                             "thu": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14,
                                                                     15, 16, 17, 18, 19, 20, 21, 22, 23],
                                                             "fri": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14,
                                                                     15, 16, 17, 18, 19, 20, 21, 22, 23],
                                                             "sat": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14,
                                                                     15, 16, 17, 18, 19, 20, 21, 22, 23],
                                                             "sun": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14,
                                                                     15, 16, 17, 18, 19, 20, 21, 22, 23]},
                               "pads": [102643], "mobile_types": ["tablets", "smartphones"], "mobile_vendors": [],
                               "mobile_operators": []}, "age_restrictions": None, "date_start": None, "date_end": None,
                "autobidding_mode": "second_price_mean", "budget_limit_day": None, "budget_limit": None,
                "mixing": "fastest", "utm": None, "enable_utm": True, "price": "8.48", "max_price": "0",
                "package_id": 961, "banners": [{"urls": {"primary": {"id": 14570324}}, "textblocks": {
                "about_company_115": {"text": campaign.description}},
                                                "content": {"image_240x400": {"id": 10270195}},
                                                "name": campaign.title}]}
        return self._request(method='POST', url=urljoin(self.base_url, path), data=json.dumps(data),
                             headers=self.request_headers)

    def post_delete_campaign(self, campaign_id):
        path = 'api/v2/campaigns/mass_action.json'
        data = [{'id': campaign_id, 'status': 'deleted'}]
        return self._request(method='POST', url=urljoin(self.base_url, path), data=json.dumps(data),
                             headers=self.request_headers, expected_status=204)
