# NOTE: requires pyapi-gitlab
# $> pip install pyapi-gitlab python-dateutil pytz

import gitlab
import pytz

from dateutil import parser


class count_recent_gitlab_commits(NebriOS):
    listens_to = ['count_recent_gitlab_commits']

    GITLAB_PROJECT_ID = shared.gitlab_project_id


    def check(self):
        return self.count_recent_gitlab_commits

    def get_project_info_cache_key(self):
        return shared.GITLAB_PROJECT_INFO_CACHE_KEY_FORMAT % self.GITLAB_PROJECT_ID

    def action(self):
        shared.GITLAB_PROJECT_INFO_CACHE_KEY_FORMAT = 'GITLAB_PROJECT_INFO_%s'
        shared.GITLAB_HOST = 'http://gitlab.com'
        shared.GITLAB_PRIVATE_TOKEN = ''
        
        gl = gitlab.Gitlab(shared.GITLAB_HOST, token=shared.GITLAB_PRIVATE_TOKEN)

        # Get project info first
        project_info_cache_key = self.get_project_info_cache_key()
        project_info_cache = getattr(shared, project_info_cache_key, None)
        if not project_info_cache:
            project_info_cache = gl.getproject(self.GITLAB_PROJECT_ID)
            project_info_cache['recent_commits_count'] = 0

        # Compute now in UTC
        utc_now = datetime.datetime.now(tz=pytz.utc)
        utc_past_day = utc_now - datetime.timedelta(hours=24)
        qualified_commits = list()

        for commit in gl.getall(gl.getrepositorycommits, self.GITLAB_PROJECT_ID, page=0):
            created_at = parser.parse(commit['created_at'])
            utc_created_at = created_at.astimezone(pytz.utc)

            if utc_created_at >= utc_past_day:
                qualified_commits.append(commit)

        # Save the data
        project_info_cache['recent_commits_count'] = len(qualified_commits)
        setattr(shared, project_info_cache_key, project_info_cache)
