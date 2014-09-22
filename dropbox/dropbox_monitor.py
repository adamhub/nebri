import dropbox

class dropbox_monitor(NebriOS):
    """Monitor dropbox activity

    checks if a certain file in your dropbox account has been motified in the last 7 days
    if it has, a KVP will be set to alert you to the existence of the new file
    """
    # The script is started by setting "dropbox_monitor_go" to True as you suggested which starts the flow
    listens_to = ["dropbox_monitor_go", ]

    def check(self):
        flow = dropbox.client.DropboxOAuth2FlowNoRedirect(shared.dropbox_key, shared.dropbox_secret)
        client = dropbox.client.DropboxClient(shared.dropbox_token)

        search = client.search("/", "report.otd", file_limit=1000, include_deleted=False)
        if search:
            for item in search:
                current_time = datetime.now()
                modified_time = item['modified']
                modified_time = datetime.strptime(modified_time, "%a, %d %b %Y %H:%M:%S +0000")
                delta = current_time - modified_time
                days = int(delta.days)
                if days <= 7:

    def action(self):
        self.new_file = True
