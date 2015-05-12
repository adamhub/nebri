import twilio
from twilio.rest import TwilioRestClient
from contact_escalation_framework.cef_framework import get_contact, get_next_available, contact_available

class smart_messenger(NebriOS):
    listens_to = ['smart_message']

    # twilio creds (test only)
    # TODO: change this to bixly creds
    TWILIO_ACCOUNT_SID = ""
    TWILIO_AUTH_TOKEN = ""
    TWILIO_NUMBER = "+15555555555"

    def check(self):
        # check if all 3 params are present
        if (self.smart_message['to'] and
            self.smart_message['message'] and
            self.smart_message['priority']):

            return True
        return False

    def send_sms(self, to, msg):
        # initialize twilio client and send SMS
        try:
            client = TwilioRestClient(self.TWILIO_ACCOUNT_SID, self.TWILIO_AUTH_TOKEN)
            status = client.messages.create(body=msg, from_=self.TWILIO_NUMBER, to=to)
            self.progress = 'SMS sent'
            return True
        except twilio.TwilioRestException as e:
            self.progress = 'SMS sending failed'
            raise Exception("Could not send SMS. Error: %s" % e)

    def action(self):
        self.ran_at = datetime.now()

        recipient = self.smart_message['to']
        message = self.smart_message['message']
        priority = self.smart_message['priority']

        # get specific user's data
        self.progress = "Retrieving user info..."
        profile = get_contact(recipient, shared.contacts)

        current_datetime = datetime.now()
        if shared.system_datetime:
            dt = shared.system_datetime
            current_datetime = datetime(
                dt.year, dt.month, dt.day, 
                dt.hour, dt.minute, dt.second
            )

        if not profile:
            # if profile returned None, user has no record in contacts, do nothing
            self.progress = "User info does not exist. Aborting..."
            return False

        if priority == 1:
            # send SMS now
            self.progress = "Sending email and SMS..."
            self.send_sms(profile['phone'], message)

            # always send email regardless of priority
            send_email(profile['email'], message)
        elif priority == 2:
            is_available = contact_available(recipient, profile, current_datetime)

            if is_available:
                # send SMS now
                self.progress = "Sending SMS..."
                self.send_sms(profile['phone'], message)
            else:
                # schedule SMS
                self.progress = "Scheduling SMS..."
                next_available = get_next_available(profile, current_datetime)

                if not shared.sms_schedule:
                    shared.sms_schedule = []
                shared.sms_schedule.append({
                    'message': message,
                    'sender': self.last_actor,
                    'schedule': next_available,
                    'recipient': profile['user'],
                    'recipient_phone': profile['phone']
                })

            # always send email regardless of priority
            self.progress = "Sending email..."
            send_email(profile['email'], message)
        elif priority == 3:
            # always send email regardless of priority
            self.progress = "Sending email..."
            #send_email(profile['email'], message)
            send_email(profile['email'], message)
        else:
            # invalid priority number
            self.progress = "Invalid data. Aborting..."
            raise Exception("Invalid priority number provided.")
