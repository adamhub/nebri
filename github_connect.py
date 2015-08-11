import datetime
from github import Github  # https://github.com/PyGithub/PyGithub

# When triggering a wake-up, repo_name needs to be sent.
class github_connect(NebriOS):
    listens_to = ['github_connect']

    def check(self):
        return self.github_connect == True

    def action(self):
        self.github_connect = "RAN"
        g = Github(shared.GITHUB_USERNAME, shared.GITHUB_PASSWORD)
        try:
            repo = g.get_repo(self.repo_name)
        except Exception as e:
            print e
            self.error = str(e)
        else:
            since = datetime.datetime.now() - datetime.timedelta(days=1)
            commits = repo.get_commits(since=since)
            # We have to iterate to get number of commits because
            # return value of above call is a pagination
            self.counter = 0
            for commit in commits:
                self.counter += 1
            print "Number of commits since %s: %s" % (since, self.counter)
