import dropbox
import time
import re
from datetime import datetime


app_key = '07gz8s75oxfvmbg'
app_secret = 'tf94vvgp96unnrf'

flow = dropbox.client.DropboxOAuth2FlowNoRedirect(app_key, app_secret)

authorize_url = flow.start()
print '1. Go to: ' + authorize_url
print '2. Click "Allow" (you might have to log in first)'
print '3. Copy the authorization code.'
code = raw_input("Enter the authorization code here: ").strip()


access_token, user_id = flow.finish(code)

def __datetime(date_str):
    return datetime.strptime(date_str, "%a, %d %b %Y %H:%M:%S +0000")

class dropbox_monitor(NebriOS):
    schedule = "0 * * * *"

    def check(self):
        client = dropbox.client.DropboxClient(access_token)
	search = client.search("/", "start", file_limit=1000, include_deleted=False)
	if(search[0]):
		for i in search:
			current_time = time.strftime("%a, %d %b %Y %H:%M:%S +0000")
			modified_time = search[0]['modified']
			start = __datetime(modified_time)
			end = __datetime(current_time)
			delta = end - start
			days = int(delta.days)
			if(days <= 7):
				return True
			else:
				return False
	else:
		return 'File does not exist.'
    def action(self):
        self.new_file = True
