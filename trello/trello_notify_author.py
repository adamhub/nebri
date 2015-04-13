class trello_notify_author(NebriOS):
    listens_to = ['trello_card_changeset']

    def check(self):
        return self.trello_card_changeset  != None

    def action(self):
        cset = self.trello_card_changeset
        self.trello_card_changeset = None
        
        if cset['author'] == 'adamtemple':
            send_email ("bob@example.com","""
                A trello card created by you was modified by '%s' on %s. The %s was changed.
                Go to the board: <a href="%s">%s</a>
                """ % (cset['changed_by'], cset['date'], cset['old'].keys()[0], cset['url'], cset['url']))

