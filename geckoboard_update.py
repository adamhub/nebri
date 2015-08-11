import json
import requests
"""  Data format for shared KVP
{
"data": {
"item": [{"value": 142}, {"value": 200}]
},
"push_url": "https://push.geckoboard.com/v1/send/142235-06263b5d-b239-4845-adde-547ee16ae2a"
}
"""



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
        api_key = ""
        
        payload = {}
        payload['api_key'] = api_key
        payload['data'] = shared.geckoboard_data['data']
    
        r = requests.post(shared.geckoboard_data['push_url'], data=json.dumps(payload))
        if r.status_code == 200:
            self.status = "Success"
        else:
            raise Exception("Could not post geckoboard update."\
                            " Error Code: {}".format(r.status_code))
                            
