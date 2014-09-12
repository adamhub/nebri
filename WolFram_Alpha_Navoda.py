import urllib
import wolframalpha
import urllib2
from xml.etree import ElementTree as etree


class wolfram(object):

    def __init__(self, appid):
        self.appid = appid

    def search(self, resp):
        client = wolframalpha.Client(self.appid)
        res = client.query(resp)
        if len(res.pods) > 0:
            texts = ""
            pod = res.pods[1]
            if pod.text:
                texts = pod.text
                Res_Split = texts.split('.')
                arg_1 = Res_Split[0]
                revenue = arg_1[1:]
                try:
                    if int(revenue) >= 300:
                        self.send_email("test@examples.com", '''Hi, Google has reached their revenue to $300b''')
                    else:
                        print "Google has not reached it's revenue to $300b yet."
                except:
                    print "Erorr in output."
            else:
                texts = "There is no result."
        else:
            print "Sorry, no Pods found."

   
if __name__ == "__main__":
    schedule = "0 0 * * *"
    appid = 'T8WRWQ-7X2GVQ6Y3V'
    query = 'Google Revenue'
    w = wolfram(appid)
    w.search(query)
