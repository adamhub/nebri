import copy

class show_monitored_urls(NebriOS):
    listens_to = ['show_monitored_urls']

    def check(self):
        return self.show_monitored_urls == True

    def action(self):
        self.show_monitored_urls = False
        
        self.show_monitored_urls_status = "Ran at %s" % datetime.now()
        
        self.monitored_urls = copy.deepcopy(shared.monitored_urls)
        
        load_card("monitored-urls")
