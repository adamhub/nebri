import httplib2
import json

class trello_cards(NebriOS):
    schedule = "*/30 * * * *" # Every 30 minutes

    def check(self):
        return self.trello_get_cards == True
    
    def fetch_json(self, path):
        # Get key here: https://trello.com/app-key
        TRELLO_KEY = ''
        # Get token here, replacing API_KEY with the key you got above
        # https://trello.com/1/authorize?key=API_KEY&name=Nebri+Scriptrunner&expiration=never&response_type=token
        OAUTH_TOKEN = ''

        url = 'https://api.trello.com/1'
        if path[0:1] != '/':
            url += '/'
        url += path
        url += '?key='+TRELLO_KEY+'&token='+OAUTH_TOKEN
        
        client = httplib2.Http()
        response, content = client.request(
            url, 'GET', headers={'Accept': 'application/json'})

        # error checking
        if response.status == 401:
            raise Exception("Resource unavailable: %s (HTTP status: %s)" % (
                url, response.status), response.status)
        if response.status != 200:
            raise Exception("Resource unavailable: %s (HTTP status: %s)" % (
                url, response.status), response.status)
        return json.loads(content)

    def action(self):
        self.trello_get_cards = False
        trello_data = []
        boards = self.fetch_json('/members/me/boards')
        for board in boards:
            cards = self.fetch_json('/boards/' + board['id'] + '/cards')
            trello_data.append({'board':board, 'cards': cards})
        
        shared.trello_data = trello_data

