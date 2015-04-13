import httplib2
import json
from urllib import urlencode

 # Get key here: https://trello.com/app-key
TRELLO_KEY = ''
# Get token here, replacing API_KEY with the key you got above
# https://trello.com/1/authorize?key=API_KEY&name=Nebri+Scriptrunner&expiration=never&response_type=token
TRELLO_TOKEN = ''

class trello_change_check(NebriOS):
    listens_to = ['trello_check_cards']

    def check(self):
        return self.trello_check_cards == True
        
    def build_url(self, path, query={}):
        url = 'https://api.trello.com/1'
        if path[0:1] != '/':
            url += '/'
        url += path
        url += '?'
        url += "key=" + TRELLO_KEY
        url += "&token=" + TRELLO_TOKEN

        if len(query) > 0:
            url += '&' + urlencode(query)

        return url
    
    def fetch_json(self, uri_path, query_params={}):
        url = self.build_url(uri_path, query_params)
        
        client = httplib2.Http()
        response, content = client.request(
            url, 'GET', headers={'Accept': 'application/json'}
        )

        # error checking
        if response.status == 401:
            raise Exception("Resource unavailable: %s (HTTP status: %s)" % (
                url, response.status), response.status)
        if response.status != 200:
            raise Exception("Resource unavailable: %s (HTTP status: %s)" % (
                url, response.status), response.status)
        return json.loads(content)

    def action(self):
        self.trello_check_cards = False
        boards = self.fetch_json('/members/me/boards')
        actions = []
        for board in boards:
            change_actions = self.fetch_json(
                '/boards/' + board['id'] + '/actions',
                query_params={'filter': 'updateCard:name,updateCard:desc'}
            )
            create_actions = self.fetch_json(
                '/boards/'+board['id']+'/actions',
                query_params={'filter':'createCard'}
            )
            for action in change_actions:
                actor_id = action['idMemberCreator']
                for caction in create_actions:
                    if action['data']['card']['id'] == caction['data']['card']['id']:
                        creator_id = caction['idMemberCreator']
                        if actor_id != creator_id:
                            # We've found a change by someone other than the author!
                            if shared.trello_notified_actions == None:
                                shared.trello_notified_actions = []

                            if action['id'] not in shared.trello_notified_actions:
                                shared.trello_notified_actions.append(action['id'])
                                ticket_name = action['data']['card']['name']
                                if len(ticket_name) > 40:
                                    ticket_name = ticket_name[:37] + '...'
                                card_url = 'https://trello.com/c/%s/' % (action['data']['card']['shortLink'],)
                                self.trello_card_changeset = {
                                    'author': caction['memberCreator']['username'],
                                    'changed_by': action['memberCreator']['username'],
                                    'changeId': action['id'],
                                    'old': action['data']['old'],
                                    'board': {'id':board['id'],'name': board['name'] },
                                    'date': action['date'],
                                    'card_name': ticket_name,
                                    'url': card_url
                                }
                        break
        
        
