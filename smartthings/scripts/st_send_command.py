import smartthings
import json

class st_send_command(NebriOS):
    listens_to = ['st_command']

    def check(self):
        if self.st_command and shared.st_access_token and self.st_device:
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
        self.st_status = "Ran Command -- %s -- with arguments -- %s -- at: %s" % (self.st_command, self.st_command_arguments, datetime.now())

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
        # I'm just translating from the example script.

        ds = st.request_devices(self.st_device['type'])
        # I have manually entered the Device Type of "switch" so that we can talk with the Ge Link light bulb in Nick's Office

        # ds = st.request_devices(self.device_type)
        # We'll need to see what "devices" actually holds

        ds = filter(lambda d: self.st_device['id'] in [ d.get("id"), d.get("label"), ], ds)
        # I have manually entered the Device ID of the GE Link light bulb in Nick's Office.

        # ds = filter(lambda d: self.device_id in [ d.get("id"), d.get("label"), ], ds)
        # This will work once we actually have the KVP for device_id setup

        requestd = {"command": self.st_command}

        if self.st_command_arguments:
            requestd["arguments"] = self.st_command_arguments

        for d in ds:
            self.st_response = st.device_request(d, requestd)
        # This is a loop cause I'm guessing there's a way to interact with multiple Devices,
        # but for now, this should only ever have 1 device in the "ds" list