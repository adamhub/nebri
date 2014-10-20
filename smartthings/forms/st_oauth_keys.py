class st_oauth_keys(Form):
    form_title = "SmartThings OAuth"
    form_instructions = """1) Go to you SmartThings dashboard
                        2) Navigate to the IOTDB.bridge SmartApp
                        3) Click on App Settings, then on OAuth
                        4) Copy the Client ID and Client Secret
                        5) Paste them into the form below"""

    st_client_id = String(label="Client ID", required=True)
    st_client_secret = String(label="Client Secret", required=True)