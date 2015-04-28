import httplib2
from datetime import datetime

from oauth2client.client import OAuth2Credentials
from apiclient.discovery import build
from apiclient import errors

def get_all_files(service):
    result = []
    page_token = None

    while True:
        try:
            param = {}
            if page_token:
                param['pageToken'] = page_token
            files = service.files().list(**param).execute()

            result.extend(files['items'])
            page_token = files.get('nextPageToken')
            if not page_token:
                break
        except errors.HttpError, error:
            break

    return result

class google_drive_monitor(NebriOS):
    listens_to = ['monitor_drive']

    def check(self):
        credentials = OAuth2Credentials.from_json(shared.client_credentials)
        http = httplib2.Http()
        http = credentials.authorize(http)

        drive_service = build('drive', 'v2', http=http)

        files = get_all_files(drive_service)

        for file in files:
            if file['title'] == 'report.otd':
                current_time = datetime.now()
                self.modified_time = file['modifiedDate']
                delta = current_time - self.modified_time.replace(tzinfo=None)
                days = int(delta.days)
                if days <= 7:
                    return True

        return False

    def action(self):
        self.new_file_drive = True
