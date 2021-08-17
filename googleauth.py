import os
import re 
from flask import session, sessions
from requests.models import Response
import main, config
import requests
from typing import Text
from requests_oauthlib import OAuth2, OAuth2Session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import insert, select, update
from sqlalchemy.sql.functions import count, user
from sqlalchemy.sql import func

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

api_key = config.goog_api_creds["api_key"]
secret_key = config.goog_api_creds["secret_key"]
redirect_uri = "http://127.0.0.1:8080/home"
scope = ['https://www.googleapis.com/auth/spreadsheets']
token_url = "https://www.googleapis.com/oauth2/v4/token"


def authorizeGoogle():
    oauth = OAuth2Session(api_key, redirect_uri=redirect_uri, scope=scope)
    auth_url = oauth.authorization_url('https://accounts.google.com/o/oauth2/auth')
    url = auth_url[0]
    session['oauth_state'] = auth_url[1]
    session['google_url'] = url
    print("Creating state for url..." + session['oauth_state'])
    return url 
   
def fetchToken(url, user):
    print("flag 2" + session['oauth_state'])
    oauth = OAuth2Session(api_key, redirect_uri=redirect_uri, state=session['oauth_state'])
    print("we sending this to google" + url)
    token = oauth.fetch_token(
            token_url,
            client_secret=secret_key,
           authorization_response=url,
            )

    print(type(token))
    # store token in persistent db 
    user_ = main.User.query.filter_by(username=user.username).first()
    print(user_.username)
    session['google_token'] = token
    
def refreshToken():
    def token_updater(token):
        session['google_token'] = token

    extra = {
        'client_id': api_key,
        'client_secret' : secret_key,
        }

    oauth = OAuth2Session(api_key, token=session.get("google_token"), 
    auto_refresh_kwargs=extra, auto_refresh_url=token_url, token_updater=token_updater)

