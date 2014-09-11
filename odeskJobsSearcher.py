import odesk
import json
import datetime
import dateutil.parser
import json


#pip install python-dateutil
#pip install python-odesk


#API keys of your application (this script)
#Get it from https://www.odesk.com/services/api/keys
public_key = "todo"
secret_key = "todo"

#Tokens for user that authorized this app
#Use odeskJobsSearcher_authentication_helper.py for getting this tokens
oauth_access_token = "todo"
oauth_access_token_secret = "todo"

#Job search parameters, tune it as needed
#(reference: https://developers.odesk.com/?lang=python#jobs_search-for-jobs)
max_date_created_offset = 7 # maximum age of job (in days)
job_search_parameter = {'job_status': 'open',
                        'days_posted': 5,
                        'budget': '1000',
                        'client_hires':'15',
                        'skills': 'python'}




class odeskJobsSearcher(NebriOS):

    listens_to = ['get_odesk_jobs']
    schedule = "0 0 * * *" # daily


    def check_date_is_within_offset(self, date, offset):
        """Checks if given date is withing given offset of
           days from today (in past)"""
        smallest_allowed_date = datetime.date.today() - datetime.timedelta(
                                                    days=offset)
        job_date = dateutil.parser.parse(date).date()
        return job_date >= smallest_allowed_date

    def convert_job(self, job):
        """Filters unneeded fields from given job, and
           returns job with only title, url and date_created fields"""
        try:
            converted_job = {'title':job['title'],
                             'url':job['url'],
                             'date_created':job['date_created']}
        except Exception, e:
            print "Job conversion error. Looks like API problem"
            raise e

        return converted_job

    def get_jobs_list(self, client, jobs_parameter):
        """Searches for all available jobs on oDesk accordingly
           to given jobs_parameter search query, then filters
           out too old jobs and returns title, url and
           date_created fields for each job"""
        jobs_api_response = []
        current_page_offset = 0
        max_page_size = 100

        while True:
            try:
                current_jobs_api_response = client.provider_v2.search_jobs(
                                     jobs_parameter,
                                     page_offset = current_page_offset,
                                     page_size = max_page_size)

            except Exception, e:
                print "API or http error occured, can't do much there :-("
                raise e

            jobs_api_response += current_jobs_api_response

            #check for last page
            if len(current_jobs_api_response) < max_page_size:
                break

            #update offset to match next page
            current_page_offset += max_page_size

        try:
            #filter jobs with date_created > max_date_created
            #get only needed data from jobs
            jobs = [self.convert_job(i) for i in jobs_api_response if
                self.check_date_is_within_offset(i['date_created'],
                                                 max_date_created_offset)]
        except Exception, e:
            print "API or https error occured, or there is API change"
            raise e

        return jobs

    def jobs_search(self):
        client = odesk.Client(public_key, secret_key,
                        oauth_access_token=oauth_access_token,
                        oauth_access_token_secret=oauth_access_token_secret)

        jobs = self.get_jobs_list(client=client,
                                  jobs_parameter=job_search_parameter)

        return jobs


    def check(self):
        jobs = self.jobs_search()
        #check passes  only if there is at least one job found
        if len(jobs) > 0:
            self.jobs = json.dumps(jobs)
            return True
        return False

    def action(self):
        #update shared variable
        shared.compatible_odesk_jobs = self.jobs
        return
		
