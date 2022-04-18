LOGIN = lambda credentials: f'email={credentials[0]}&' \
                            f'password={credentials[1]}&' \
                            'continue=https://target.my.com/auth/mycom?state=target_login=1&ignore_opener=1#email&' \
                            'failure=https://account.my.com/login/'

SEGMENT = lambda name: {'name': name, 'pass_condition': 1, 'relations': [{'object_type': 'remarketing_app_category',
                                                                          'params': {'right': 0, 'left': 365,
                                                                                     'type': 'positive',
                                                                                     'source_id': 14595}}]}

CAMPAIGN = lambda name: {"name": name, "objective": "traffic", "targetings": {"pads": [102643]}, "package_id": 961,
                         "banners": [
                             {"urls": {"primary": {"id": 14570324}}, "content": {"image_240x400": {"id": 10270195}}}]}
