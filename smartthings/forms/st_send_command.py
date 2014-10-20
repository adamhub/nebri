class st_send_command(Form):
    form_title = "Send Command to SmartThings"
    form_instructions = "Choose your device and then enter the command:"

    def get_device_names():
        if shared.st_devices:
            return [('{"id": "%s", "type": "%s"}' % (device['id'], device['type']), device['label']) for device in shared.st_devices]
        return []

    st_device = String(label="Device Name", choices=get_device_names(), required=True)
    st_command = String(label="Command", message="Enter the Command you want to execute. e.g. 'setCoolingSetpoint'", required=True)
    st_command_arguments = String(label="Arguments List", message="Enter a LIST of Arguments for the Command using Python List style syntax. e.g. [78]")