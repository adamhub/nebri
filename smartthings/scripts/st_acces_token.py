class st_acces_token(NebriOS):
    listens_to = ['st_access_token']

    def check(self):
        return self.st_access_token

    def action(self):
        shared.st_access_token = self.st_access_token
        self.st_get_devices = True