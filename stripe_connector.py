import stripe
import json


class stripe_connector(NebriOS):
    listens_to = ['stripe_connect']

    def check(self):
        return self.stripe_connect  == True

    def action(self):
        # fill in secret key, or use a shared kvp
        SECRET_KEY = ''
        stripe.api_key = shared.SECRET_KEY
        s = stripe.Charge.all(limit=1) 
        # the API returns latest payments first
        arr = s['data']
        s_data = "null"
        if len(arr) > 0:
            s_data = arr[0]

        s_data = json.dumps(s_data)
        
        self.latest_payment = s_data
