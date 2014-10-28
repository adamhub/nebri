class st_example(NebriOS):
    listens_to = ['st_example']

    def check(self):
        return True

    def action(self):

        # The Script st_send_commands have been built as a wrapper to the SmartThings Hub
        # It takes 2 Required KVPs plus 1 optional KVP
        # Simply populate the KVPs will the necessary values and it will take it from there

        # First, set self.st_device_label to the Label of the device you want to control
        # Note that in SmartThings this is the Label and not the Name

        self.st_device_label = "Office Thermostat"

        # Next, store the specific device command to run into "self.st_command"

        self.st_command = "setCoolingSetpoint"

        # We are sending the command "setCoolingSetpoint" to our Thermostat

        # A full list of built-in commands are available here: https://graph.api.smartthings.com/ide/doc/capabilities
        # Custom device-types can also be triggered by simply using the appropriate command names

        # If your command accepts arguments, such as our command used above,
        # add the arguments to a List and save to self.st_command_arguments

        # This KVP is optional

        self.st_command_arguments = [78]


        # All together, setting these 3 KVPs will cause st_send_command to tell our Thermostat to
        # beging cooling the office to 78 degrees