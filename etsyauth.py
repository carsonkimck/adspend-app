import config
import requests
from typing import Text
import json
from requests_oauthlib import OAuth1, OAuth1Session
from flask import Flask, render_template


api_key = config.etsy_api_creds["api_key"]
secret_key = config.etsy_api_creds["secret_key"]

access_key = config.etsy_access_token["access_key"]
access_secret = config.etsy_access_token["access_secret"]

# Fetch Request Token 

oauth = OAuth1Session(api_key, client_secret=secret_key)

request_token_url = "https://openapi.etsy.com/v2/oauth/request_token?scope=email_r%20billing_r"
fetch_response = oauth.fetch_request_token(request_token_url)

login_url = fetch_response.get('login_url')
resource_owner_key = fetch_response.get('oauth_token')
resource_owner_secret = fetch_response.get('oauth_token_secret')

print("login url: " + login_url)

# Click authorization link, get Verifier
verifier = input("Please enter your verification code: ")



# Fetch Access Token 
oauth = OAuth1Session(api_key,
                        client_secret=secret_key,
                        resource_owner_key=resource_owner_key,
                        resource_owner_secret=resource_owner_secret,
                        verifier=verifier)

access_url = "https://openapi.etsy.com/v2/oauth/access_token"
oauth_tokens = oauth.fetch_access_token(access_url)
print(oauth_tokens)

resource_owner_key = oauth_tokens.get('oauth_token')
resource_owner_secret = oauth_tokens.get('oauth_token_secret')

print(resource_owner_key)
print(resource_owner_secret)

# Access Protected Resources
headeroauth = OAuth1(api_key, secret_key,
                     access_key, access_secret,
                     signature_type='auth_header')

get_charges = 'https://openapi.etsy.com/v2/users/509187507/charges?min_created=1626400643'

r = requests.get(url=get_charges, auth=headeroauth)
print(r.text)


