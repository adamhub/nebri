import json

from slackclient import SlackClient    # pip install slackclient

# This script requires that send_slack_message is set to True,
# and that a message and channel are specified. If your message
# has spaces, it will need to be enclosed in quotes.

token = ''
client = SlackClient(token)


class slack_connector(NebriOS):
    listens_to = ['send_slack_message']

    def check(self):
        return self.send_slack_message  == True

    def action(self):
        channel = self.slack_channel
        msg = self.slack_message
        if channel and msg:
            success, channel = get_channel_id(channel)
            if success:
                client.api_call("chat.postMessage", channel=channel, text=msg)
            else:
                print "Error: {}".format(channel)
        self.send_slack_message = False
            

def get_channel_id(name):
    # helper function that get's a channel's ID for use in other API calls
    response = client.api_call('channels.list')
    response = json.loads(response)

    if response['ok'] == True:
        for channel in response['channels']:
            if channel['name'] == name:
                return True, channel['id']
        return False, "Channel not found"

    return False, response['error']
