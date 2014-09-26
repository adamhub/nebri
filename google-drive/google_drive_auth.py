import httplib2

from apiclient.discovery import build
from apiclient.http import MediaFileUpload
from oauth2client.client import OAuth2WebServerFlow

OAUTH_SCOPE = 'https://www.googleapis.com/auth/drive'
REDIRECT_URI = 'urn:ietf:wg:oauth:2.0:oob'

class google_drive_auth(NebriOS):
    listens_to = ['shared.drive_key', 'shared.drive_secret', 'shared.drive_code', 'drive_test']

    def check(self):
        return shared.drive_key and shared.drive_secret

    def action(self):
        flow = OAuth2WebServerFlow(shared.drive_key, shared.drive_secret, OAUTH_SCOPE, REDIRECT_URI)
        if shared.drive_code:
            shared.drive_credentials = flow.step2_exchange(shared.drive_code).to_json()
        else:
            self.authorize_url = flow.step1_get_authorize_url()
            send_email("tomk@bixly.com",
                "Hello, Please click the link and enter the confirmation code in the form {{authorize_url}} shared_drive_code := - Please enter the confirmation code\n-Nebri OS",
                subject="Nebri OS Google Drive"
            )
