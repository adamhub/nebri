# pip install first
import thermostat

class thermostat(NebriOS):
    # this KVP is updated from another script
    # that checks the thermostat
    listens_to == ['shared.temperature'] 

    # determine if the script should run
    def check(self):
        return shared.temperature > 79 

    # if the check is true, action() runs
    def action(self):
        send_email("manager@example.com", "Temperature Adjusted")

        # install and call any Python package 
        thermostat.set(75)
