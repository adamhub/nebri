import twitter # from python-twitter package

class twitter_connect(NebriOS):
    listens_to = ['twitter_connect']

    def check(self):
        return self.twitter_connect == True and self.twitter_screen_name != ''

    def action(self):
        consumer_key = shared.consumer_key
        consumer_secret = shared.consumer_secret
        access_key = shared.access_key
        access_secret = shared.access_secret
        api = twitter.Api(
            consumer_key=consumer_key, 
            consumer_secret=consumer_secret, 
            access_token_key=access_key, 
            access_token_secret=access_secret
        )

        twitter_user = api.GetUser(screen_name=self.twitter_screen_name)
        self.twitter_user_dict = twitter_user.AsDict()
            # just pulling user's profile data as an example
