class add_url_monitor(NebriOS):
    listens_to = ['add_url_monitor']

    def check(self):
        if self.add_url_monitor == True:
            if not self.url in shared.monitored_urls:
                return True

    def action(self):
        self.add_url_monitor = False
        
        self.add_url_monitor_status = "Ran at %s" % datetime.now()
        
        shared.monitored_urls.append(self.url)
        
        self.show_monitored_urls = True
