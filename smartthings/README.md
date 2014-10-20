# Smart Thing NebriOS

These scripts will allow you to control your smart things devices from NebriOS.
## Setup

1. First, you create an app on smart things using our modified IOTDB bridge app. These scripts can be found in the iotdb folder found [here](https://github.com/adamhub/nebri/tree/master/smartthings/iotdb).

2. Give OAuth access to this app from inside SmartThings so NebriOS can communicate with it. More information on setting up these steps can be found here: https://github.com/dpjanes/iotdb-smartthings

3. Add the included scripts and forms to your NebriOS instance. Be sure to change relevant information, namely the instance_name in the st_authorize script.


## Running The Flow

1. Obtain the OAuth Client ID and Secret for your app from Smart Things. 
2. Enter these values in the St OAuth Keys form in Nebrios.
3. You should receive an email from NerbiOS with a link to authorize the app. Follow the link and authorize the items you would like.You will be redirected to your instance. It may take a few minutes for your device list to populate; after that, you can fill out the SmartThings Send Command form to send commands to any of your authorized devices.

A list of commands can be found here:
https://graph.api.smartthings.com/ide/doc/capabilities

The authorization only needs to be run once, and from that point you can just run commands from the form.
