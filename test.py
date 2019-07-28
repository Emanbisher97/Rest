'''
Created on ١٨ ذو القعدة ١٤٤٠ هـ

@author: eman
'''
import requests,json

data = { 'username' : 'eman', 'password' : '1234' }
r = requests.post('http://127.0.0.1:5000/team/members', data=data, verify=False)
print(r.text)
cookies=dict(r.cookies)
#token = json.loads(r.cookies._cookies['172.20.203.3']['/'])['session']
token = r.cookies._cookies['127.0.0.1:5000']['/']['session'].value
headers = { 'Authorization' : 'Token ' + token }
r = requests.get('http://127.0.0.1:5000/team/members', headers=headers, verify=False,cookies=cookies)
print(r.text)
parsed = json.loads(r.text)

    
    