import odesk

def api_authorization():

    print """
        Use 
        https://www.odesk.com/services/api/keys
        for getting API keys for your app.
        It can take up to 24 hours to get your keys.
        Use "desktop" application type for your API keys request.
        """

    public_key = raw_input('Please enter public key ("Key" field): > ')
    secret_key = raw_input('Please enter secret key ("Secret" field): > ')

    try:
        client = odesk.Client(public_key, secret_key)
        verifier = raw_input(
            '\nPlease enter the verification code you get '
            'following this link:\n{0}\n'
            'You should be logged in as application user\n> '.format(
            client.auth.get_authorize_url()))
    except Exception, e:
        print "Something went wrong, please check entered keys"
        return



    print 'Getting tokens'

    try:
        access_token, access_token_secret = client.auth.get_access_token(verifier)
    except Exception, e:
        print "Something went wrong, please check verification code is correct"
        return
    
    try:
        client = odesk.Client(public_key, secret_key,
                              oauth_access_token=access_token,
                              oauth_access_token_secret=access_token_secret)
    except Exception, e:
        print "Something went wrong, looks like tokens aren't ok, check them"
        return

    print 'Use following information for API usage:'
    print 'oauth_access_token: "{0}"'.format(access_token)        
    print 'oauth_access_token_secret: "{0}"'.format(access_token_secret)


if __name__ == '__main__':
    client = api_authorization()




