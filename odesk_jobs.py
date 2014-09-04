import odesk
from datetime import datetime, timedelta
import mechanize,cookielib
import re
import sys
import json

class odesk_jobs(NebriOS):
    listens_to = ['example']
    #schedule = "0 0 * * *" # daily

    app_key = 'e314b3e45875cfd14a0e4d5a1f0f4e86'  # your oDesk application key
    app_secret = '4ae4c042138d1e63'               # oDesk application secret key
    
    #to get oDesk api tokens you need:
    username = '' # your oDesk login
    password = '' # your oDesk password

    def login_to_odesk(self, client, br):
        # Cookie Jar
        cj = cookielib.LWPCookieJar()
        br.set_cookiejar(cj)

        # Browser options
        br.set_handle_equiv(True)
        br.set_handle_gzip(True)
        br.set_handle_redirect(True)
        br.set_handle_referer(True)
        br.set_handle_robots(False)

        # Follows refresh 0 but not hangs on refresh > 0
        br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

        # Want debugging messages?
        #br.set_debug_http(True)
        #br.set_debug_redirects(True)
        #br.set_debug_responses(True)

        # User-Agent
        br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

        # Open odesk site
        r = br.open('https://www.odesk.com/login.php')
        form = br.forms().next()  # actually login form name is 'login' but there is only one form
        print 'Logging in to oDesk using URL', form.action
        form['username'] = self.username
        form['password'] = self.password
        br.form = form
        r = br.submit()
        html = r.read()
        m = re.match('[^]*(Invalid username, email or password)[^]*', html)

        if m.groups():
            raise RuntimeError, 'Cannot login to oDesk: Invalid username, email or password'
        else:
            print 'Login successful'

    def get_verifier(self, client, br):
        verifier = ''
        if client and br:
            url = client.auth.get_authorize_url()
            print 'Getting verifier using URL', url
            r = br.open(url)
            html = r.read()
            # authorize our application (if needed)
            for form in br.forms():
                if form.attrs['id'] == 'authorize':
                    print "Sending authorize"
                    br.form = form
                    r = br.submit()
                    html = r.read()
                    break
            # check that our verifier is on form and return it
            m = re.search('Your oauth_verifier=([a-zA-Z0-9]+)<\/div>', html)
            if m:
                verifier = m.groups()[0]
                print 'Verifier received:', verifier
        else:
            print "Something is wrong in initialisation: client:", client, "browser:", br
        return verifier


    def authorize(self):
        # for details go to https://developers.odesk.com/?lang=python#authentication_oauth-10
        client = odesk.Client(public_key=self.app_key, secret_key=self.app_secret)

        # 1. Get request token
        request_token, request_token_secret = client.auth.get_request_token()
        print 'Received request_token:', request_token, ', request_token_secret:', request_token_secret

        # 2. Authorize and get verifier
        # Browser
        br = mechanize.Browser()
        self.login_to_odesk(client, br)
        verifier = self.get_verifier(client, br)

        # 3. Get access token
        access_token, access_token_secret = client.auth.get_access_token(verifier)

        # 4. update and save new tokens
        if access_token and access_token_secret:
            client = odesk.Client(public_key=self.app_key, secret_key=self.app_secret,
                                       oauth_access_token=access_token, oauth_access_token_secret=access_token_secret,
                                       fmt='json')
            self.access_token = access_token
            self.access_token_secret = access_token_secret
            return client
        return

    def search_jobs(self, client):
        if not client:
            print('Client must be initialized before calling job_search')
            raise RuntimeError, 'Client is not initialized'

        request_params = {'q':'python',
                          'job_status': 'open',
                          'days_posted': 5,
                          'budget': '1000',
                          'client_hires': '15',
                          'skills':['python'] }
        response = client.provider_v2.search_jobs(data=request_params)
        if response:
            jobs_found = response
            return jobs_found
        return

    def filter_date_created(self, jobs_found, days_ago=7):
        if not jobs_found:
            return
        jobs_filtered = []
        #get current datetime in utc because server gives us response in utc
        week_ago = datetime.utcnow() - timedelta(days=days_ago)
        for job in jobs_found:
            date_created = datetime.strptime(job[u'date_created'], "%Y-%m-%dT%H:%M:%S+%f")
            if (date_created.isoformat() > week_ago.isoformat() ):
                jobs_filtered.append(job)
        print 'Total jobs found: ', len(jobs_found)
        print 'Filtered jobs: ', len(jobs_filtered)
        self.jobs_filtered = jobs_filtered
        return jobs_filtered


    def check(self):
        # 3 atempts to get acess tokens and create odesk clint
        for a in range(3):
            # if we have all tokens - just create oDesk Client
            if self.access_token and self.access_token_secret:
                client = odesk.Client(public_key=self.app_key, secret_key=self.app_secret,
                                       oauth_access_token=self.access_token, oauth_access_token_secret=self.access_token_secret,
                                       fmt='json')
            else: #else we have to login and get access tokens
                client = self.authorize()

            if not client: continue

            # get jobs from oDesk:
            try:
                jobs = self.search_jobs(client)
            except RuntimeError, err:
                print 'Error while searching jobs on oDesk:', err
                continue

            if not jobs: continue

            jobs_filtered = self.filter_date_created(jobs)
            if not self.jobs_filtered: continue
            else: return True
        #if during 3 attempts we didn't return True, nothing is found or error occured.
        return False


    def action(self):
        if not shared.compatible_odesk_jobs:
            shared.compatible_odesk_jobs = []
        if not self.jobs_filtered:
            return

        for job in self.jobs_filtered:
            shared.number_of_elements_in_list_at_action = len(self.jobs_filtered)
            shared.compatible_odesk_jobs.append( {'job' : job['title'],
                                                  'url' : job['url'],
                                                  'date_created': job['date_created']})