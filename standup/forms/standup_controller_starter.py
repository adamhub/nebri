class standup_controller_starter(Form):
    form_title = "Manually Run the Standup Controller"
    form_instructions = "Simply submit this Form to get the Standup Controller to go"

    standup_controller_go = Boolean(initial=True)