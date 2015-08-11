import requests
import json


class pipelinedeals_connect(NebriOS):
    listens_to = ['connect_pipelinedeals']

    def check(self):
        return self.connect_pipelinedeals  == True

    def action(self):
        self.connect_pipelinedeals = "RAN"
        api_key = shared.pipelinesdeals_api_key
        first_name = shared.pipelinedeals_first_name
        
        base_url = "https://api.pipelinedeals.com/api/v3/people.json"
        
        full_url = "%s?api_key=%s&conditions[person_name]=%s" % (base_url, api_key, first_name)
        
        d=requests.get(full_url)
        data = d.json()
        data = data['entries']
        
        #check the first name if it is equal to first_name
        final_data = []
        for dn in data:
            if first_name.lower().strip() == dn['first_name'].lower().strip():
                final_data.append(dn)
        
        d_enc = json.dumps(final_data)
        self.users_retrieved = d_enc
