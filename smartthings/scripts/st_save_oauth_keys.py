class st_save_oauth_keys(NebriOS):
    listens_to = ['st_client_id', 'st_client_secret']

    def check(self):
        if self.st_client_id and self.st_client_secret:
            return True
        else:
            return False

    def action(self):
        self.st_oauth_status = "New Keys Set: %s" % datetime.now()

        shared.st_client_id = self.st_client_id
        shared.st_client_secret = self.st_client_secret
        shared.st_oauth_email = self.last_actor