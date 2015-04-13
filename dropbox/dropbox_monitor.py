import dropbox

class dropbox_monitor(NebriOS):
    listens_to = ["dropbox_monitor_go", ]

    def check(self):
        flow = dropbox.client.DropboxOAuth2FlowNoRedirect(shared.dropbox_key, shared.dropbox_secret)
        client = dropbox.client.DropboxClient(shared.dropbox_token)

        search = client.search("/", "report.xlx", file_limit=1000, include_deleted=False)
        if search:
            for item in search:
                current_time = datetime.now()
                modified_time = item['modified']
                modified_time = datetime.strptime(modified_time, "%a, %d %b %Y %H:%M:%S +0000")
                delta = current_time - modified_time
                days = int(delta.days)
                if days <= 7:
                    return True

    def action(self):
        send_email("me@example.com","The report is late!!!")
