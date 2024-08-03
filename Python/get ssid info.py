import requests
from pprint import pprint
from requests import session

#Admin prompt to input Meraki API Key
API_KEY = input("Please enter the Meraki Dashboard API key: ")

org_id = 90527

url = f"https://api.meraki.com/api/v1/organizations/{org_id}"

headers = {
    'X-Cisco-Meraki-API-Key': API_KEY,
    'Accept': "application-json",
    'content-Type' : "application-json"    
}

