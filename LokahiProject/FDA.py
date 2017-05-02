import requests
import os
import urllib
import urllib.request
import getpass
import django
import webbrowser
from time import sleep

from Crypto.Cipher import AES

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LokahiProject.settings')
django.setup()

print('========================================')
print('Welcome to the File Download Application')
print('========================================')
username = input("Username: ")
password = getpass.getpass('Password: ')
payload = {
    'username': username,
    'password': password
}

host = "http://127.0.0.1:8000"

with requests.session() as s:
    p = s.post(host + '/LokahiApp/fda_login/', data=payload)
    if not p.text == "Login successful.":
        print("Your credentials were denied.")
        exit()

    p1 = s.post(host + '/LokahiApp/fda_viewreports/', data=payload)
    print(p1.text)
    if p1.text == "You don't have any reports to view.":
        print("The FDA will now exit.")
        exit()
    reportID = input("Input the # of the report you wish to display: ")
    payload['reportID'] = reportID

    p2 = s.post(host + '/LokahiApp/fda_displayreport/', data=payload)
    print(p2.text)
    while p2.text == 'Invalid report ID. Try again.':
        reportID = input("\nInput the # of the report you wish to display: ")
        payload['reportID'] = reportID
        p2 = s.post(host + '/LokahiApp/fda_displayreport/', data=payload)
        print(p2.text)

    # parse = p2.text
    # parse2 = p2.text