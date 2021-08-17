import os
from flask import session
import main, config
from typing import Text
from requests_oauthlib import OAuth2Session
from time import time 


os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

api_key = config.goog_api_creds["api_key"]
secret_key = config.goog_api_creds["secret_key"]
redirect_uri = "http://127.0.0.1:8080/home"
scope = ['https://www.googleapis.com/auth/spreadsheets']
token_url = "https://www.googleapis.com/oauth2/v4/token"


def authorizeGoogle():
    oauth = OAuth2Session(api_key, redirect_uri=redirect_uri, scope=scope)
    auth_url = oauth.authorization_url('https://accounts.google.com/o/oauth2/auth', access_type="offline", prompt="consent")
    url = auth_url[0]
    session['oauth_state'] = auth_url[1]
    session['google_url'] = url
    print("Creating state for url... " + session['oauth_state'])
    return url 
   
def fetchToken(url, user):
    oauth = OAuth2Session(api_key, redirect_uri=redirect_uri, state=session['oauth_state'])
    print("we sending this to google" + url)

    token = oauth.fetch_token(
            token_url,
            client_secret=secret_key,
           authorization_response=url,
            )

    print(token)
    print(oauth)
   

    session['google_token'] = token
    session['google_token_expir'] = token['expires_in'] + time()
    session['google_refresh'] = token["refresh_token"]
    

    print(session['google_token_expir'])
    
def refreshToken():
   
    token = session.get('google_token')

    extra = {
        'client_id': api_key,
        'client_secret' : secret_key,
        }

    oauth = OAuth2Session(client_id=api_key, token=token)

    session['google_token'] = oauth.refresh_token(token_url=token_url, refresh_token=session["google_refresh"],
    **extra)

def getGoogleAdsCharges():
    return 5000