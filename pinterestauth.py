import config
import requests
from typing import Text
import json
from requests_oauthlib import OAuth2, OAuth2Session
from flask import Flask, render_template


api_key = config.api_creds["api_key"]
secret_key = config.api_creds["secret_key"]

access_key = config.access_token["access_key"]
access_secret = config.access_token["access_secret"]

redirect_uri = "https://adspend-app.wl.r.appspot.com/"


request_token_url = "https://www.pinterest.com/oauth/?client_id={api_key}&redirect_uri={redirect_uri}&response_type=code".format(api_key=api_key, redirect_uri=redirect_uri)

print(request_token_url)
