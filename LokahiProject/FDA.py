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
# username = input("Username: ")
# password = getpass.getpass('Password: ')
payload = {
    'username': "manager",
    'password': "admin123"
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
    while p2.text == 'Invalid report ID.':
        reportID = input("\nInput the # of the report you wish to display: ")
        payload['reportID'] = reportID
        p2 = s.post(host + '/LokahiApp/fda_displayreport/', data=payload)
        print(p2.text)
    if p2.text[-4:] == 'ing.':
        exit()
    file_download = input("Input one of the file numbers above to download the corresponding file: ")
    payload['file_download'] = file_download

    p3 = s.post(host + '/LokahiApp/fda_downloadfile/', data=payload)
    while p3.text == "Invalid file number selection.":
        file_download = input("\nTry again, input one of the file numbers above to download the corresponding file: ")
        payload['file_download'] = file_download
        p3 = s.post(host + '/LokahiApp/fda_downloadfile/', data=payload)
    print(host + p3.text)
    cwd = os.getcwd()
    webbrowser.open(cwd + '\\LokahiApp' + p3.text)
