class st_authorize(NebriOS):
    listens_to = ['shared.st_client_id', 'shared.st_client_secret', 'shared.st_oauth_email', 'st_authorize']

    def check(self):
        return shared.st_client_id and shared.st_client_secret and shared.st_oauth_email


    def action(self):
        send_email(shared.st_oauth_email,
                   """
                   Please authorize your SmartThings App by following this link:

                   http://oauth.nebrios.com/smartthings/oauth/authorize/?client_id={{ shared.st_client_id }}&client_secret={{ shared.st_client_secret }}&instance_inbox=risethink@nebrios.com&instance_name=risethink&sender={{ last_actor }}

                   Thank you.
                   """,
                   subject="Authorize SmartThings App",
                   attach_variables=False)