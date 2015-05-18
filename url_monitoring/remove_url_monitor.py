class remove_url_monitor(NebriOS):
    listens_to = ['remove_url_monitor']

    def check(self):
        if self.remove_url_monitor == True:
            if self.url in shared.monitored_urls:
                return True

    def action(self):
        self.remove_url_monitor = False
        
        self.remove_url_monitor_status = "Ran at %s" % datetime.now()
        
        shared.monitored_urls.remove(self.url)
        
        self.show_monitored_urls = True