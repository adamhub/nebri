import httplib2

from apiclient.discovery import build
from oauth2client.client import OAuth2WebServerFlow

# scope now includes google docs spreadsheet as well as the drive
OAUTH_SCOPE = ['https://www.googleapis.com/auth/drive',
               'https://spreadsheets.google.com/feeds',
               'https://docs.google.com/feeds']
REDIRECT_URI = 'https://www.example.com/oauth2callback'

"""
shared.client_key - string. app's client id from google developers
shared.client_secret - string. app's client secret from google developers
shared.client_code - string. adde by user with code generated from auth url sent in email
shared.client_credentials - string. auto-filled by script
shared.update_gsheet - dict. contains spreadsheet filename and list of data to insert
ex: {"data": [["583.33", "Jone", "false"], ["58.4", "Kit", "false"], ["1083.27", "Nothing Jordan", "true"]], "filename": "test"}
"""


class google_auth(NebriOS):
    listens_to = ['shared.client_key', 'shared.client_secret',
                  'shared.client_code', 'googleauth_test']
    
    def check(self):
        return shared.client_key and shared.client_secret

    def action(self):
        flow = OAuth2WebServerFlow(shared.client_key, shared.client_secret,
                                   OAUTH_SCOPE, REDIRECT_URI)
        authorize_url = flow.step1_get_authorize_url()

        if shared.client_code:
            shared.client_credentials = flow.step2_exchange(shared.client_code).to_json()
        else:
            self.authorize_url = flow.step1_get_authorize_url()
            send_email(self.last_actor,
                "Hello, Please click the link and enter the confirmation code in the form {{authorize_url}} shared_drive_code := - Please enter the confirmation code\n-Nebri OS",
                subject="Nebri OS Google Auth"
            )
