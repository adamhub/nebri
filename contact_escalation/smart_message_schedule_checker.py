import twilio, copy
from twilio.rest import TwilioRestClient

class smart_message_schedule_checker(NebriOS):
    schedule = "0 * * * *"

    # twilio creds (test only)
    # TODO: change this to bixly creds
    TWILIO_ACCOUNT_SID = ""
    TWILIO_AUTH_TOKEN = ""
    TWILIO_NUMBER = "+15555555555"

    def check(self):
        return shared.sms_schedule and len(shared.sms_schedule)

    def send_sms(self, to, msg):
        # initialize twilio client and send SMS
        try:
            client = TwilioRestClient(self.TWILIO_ACCOUNT_SID, self.TWILIO_AUTH_TOKEN)
            status = client.messages.create(body=msg, from_=self.TWILIO_NUMBER, to=to)
            return True
        except twilio.TwilioRestException as e:
            raise Exception("Could not send SMS. Error: %s" % e)

    def action(self):
        self.status = "Ran"
        self.ran_at = datetime.now()

        self.current_datetime = self.ran_at
        if shared.system_datetime:
            dt = shared.system_datetime
            self.current_datetime = datetime(
                dt.year, dt.month, dt.day, 
                dt.hour, dt.minute, dt.second
            )

        sms_schedules = copy.copy(shared.sms_schedule)
        for record in sms_schedules:
            if (self.current_datetime < record['schedule'] and 
                record['schedule'] <= self.current_datetime + timedelta(hours=1)):

                # Record only as a KVP if datetime is 
                # spoofed and do not send message
                if shared.system_datetime:
                    self.cef_test_result_message = {
                        'sender': record['sender'],
                        'message': record['message'], 
                        'schedule': record['schedule'], 
                        'recipient': record['recipient']
                    }
                else:
                    self.send_sms(record['recipient_phone'], record['message'])
                    shared.sms_schedule.remove(record)

