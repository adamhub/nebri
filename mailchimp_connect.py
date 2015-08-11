import mailchimp # pip install mailchimp


MAILCHIMP_API_KEY = shared.mailchimp_api_key


class mailchimp_connect(NebriOS):
    listens_to = ['mailchimp_retrieve_stats']

    def check(self):
        return self.mailchimp_retrieve_stats  == True

    def action(self):
        mc = mailchimp.Mailchimp(MAILCHIMP_API_KEY)
        
        cl = mc.campaigns.list()
        if len(cl['data']) > 0:
            latest_campaign_data = cl['data'][0]
            unique_opens = latest_campaign_data['summary']['unique_opens']
            emails_sent = latest_campaign_data['summary']['emails_sent']
            
            open_rates = 0
            if emails_sent > 0:
                open_rates = float(unique_opens)/emails_sent
            
            self.open_rates = open_rates
            #print "STATS: %d/%d = %0.2f" % (unique_opens, emails_sent, float(unique_opens)/emails_sent)
