''' This script will send a mail to the client when Google reaches their revenue to $300b. '''

import urllib2
import urllib
import httplib
from xml.etree import ElementTree as etree
import smtplib


class wolfram(object):

    def __init__(self, appid): 
        self.appid = appid
        self.base_url = 'http://api.wolframalpha.com/v2/query?'
        self.headers = {'User-Agent': None}

    
    def _get_xml(self, ip):
        url_params = {'input': ip, 'appid': self.appid}
        data = urllib.urlencode(url_params)
        req = urllib2.Request(self.base_url, data, self.headers)
        xml = urllib2.urlopen(req).read()
        return xml

    
    def _xmlparser(self, xml):
        data_dics = {}
        tree = etree.fromstring(xml)
        # retrieving every tag with label 'plaintext'
        for e in tree.findall('pod'):
            for item in [ef for ef in list(e) if ef.tag == 'subpod']:
                for it in [i for i in list(item) if i.tag == 'plaintext']:
                    if it.tag == 'plaintext':
                        data_dics[e.get('title')] = it.text
        return data_dics

    
    def search(self, ip):
        # This function will query about Google's revenue using WolframAlpha API
        xml = self._get_xml(ip)
        result_dics = self._xmlparser(xml)
        titles = result_dics.keys()
        Res = result_dics['Result']
        Res_Split = Res.split('.')
        arg_1 = Res_Split[0]
        revenue = arg_1[1:]
        try:
            if int(revenue) >= 300:
                self.send_mails()
            else:
                print "Google has not reached it's revenue to $300b yet."
        except:
            print "Erorr in output."

   
    def send_mails(self):
        gmail_user = "test@test.com"
        gmail_pwd = "test@123"
        FROM = 'test@test.com'
        TO = ['test1@test.com'] #must be a list
        SUBJECT = "Google has reached it's revenue to $300b"
        TEXT = "Hi,\n\nThis is to inform you that Google has reached it's revenue to $300b.\n \nRegards,\nAutomatic Mail Sender."

         # Prepare actual message
        message = """\From: %s\nTo: %s\nSubject: %s\n\n%s
        """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
        try:
            #server = smtplib.SMTP(SERVER) 
            server = smtplib.SMTP("smtp.test.com", 25) 
            server.ehlo()
            server.starttls()
            server.login(user_name, password)
            server.sendmail(FROM, TO, message)
                #server.quit()
            server.close()
            print 'Google has reached their revenue to $300b.\nSuccessfully sent the mail'
        except:
            print "Failed to send mail"


if __name__ == "__main__":
    schedule = "0 0 * * *"
    appid = 'T8WRWQ-7X2GVQ6Y3V'
    query = 'Google Revenue'
    w = wolfram(appid)
    w.search(query)
    
