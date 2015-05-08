import httplib2
import json
import logging
from urllib import urlencode


logging.basicConfig(filename='trello-change-check.log', level=logging.DEBUG)

# Get key here: https://trello.com/app-key
# Add shared KVP 'TRELLO_KEY' with a value of the key
# Get token here, replacing API_KEY with the key you got above
# https://trello.com/1/authorize?key=API_KEY&name=Nebri+Scriptrunner&expiration=never&response_type=token
# Add shared KVP trello_tocken and trello_key with the appropriate values

class trello_log_nonauthor_changes(NebriOS):
    """
    This class finds cards across all boards your API has access to
    and logs them to Nebri. Other rules reacto to it to send notifcations
    and such.
    """
    listens_to = ['trello_check_cards']
        # this should be a drip

    def check(self):
        return self.trello_check_cards == True
        
    def build_url(self, path, query={}):
        url = 'https://api.trello.com/1'
        if path[0:1] != '/':
            url += '/'
        url += path
        url += '?'
        url += "key=" + shared.TRELLO_KEY
        url += "&token=" + shared.TRELLO_TOKEN

        if len(query) > 0:
            url += '&' + urlencode(query)

        #logging.debug('[Url] >> %s' % (url,))
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
                
        json_loaded_content = json.loads(content)
        
        return json_loaded_content

    def action(self):
        self.trello_check_cards = False
        boards = self.fetch_json('/members/me/boards')
        #logging.debug('[Boards] >> %s' % (boards,))
        
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
            #logging.debug('[Change actions]: %s' % (change_actions,))
            #logging.debug('[Create actions]: %s' % (create_actions,))
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
                                    
                                if action.get('data') and action.get('data').get('card') and action.get('data').get('card').get('shortLink'):
                                    card_url = 'https://trello.com/c/%s/' % (action['data']['card']['shortLink'],)
                                    #logging.debug('[Affected card]: %s' % (card_url,))
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
        
        
