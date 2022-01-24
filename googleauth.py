import os
from flask import session
import main, config
from typing import Text
from requests_oauthlib import OAuth2Session
from time import time 
import json
import requests



os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

api_key = config.google_api_key
secret_key = config.google_secret_key
redirect_uri = config.google_callback_uri
scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/adwords']
token_url = "https://www.googleapis.com/oauth2/v4/token"


def authorizeGoogle():
    oauth = OAuth2Session(api_key, redirect_uri=redirect_uri, scope=scope)
    auth_url = oauth.authorization_url('https://accounts.google.com/o/oauth2/auth', access_type="offline", prompt="consent")
    url = auth_url[0]
    session['oauth_state'] = auth_url[1]
    session['google_url'] = url
    
    # sets the session to accept the Google code in redirect uri 
    session['auth_code_type'] = 'google'
    return url 
   
def fetchToken(url, user):
    oauth = OAuth2Session(api_key, redirect_uri=redirect_uri, state=session.get('oauth_state'))

    token = oauth.fetch_token(
            token_url,
            client_secret=secret_key,
           authorization_response=url,
            )


    session['google_token'] = token
    session['google_token_expir'] = token['expires_in'] + time()
    session['google_refresh'] = token["refresh_token"]
    
    
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
    payload = {"query" : ''' 
                SELECT
                campaign.name,
                campaign.status,
                segments.device,
                metrics.impressions,
                metrics.clicks,
                metrics.ctr,
                metrics.average_cpc,
                metrics.cost_micros
                FROM campaign
                WHERE segments.date DURING THIS_MONTH
            '''
    }
    
    customer_id = "491-551-6145"
    url = "https://googleads.googleapis.com/v9/customers/{customer_id}/googleAds:searchStream".format(customer_id=customer_id)


    google = OAuth2Session(config.google_api_key, token=session.get("google_token"))
    r = google.put(url=url, params=payload)

    response = json.loads(r.text)

    print(response)
    cost_micros = response["results"]["metrics.cost_micros"]
    print(cost_micros)
    dollar_spend = cost_micros/1000000
    return dollar_spend
    


    

   # https://developers.google.com/google-ads/api/reference/rpc/v9/Metrics#cost_micros


