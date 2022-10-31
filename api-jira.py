import requests
from requests.auth import HTTPBasicAuth
from datetime import datetime
import json

from tk import *



'''
curl -H "Authorization: Bearer MDAzNzcxNDQwMzYxOgM14bEjncM6un808o/n39OKludK" -X GET -H "Content-Type: application/json" https://jira-epic.woc.noaa.gov/rest/api/2/issue/createmeta

curl -u "jef.dodson:wWI00ZRAHD0dWThEcGpd" -X GET -H "Content-Type: application/json" https://jira-epic.woc.noaa.gov/rest/api/2/issue/createmeta

'''

# jira personal access token for jef.dodson
TOKEN = JIRA_TOKEN

user = USERNAME
password = PASSWORD

auth = HTTPBasicAuth(user, password)

HEADERS = {'Content-Type': 'application/json',
           'Authorization': f'Bearer {TOKEN}'
          }

HEADERS = {'Content-Type': 'application/json',
           'Accept': 'application/json',
           'Authorization': f'Bearer {TOKEN}'
          }


# URLs
BASE = f'https://jira-epic.woc.noaa.gov'

meta = f'{BASE}/rest/api/2/issue/createmeta'
sd = f'{BASE}/rest/servicedeskapi/servicedesk?start=0&limit=100'
rt = f'{BASE}/rest/servicedeskapi/servicedesk/1/requesttype'

field = f'{BASE}/rest/servicedeskapi/servicedesk/1/requesttype/14/field'

create = f'{BASE}/rest/servicedeskapi/request'

data = {
    'serviceDeskId': '1',
    'requestTypeId': '14',
    'requestFieldValues': {
        'summary': 'Test summary',
        'description': 'Test description'
    }
}

data = {
    'serviceDeskId': '1',
    'requestTypeId': '14',
    'requestFieldValues': {
        'summary': 'Test summary',
        'description': 'Test description',
        'components': [
            {'id': '10302'},
            {'id': '10303'},
            ],
        'priority': {'id': '4'},
        'customfield_10602': {'id': '10514'},
    }
}


'''
https://community.atlassian.com/t5/Jira-questions/Service-Desk-API-Adding-Attachment/qaq-p/1072896
https://stackoverflow.com/questions/12989442/uploading-multiple-files-using-formdata
'''


def get():
    user = USERNAME
    password = PASSWORD
    auth = HTTPBasicAuth(user, password)
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
              }
    url = sd
    print(url)
    r = requests.get(url, headers=headers, auth=auth)
    #content = json.loads(r.content)
    print(r.status_code)
    print(r.content)

def post():
    url = create
    print(url)
    r = requests.post(url, headers=HEADERS, json=data)
    #content = json.loads(r.content)
    print(r.status_code)
    print(r.content)





get()

