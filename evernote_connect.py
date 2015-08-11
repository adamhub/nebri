import evernote.edam.type.ttypes as Types        #from evernote
from evernote.api.client import EvernoteClient   #from evernote


class evernote_connect(NebriOS):
    listens_to = ['save_to_evernote']

    def check(self):
        return self.save_to_evernote == True

    def action(self):
        self.save_to_evernote= "RAN"
        dev_token = shared.EVERNOTE_DEV_TOKEN
        client = EvernoteClient(token=dev_token, sandbox=False)
        # you can get your personal DEV_TOKEN here:
        # https://www.evernote.com/api/DeveloperToken.action
        
        note_title = "Test note title"
        note_body = "Test note body"
        
        note_store = client.get_note_store()
        note = Types.Note()
        note.title = note_title
        note.content = '<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd">'
        note.content += '<en-note>%s</en-note>' % note_body
        note_store.createNote(note)
