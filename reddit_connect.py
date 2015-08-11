import praw


class reddit_checker(NebriOS):
    listens_to = ['check_reddit']

    def check(self):
        return self.check_reddit == True

    def has_new(self):
        r = praw.Reddit(user_agent="nebritest1.0")
        submissions = r.get_subreddit('cryptocurrency').get_new()
        for thread in submissions:
            created = datetime.fromtimestamp(int(thread.created_utc))
            hours_ago = abs(datetime.now() - created).total_seconds() / 3600.0

            # Set a drip for every 12 hours so all threads created within 12hrs of
            # current datetime is considered as new
            if hours_ago <= 12.0:
                return True
        return False

    def action(self):
        shared.reddit_has_new_thread = self.has_new()
