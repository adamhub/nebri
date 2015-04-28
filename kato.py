import json
import httplib2


class send_to_kato(NebriOS):
    KATO_HTTP_POST_FORMAT = 'https://api.kato.im/rooms/%s/simple'
    
    # Fill in your room id 
    KATO_ROOM_ID = ''
    KATO_HTTP_POST_ENDPOINT = KATO_HTTP_POST_FORMAT % (KATO_ROOM_ID,)

    listens_to = ['send_to_kato']
    

    def check(self):
        return u'%s' % self.send_to_kato

    def action(self):
        data = {
            'renderer': 'markdown',
            'text': u'%s' % self.send_to_kato
        }

        headers = {
            'content-type': 'application/json'
        }
        
        h = httplib2.Http('.cache')
        (resp, content) = h.request(
            self.KATO_HTTP_POST_ENDPOINT,
            'POST',
            body=json.dumps(data),
            headers=headers
        )
