import requests
import os
import urllib.request
import getpass
import django
import webbrowser
from time import sleep
from django.core.files import File

from Crypto.Cipher import ARC4

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
    cont = 1

    while cont:
        p1 = s.post(host + '/LokahiApp/fda_viewreports/', data=payload)
        print(p1.text)
        if p1.text == "========================================\nYou don't have any reports to view.":
            again = input("Press 'n' to exit or any other key to open a new report.")
            if again == 'n':
                exit()
            continue
        reportID = input("Input the # of the report you wish to display: ")
        if(type(reportID)==int):
            print(str(int(reportID))+'===================')
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
        file_download = input("Input one of the file numbers above to download the corresponding file or press 'n' to exit: ")
        if file_download == 'n':
            exit()
        payload['file_download'] = file_download

        p3 = s.post(host + '/LokahiApp/fda_downloadfile/', data=payload)
        while p3.text == "Invalid file number selection.":
            file_download = input("\nTry again, input one of the file numbers above to download the corresponding file: ")
            payload['file_download'] = file_download
            p3 = s.post(host + '/LokahiApp/fda_downloadfile/', data=payload)
        cwd = os.getcwd()

        # webbrowser.open(cwd + '\\LokahiApp' + p3.text)
        file_path = os.path.join(cwd + "\\", p3.text.replace('/', '\\'))
        print(str(file_path))

        if os.path.exists(file_path):
            # # Copy file from directory to location
            # urllib.request.urlretrieve(str(file_path).replace('\\', '/'), p3.text)

            print(file_path)
        else:
            print("Invalid file selection.")
            continue
        again = input("Type 'y' to download another file. Type any other key to exit. ")
        if not again == "y":
            cont = None

        # f = open(file_path, 'rb')
        # file = File(f)
        # print(file_path)
        # response = HttpResponse(file, content_type='application/force_download')
        # response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(os.path.basename(file_path))
        # return response


# def encrypt_file(filename, key):
#     if (os.path.isfile(filename) and (str(type(key))==str(type("hello")))):
#         key = key.encode("UTF-8")
#         encryptedfile = ARC4.new(key)
#         f = open(filename, 'rb')
#         cipher_text = encryptedfile.encrypt(f.read())
#         Outputfile_name = filename + ".enc"
#         Outputfile = open(Outputfile_name, 'wb')
#         Outputfile.write(cipher_text)
#         f.close()
#         Outputfile.close()
#         return True
#     else:
#         print("File does not exist or key is incorrect type")
#         return False
#
#
# def decrypt_file(filename, key):
#     if (os.path.isfile(filename) and (str(type(key))==str(type("hello")))):
#         key = key.encode("UTF-8")
#         decryptedfile = ARC4.new(key)
#         f = open(filename, 'rb')
#         cipher_text = decryptedfile.decrypt(f.read())
#         Outputfile_name = "DEC_" + filename
#         Outputfile = open(Outputfile_name, 'wb')
#         Outputfile.write(cipher_text)
#         f.close()
#         Outputfile.close()
#         return True
#     else:
#         print("File does not exist or key is incorrect type")
#         return False
