import main, config
import requests
from requests_oauthlib import OAuth1, OAuth1Session
from flask import session
from datetime import datetime
import time




api_key = config.etsy_api_key
secret_key = config.etsy_secret_key
callback_uri = config.etsy_callback_uri 

# Fetch Request Token 
def authorizeEtsy():
    # if user hasn't authorized yet, set the resource owner tokens and allow them to access link. 
    oauth = OAuth1Session(api_key, client_secret=secret_key, callback_uri=callback_uri)
    request_token_url = "https://openapi.etsy.com/v2/oauth/request_token?scope=email_r%20billing_r%20shops_rw"
    fetch_response = oauth.fetch_request_token(request_token_url)

    login_url = fetch_response.get('login_url')
    
    session['resource_key'] = fetch_response.get('oauth_token')
    session['resource_secret'] = fetch_response.get('oauth_token_secret')
    session["etsy_url"] = login_url
    
    return login_url

# Fetch Access Token 
def fetchToken(verifier, user): 
    oauth = OAuth1Session(api_key,
                            client_secret=secret_key,
                            resource_owner_key=session['resource_key'],
                            resource_owner_secret=session['resource_secret'],
                            verifier=verifier)

    access_url = "https://openapi.etsy.com/v2/oauth/access_token"
    oauth_tokens = oauth.fetch_access_token(access_url)
   
    # store oauth token to user in persistent db
    oauth_key = oauth_tokens.get('oauth_token')
    oauth_secret = oauth_tokens.get('oauth_token_secret')
    user_ = main.User.query.filter_by(username=user.username).first()
    user_.etsy_key = oauth_key
    user_.etsy_secret = oauth_secret
    main.db.session.commit()
  
# Access Protected Resources
def getEtsyCharges(etsy_key, etsy_secret):

    alex_etsy = "3f7681cf8f9a4661466b21f70ebae7"
    alex_secret = "ddf61fb0c5"


    carson_etsy = "7442f6bf367425fda17ef1fe410e8a"
    carson_secret = "977378e010"

    headeroauth = OAuth1(api_key, secret_key,
                        alex_etsy, alex_secret,
                        signature_type='auth_header')


    '''headeroauth = OAuth1(api_key, secret_key,
                        etsy_key, etsy_secret,
                        signature_type='auth_header')
                       '''


    month_begin = datetime(year=datetime.now().year, month=datetime.now().month, day=1, hour=0, second=0).timestamp()
    month_end = time.time()

    print(month_begin)
    print(month_end)

    user_id = "464320483"
    get_profile = 'https://openapi.etsy.com/v2/users/464320483/profile'
  
    get_charges = "https://openapi.etsy.com/v2/users/464320483/charges"

    payload = {"min_created": month_begin, "max_created" : month_end}

    get_shop = 'https://openapi.etsy.com/v2/shops/28523366'
    get_billing = "https://openapi.etsy.com/v2/users/464320483/billing/overview"

    print(carson_etsy)
    print(carson_secret)
    r = requests.get(url=get_charges, auth=headeroauth, params=payload)
    print("hellooo")
    print(r.text)
    


    return r

     #shop_id = 28523366






