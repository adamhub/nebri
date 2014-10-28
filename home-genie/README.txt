Home Genie Home Automation
==========================

First, to use this script you will have to set up an email account for Home Genie to use. To do this do the following:
Home > Configure > Automation > Messaging and Social > E-mail Account > Enter relevant information here

Add the scripts to Home Genie by doing the following:
Home > Configure > Automation > Add Group (name it Nebri or whatever you want) > Enter Group > Actions > Add new program (name it motion sensor) > Program Type to C# > copy code from home-genie-script/action.cs into Program Code > Compile > copy code from home-genie-script/condition.cs into Trigger Code > Compile

Be sure to change email and sensor names and the like to match your setup.

Add the simple NebriOS script to your NebriOS instance and trigger the motion sensor.
