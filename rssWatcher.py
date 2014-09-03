import feedparser

class rssWatcher(NebriOS):
    listens_to = ['rss_deal_checker']

    def check(self):
        return True

    def action(self):
        #Query the feed
        feed = feedparser.parse("http://s1.dlnws.com/dealnews/rss/editors-choice.xml")

        new_last_entry = feed.entries[0]['title']

        if shared.deal_list2 is None:
            shared.deal_list2 = []

        #iterate the entries
        for entry in feed.entries:
            #Compare to each input
            for inp in shared.rss_inputs:
                #Break out of function because we have been to this point in the feed before.
                if shared.last_rss_entry == entry['title']:
                    #Update with the most recent "last_entry"
                    shared.last_rss_entry = new_last_entry
                    return
                #We make this case insensitive with .lower()
                if inp.lower().strip() in entry['title'].lower():
                    #update the KVP
                    print entry['title']
                    shared.deal_list2.append(entry['title'])

        #Got through the whole RSS Feed
        #Update with the most recent "last_entry"
        shared.last_rss_entry = new_last_entry
