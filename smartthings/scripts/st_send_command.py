import smartthings
import json

class st_send_command(NebriOS):
    listens_to = ['st_command']

    def check(self):
        if self.st_command and self.st_device_label and shared.st_access_token:
            return True
        elif not shared.st_access_token:
            send_email(self.last_actor,
                       """Access not setup yet. Use this form to get connected:

                       {{ forms.st_oauth_keys }}

                       -Nebri""", subject="Need Access", attach_variables=False)
            return False
        else:
            return False


    def action(self):

        self.st_status = "Ran Command -- %s -- with arguments -- %s -- on device label -- %s -- at: %s" % (self.st_command, self.st_command_arguments, self.st_device_label, datetime.now())

        st = self.st_api_connection()

        if not shared.st_devices:
            self.st_get_devices(st)

        for device in shared.st_devices:
            if device['label'] == self.st_device_label:
                self.st_device = {"id": device['id'], "type": device['type'], "label": device['label']}
                break


        ds = st.request_devices(self.st_device['type'])

        ds = filter(lambda d: self.st_device['id'] in [ d.get("id"), d.get("label"), ], ds)

        requestd = {"command": self.st_command}

        if self.st_command_arguments:
            requestd["arguments"] = self.st_command_arguments

        for d in ds:
            self.st_response = st.device_request(d, requestd)
        # This is a loop cause I'm guessing there's a way to interact with multiple Devices,
        # but for now, this should only ever have 1 device in the "ds" list


    def st_api_connection(self):
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
        return st


    def st_get_devices(self, st):
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