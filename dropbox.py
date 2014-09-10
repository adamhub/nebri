import dropbox
import time
import re
from datetime import datetime

#App key and secret to be acquired from the Dropbox developer site.
app_key = 'APP_KEY'
app_secret = 'APP_SECRET'

#Starting the Authorization flow
flow = dropbox.client.DropboxOAuth2FlowNoRedirect(app_key, app_secret)

#Instead of a direct redirect here we simply print the url
authorize_url = flow.start()
print '1. Go to: ' + authorize_url
print '2. Click "Allow" (you might have to log in first)'
print '3. Copy the authorization code.'

#What this does is prompt the user to input the Authorization code
code = raw_input("Enter the authorization code here: ").strip()

#We use the Auth Code to request an access_token which we can store and associate with a particular user.
access_token, user_id = flow.finish(code)

#We define a function to interact with the date, time property returned by the dropbox API when we run a search later on
def __datetime(date_str):
    return datetime.strptime(date_str, "%a, %d %b %Y %H:%M:%S +0000")

#We begin the integration with NebriOS
class dropbox_monitor(NebriOS):
	#Setting the script to run hourly
    schedule = "0 * * * *"

    def check(self):
    	#Create a client object
        client = dropbox.client.DropboxClient(access_token)
	#Run a search for the file report.otd in our root Dropbox folder
	search = client.search("/", "report.otd", file_limit=1000, include_deleted=False)
	#A check for results
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
