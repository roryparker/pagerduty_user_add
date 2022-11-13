import http.client
import json
import csv

api_key = ""
# Email of the person running this script
from_email = ""
pagerduty_team_id = ""
userObjects = []

with open("users.csv", newline='') as csvUsers:
    fileReader = csv.reader(csvUsers)
    for userData in fileReader:
        name = userData[0]
        email = userData[1]
        title = userData[2]
        userObject = {
            "type": "user",
            "name": name,
            "email": email,
            "job_title": title,
            "role": "limited_user",
        }
        userObjects.append(json.dumps(userObject))

conn = http.client.HTTPSConnection("api.pagerduty.com")

headers = {
    'Content-Type': "application/json",
    'Accept': "application/vnd.pagerduty+json;version=2",
    'From': from_email,
    'Authorization': f'Token token={api_key}'
    }
    
for userObject in userObjects:
    conn.request("POST", "/users", userObject, headers)
    res = conn.getresponse()
    data = json.loads(res.read())
    payload = "{\n  \"role\": \"responder\"\n}"
    conn.request("PUT", f'/teams/{pagerduty_team_id}/users/{data["user"]["id"]}', payload, headers)
    res = conn.getresponse()
    data2 = res.read()
