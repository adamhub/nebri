import twitter # from python-twitter package

class twitter_connect(NebriOS):
    listens_to = ['twitter_connect']

    def check(self):
        return self.twitter_connect == True and self.twitter_screen_name != ''

    def action(self):
        # pull from shared kvps
        api = twitter.Api(
            consumer_key=consumer_key, 
            consumer_secret=consumer_secret, 
            access_token_key=access_key, 
            access_token_secret=access_secret
        )

        twitter_user = api.GetUser(screen_name=self.twitter_screen_name)
        self.twitter_user_dict = twitter_user.AsDict()
