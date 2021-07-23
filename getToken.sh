#!/bin/bash
# username='CIBMTR Service Account Username'
# password='CIBMTR Service Account Password'
# clientid='Application Client ID'
# clientsecret='Application Client Secret'
# scope='Application Scope'

username=''
password=''
clientId=''
clientSecret=''
clientScope=''

auth_string="Basic $(echo -n ${clientId}:${clientSecret}|base64)"

curl -s --location \
--request POST 'https://nmdp.oktapreview.com/oauth2/ausaexcazhlhxknjs0h7/v1/token' \
--header 'Accept: application/json' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--header "Authorization: ${auth_string}" \
--data-urlencode "grant_type=password" \
--data-urlencode "scope=${clientScope}" \
--data-urlencode "username=${username}" \
--data-urlencode "password=${password}" \
| jq '.access_token' | tr -d '"'