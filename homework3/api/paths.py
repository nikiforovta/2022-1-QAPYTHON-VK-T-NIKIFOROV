LOGIN = 'https://auth-ac.my.com/auth?lang=ru&nosavelogin=0'

GET_SEGMENTS = 'api/v2/remarketing/segments.json?fields=id,name&limit=500'
GET_SEGMENT = lambda segment_id: f'api/v2/remarketing/segments/{segment_id}.json'
CREATE_SEGMENT = 'api/v2/remarketing/segments.json?fields=relations__object_type,relations__object_id,' \
                 'relations__params,relations__params__score,relations__id,relations_count,id,name,pass_condition,' \
                 'created,campaign_ids,users,flags '

GET_CAMPAIGNS = 'api/v2/campaigns.json?fields=id,name&sorting=-id&limit=250'
GET_CAMPAIGN = lambda campaign_id: f'api/v2/campaigns.json?fields=id,name&limit=1&_q={campaign_id}'

URLS_ID = 'api/v1/urls'
CONTENT_ID = 'api/v2/content/static.json'
CREATE_CAMPAIGN = 'api/v2/campaigns.json'

DELETE_CAMPAIGN = 'api/v2/campaigns/mass_action.json'
