import smartthings

class st_get_devices(NebriOS):
    listens_to = ['st_get_devices']

    def check(self):
        return True

    def action(self):
        # TODO: loop through list of device types
        # TODO: loop through each device
        # TODO: create dictionary for each device
        # TODO: save list of dictionaries for each device to shared
        st = smartthings.SmartThings(verbose=True)
        st.std = {
            'access_token': shared.st_access_token,
            'api': 'https://graph.api.smartthings.com/api/smartapps/endpoints/%s/' % shared.st_client_id,
            'api_location': 'graph.api.smartthings.com',
            'client_id': shared.st_client_id,
            'client_secret': shared.st_client_secret,
            'scope': 'app',
            'expires_in': 1576799999,
            'token_type': 'bearer',
        }

        st.request_endpoints()

        device_type = ['switch', 'motion', 'temperature', 'contact', 'acceleration', 'presence', 'battery', 'threeAxis']

        shared.st_devices = []

        for type in device_type:
            ds = st.request_devices(type)
            for d in ds:
                shared.st_devices.append({
                    'type': d['type'],
                    'id': d['id'],
                    'label': d['label'] if d['label'] else d['name'],
                });