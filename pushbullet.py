from pushbullet import Pushbullet # from pushbullet.py package

class pushbullet_connect(NebriOS):
    listens_to = ['pushbullet_connect']

    def check(self):
        return self.pushbullet_connect == True

    def action(self):
        # fill in the shared kvp in your instance
        pb_api = Pushbullet(shared.pb_api_key)
        notif_dict = self.notif_dict

        if notif_dict['type'] == 'note':
            note = pb_api.push_note(notif_dict['title'], notif_dict['note'])
        elif notif_dict['type'] == 'link':
            link = pb_api.push_link(notif_dict['title'], notif_dict['link'])
        elif notif_dict['type'] == 'list':
            pb_list = pb_api.push_list(notif_dict['title'], notif_dict['list'])
        elif notif_dict['type'] == 'address':
            address = pb_api.push_address(notif_dict['title'], notif_dict['address'])

        # Push Note
        # note = pb_api.push_note("This is the title", "This is the body")

        # Push Address
        # address = ""
        # address = pb_api.push_address("home", address)

        # Push List
        # to_buy = ["milk", "bread", "cider"]
        # to_buy_list = pb.push_list("Shopping list", to_buy)
