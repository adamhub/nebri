import twitter # from python-twitter package

class twitter_connect(NebriOS):
    listens_to = ['twitter_connect']

    def check(self):
        return self.twitter_connect == True and self.twitter_screen_name != ''

    def action(self):
        api = twitter.Api(
            consumer_key=shared.TWITTER_CONSUMER_KEY, 
            consumer_secret=shared.TWITTER_CONSUMER_SECRET, 
            access_token_key=shared.TWITTER_ACCESS_TOKEN_KEY, 
            access_token_secret=shared.TWITTER_ACCESS_TOKEN_SECRET
        )

        twitter_user = api.GetUser(screen_name=self.twitter_screen_name)
        print twitter_user
