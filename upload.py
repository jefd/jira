import requests
import json

from tk import *

#url = 'http://localhost:8000'
BASE = f'https://jira-epic.woc.noaa.gov'

def create_request():
    create_url = f'{BASE}/rest/servicedeskapi/request'
    print(create_url)

    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'Authorization': f'Bearer {TOKEN}'
              }
    data = {
        'serviceDeskId': '1',
        'requestTypeId': '14',
        'requestFieldValues': {
            'summary': 'Test summary with attachments',
            'description': 'Test description with attachments',
            'components': [
                {'id': '10302'},
                {'id': '10303'},
                ],
            'priority': {'id': '4'},
            'customfield_10602': {'id': '10514'},
        }
    }

    r = requests.post(create_url, headers=headers, json=data)
    print(r.status_code)
    print(r.content)
    if r.status_code == 201:
        content = json.loads(r.content)
        #issue_id = content['issueId']
        return content


def upload():
    upload_url = f'{BASE}/rest/servicedeskapi/servicedesk/1/attachTemporaryFile'
    print(upload_url)

    headers = {'Accept': 'application/json',
               'Authorization': f'Bearer {TOKEN}',
               'X-Atlassian-Token': 'no-check',
               'X-ExperimentalApi': 'opt-in',
              }


    # files = [('file', open('a.txt', 'rb')), ('file', open('a.html', 'rb')), ('file', open('binary', 'rb'))]


    multiple_files = [

        ('file', ('a.txt', open('a.txt', 'rb'), 'text/plain')),
        ('file', ('a.html', open('a.html', 'rb'), 'text/html')),
        ('file', ('a.bin', open('a.bin', 'rb'), 'application/octet-stream')),
    ]

    # r = requests.post(url, data=payload, files=files)
    r = requests.post(upload_url, headers=headers, files=multiple_files)
    print(r.status_code)
    print(r.content)
    if r.status_code == 201:
        content = json.loads(r.content)
        return content
        

def attach(issue_id, temp_ids):
    attach_url = f'{BASE}/rest/servicedeskapi/request/{issue_id}/attachment'
    print(attach_url)
    #issue_id = '13002'
    headers = {'Accept': 'application/json',
               'Content-Type': 'application/json',
               'Authorization': f'Bearer {TOKEN}',
               #'X-Atlassian-Token': 'no-check',
               'X-ExperimentalApi': 'opt-in',
              }

    '''
    json = {
            'temporaryAttachmentIds': [
                'temp13320094701793446871',
                'temp18358553896228365731',
                'temp11794625735693222861',
            ],
            'public': True
    }
    '''

    json_data = {'temporaryAttachmentIds': temp_ids, 
                 'public': True}
            

    r = requests.post(attach_url, headers=headers, json=json_data)
    print(r.status_code)
    print(r.content)
    if r.status_code == 201:
        content = json.loads(r.content)
        return content


def main():
    '''
    sd_request = create_request()
    issue_id = sd_request['issueId']
    content = upload()
    temp_ids = [item['temporaryAttachmentId'] for item in content['temporaryAttachments']] 
    attach(issue_id, temp_ids)
    '''
    print(TOKEN)
     

if __name__ == '__main__':
    main()


