import json

# Note that mailparser can only send data through a webhook,
# and it need to be updated to use Nebri's webhooks
# to do the following:
#
# @csrf_exempt
# def webhook(request):
#     val = json.dumps(request.POST)
#     #send email to scriptrunner@nebrios.com
#     #with body:
#     #mailparser_json_string := '{ val }'
# 
#     body = "mailparser_json_string := '%s'" % val
# 
#     send_mail('Test Subject', body, TO, FROM, fail_silently=False)
# 
#     return HttpResponse('Hello from Python!')

# To trigger this via email, send a string to ufhtd@mailparser.io. This string 
# can be an object i.e. {"foo":"bar"}. There is no need for outer quotes when 
# sending via email.

class mailparser_receiver(NebriOS):
    listens_to = ['mailparser_json_string']

    def check(self):
        return not self.ran
        #return isinstance(self.mailparser_json_string, basestring)

    def action(self):
        if isinstance(self.mailparser_json_string, basestring):
            self.mailparser_json_string = json.loads(self.mailparser_json_string)
        self.ran = True
