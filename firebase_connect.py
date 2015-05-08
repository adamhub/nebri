from firebase import firebase    # from python-firebase


class firebase_connect(NebriOS):
    listens_to = ['trigger_firebase_write']

    def check(self):
        return self.trigger_firebase_write  == True

    def action(self):
        self.trigger_firebase_write = "RAN"
        firebase_url = shared.FIREBASE_URL # sample: "https://example.firebaseio.com"
        value = "test_value"
        location = "" # can be any location under the firebase url (e.g. '/users') or blank for root
        
        secret = shared.FIREBASE_SECRET
        email = shared.FIREBASE_EMAIL # not really needed. can be blank
        authentication = None
        if secret:
            authentication = firebase.FirebaseAuthentication(secret, email)
        
        fbase = firebase.FirebaseApplication(firebase_url, authentication)
        
        result = fbase.post(location, value, params={'print': 'pretty'}, headers={'X_FANCY_HEADER': 'VERY FANCY'}, connection=None)
        
        self.fetched = result
