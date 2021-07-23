#!/usr/bin/env python3

import requests
from requests.auth import HTTPBasicAuth

# username = 'CIBMTR Service Account Username'
# password = 'CIBMTR Service Account Password'
# clientId = 'Application Client ID'
# clientSecret = 'Application Client Secret'
# clientScope = 'Application Scope'

username = ''
password = ''
clientId = ''
clientSecret = ''
clientScope = ''

headers = {'Content-Type': 'application/x-www-form-urlencoded',
           'Accept': 'application/json'}

data = {'grant_type': 'password',
        'scope': clientScope,
        'username': username,
        'password': password}

r = requests.post('https://nmdp.oktapreview.com/oauth2/ausaexcazhLhxKnJs0h7/v1/token',
                  auth=HTTPBasicAuth(clientId, clientSecret),
                  data=data,
                  headers=headers)

accessToken = r.json()["access_token"]
print(accessToken)
