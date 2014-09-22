import dropbox

class dropbox_authenticate(NebriOS):
    listens_to = ['shared.dropbox_secret', 'shared.dropbox_key', 'shared.code', 'db_test']

    def check(self):
        return shared.dropbox_secret and shared.dropbox_key

    def action(self):
        flow = dropbox.client.DropboxOAuth2FlowNoRedirect(shared.dropbox_key, shared.dropbox_secret)
        if shared.code:
            try:
                shared.dropbox_token, shared.dropbox_user_id = flow.finish(shared.code)
            except dropbox.rest.ErrorResponse as e:
                send_email(self.last_actor,
                    "Hello, Your code did not work; please click the link and enter the new confirmation code in the form {{authorize_url}} shared_code := - Please enter the confirmation code\n-Nebri OS",
                    subject="Nebri OS Dropbox"
                )
        else:
            self.authorize_url = flow.start()
            send_email(self.last_actor,
                "Hello, Please click the link and enter the confirmation code in the form {{authorize_url}} shared_code := - Please enter the confirmation code\n-Nebri OS",
                subject="Nebri OS Dropbox"
            )
