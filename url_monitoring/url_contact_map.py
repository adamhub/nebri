class url_contact_map(NebriOS):
    listens_to = ['broken_urls']

    def check(self):
        if self.broken_urls != []:
            return True

    def action(self):
        #to_contact = shared.url_watch_map[self.url_down]
        # program if from a shared kvp later
        
        self.contactor = []
        
        for url in self.broken_urls:
            contact_email = ""
            contact_cell = 
            self.contactor.append({'priority':2, 'email': contact_email, 'cell': contact_cell, 'message': 'Your website is down! URL: %s' % url, 'subject': 'Site is down: %s' % url})
                # priority 1 - cell/email - now
                # priority 2 - email now cell later
                # priority 3 - email now
                
            #send_email("nick@bixly.com", "This Url is broken: %s" % url, subject="Broken Url: %s" % url)
