from feedparser import feedparser

class rssfeed(NebriOS):
    listens_to = ['shared.watch_list']

    def check(self):
       return True

    def action(self):
        feed = feedparser.parse("http://s1.dlnws.com/dealnews/rss/editors-choice.xml")
        list_of_products_brands = shared.watch_list.splitlines()
        matches_from_feed = set()
        for i in range(0, len(feed['entries'])):
            for keyword in list_of_products_brands:
                if keyword in feed['entries'][i].title:
                    matches_from_feed.add(feed['entries'][i].title)
        shared.deal_list = '\n'.join(matches_from_feed)
