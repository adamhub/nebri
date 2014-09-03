# pip install twilio
from twilio.rest import TwilioRestClient

ACCOUNT_SID = ""  # SID from Twilio account
AUTH_TOKEN = ""  # Token from Twilio account

class send_sms_on_change(NebriOS):
    listens_to = ['sms_to', 'sms_message']

    client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)

    def check(self):
        return self.sms_to is not None and self.sms_message is not None

    def action(self):
        self.client.messages.create(
            to="+%s" % self.sms_to,
            from_="+197xxxxxxxx", # your Twilio number, required
            body=str(self.sms_message),
        )


