import json
import requests

class geckoboard_update(NebriOS):
    listens_to = ['shared.geckoboard_data']

    def check(self):
        if shared.geckoboard_data:
            return True
        return False

    def action(self):
        self.status = "Ran"
        self.ran_at = datetime.now()
        
        # geckoboard api key
        # TODO: change this to bixly creds (sample only)
        api_key = "0be2329c71bee77b53904b2b91ccf576"
        
        payload = {}
        payload['api_key'] = api_key
        payload['data'] = shared.geckoboard_data['data']
    
        r = requests.post(shared.geckoboard_data['push_url'], data=json.dumps(payload))
        if r.status_code == 200:
            self.status = "Success"
        else:
            raise Exception("Could not post geckoboard update."\
                            " Error Code: {}".format(r.status_code))
