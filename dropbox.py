import dropbox
 
class dropbox_monitor(NebriOS):
  #Hourly cron for now, still poking at drips
    schedule = "0 * * * *"
  #The script is started by setting "dropbox_monitor_go to true as you suggested which starts the flow, the "code" is to restart the script when the confirmation code is enterd via an email form""
    listens_to = ["dropbox_monitor_go", "code"]
  #class attributes
    app_key = 'APP_KEY'
    app_secret = 'APP_SECRET'
  #Start the flow so as to populate the authorize_url variable to be emailed later if code isn't set.
    flow = dropbox.client.DropboxOAuth2FlowNoRedirect(app_key, app_secret)
    authorize_url = flow.start()
    
    def __datetime(self, date_str):
    return datetime.strptime(date_str, "%a, %d %b %Y %H:%M:%S +0000")
    
    def check(self):
      #check if the code (the confirmation code from dropbox) is set
      if self.code is not None:
		    access_token, user_id = flow.finish(self.code)
		    client = dropbox.client.DropboxClient(access_token)
		    search = client.search("/", "report.otd", file_limit=1000, include_deleted=False)
	    	if(search[0]):
			    for i in search:
				    current_time = time.strftime("%a, %d %b %Y %H:%M:%S +0000")
				    modified_time = search[0]['modified']
				    start = self.__datetime(modified_time)
				    end = self.__datetime(current_time)
			    	delta = end - start
				    days = int(delta.days)
				    if(days <= 7):
				    	return True
				    else:
				    	return False
		    else:
		    	return 'File does not exist.'
	else:
	  #If it isn't set an email is sent with an authorize_url to be clicked to reveal the code, the email also avails a form to fill in the code, once this KVP is set/updated the script is restarted
		send_email(self.last_actor,
            """Hello, Please click the link and enter the confirmation code in the form {{authorize_url}} code := - Please enter the confirmation code
-Nebri OS""", subject="Nebri OS Dropbox")
    def action(self):
        self.new_file = True
