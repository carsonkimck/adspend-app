from requests.api import request
from requests_oauthlib import OAuth2Session
from sqlalchemy.sql.expression import text
import etsyauth, googleauth, main, config 
import requests
from flask import session
import json


sheet_template_id = config.sheet_template_id 

def createNewSheet():
    user = main.current_user 
    oauth = OAuth2Session(config.google_api_key , token=session.get("google_token"))
    
    # attempt to connect to Google, see if token is fresh
  
    # create a new spreadsheet
    r = oauth.post("https://sheets.googleapis.com/v4/spreadsheets/")
    text_response = r.text
    result = json.loads(text_response)
    newSheetId = result['spreadsheetId']

    # copy template to newly created spreadsheet
    request_body = {
        "destinationSpreadsheetId": newSheetId
    }

  
    r = oauth.post("https://sheets.googleapis.com/v4/spreadsheets/{spreadsheetId}/sheets/{sheetId}:copyTo".format(
        spreadsheetId=sheet_template_id, sheetId=0),data=request_body)
    text_response = r.text
    
    # prepare the request body for update
    request_body =  {
        "requests": [
            {
            "updateSpreadsheetProperties": {
                "properties": {
                "title": "Ad Spend Tracker"
                },
                "fields": "title"
            }
            },
            {
            "deleteSheet": {
                "sheetId": 0,
            }
            }
        ], 
        "includeSpreadsheetInResponse": True
        }

    # update the spreadsheet (rename and delete unused blank sheet)
    r = oauth.post("https://sheets.googleapis.com/v4/spreadsheets/{newSheetId}:batchUpdate".format(newSheetId=newSheetId),
                    data=json.dumps(request_body))
    
    result = json.loads(r.text)
   
    # store spreadsheet ID
    user_ = main.User.query.filter_by(username=user.username).first()
    user_.spreadsheetId = newSheetId
    a = main.db.session.commit()

    # return spreadsheet url 
    sheetURL =  updateSheet(newSheetId)
    return sheetURL

# add charges to sheet, pull from Etsy, Pinterest, Google, etc.
def updateSheet(spreadsheet_id):

    user = main.current_user
    accounts = {"Etsy": ["C4", 0], "Google": ["C5", 0], "Pinterest": ["C6", 0] }

    # Add Etsy Charges
    etsyCharges = etsyauth.getEtsyCharges(user.etsy_key, user.etsy_secret)
    accounts["Etsy"][1] = 5000

    # Add GoogleAds Charges
    googleAdsCharges = googleauth.getGoogleAdsCharges()
    accounts["Google"][1] = 5000

    # Add Pinterest Charges
    # pinterestCharges = pinterestAuth.getPinterestCharges()
    # accounts["Pinterest"][1] = 5000

    # update all account charges! 
    google = OAuth2Session(config.google_api_key, token=session.get("google_token"))
  
    keys = accounts.keys()
    print(keys)

    for key in keys:
        range = accounts[key][0]
        value = accounts[key][1]

        r = google.get("https://sheets.googleapis.com/v4/spreadsheets/{id}/values/{range}".format(
            id=spreadsheet_id, range=range)
        )

        result = json.loads(r.text)
        if result.get("values") == None:
            existing_charges = 0 
        else:
            # flatten and format string, convert to float
            string = ((flatten_list(result["values"])[0]))
            string = string.replace("$", '')
            string = string.replace(",", '')
            existing_charges = float(string)
        
        # just update with current monthly total, if there's already value there
        if existing_charges != 0:
            total = value

        request_body = {
            "values": [
                [total]
            ] }

        payload = {"valueInputOption": "USER_ENTERED" }

        r = google.put("https://sheets.googleapis.com/v4/spreadsheets/{id}/values/{range}".format(
            id=spreadsheet_id, range=range), params=payload, data=json.dumps(request_body))
        
        result = json.loads(r.text)
        print(r.text)

    r = google.get("https://sheets.googleapis.com/v4/spreadsheets/%s" % spreadsheet_id) 
    result = json.loads(r.text)
    url = result["spreadsheetUrl"]
    return url


def flatten_list(_2d_list):
    flat_list = []
    # Iterate through the outer list
    for element in _2d_list:
        if type(element) is list:
            # If the element is of type list, iterate through the sublist
            for item in element:
                flat_list.append(item)
        else:
            flat_list.append(element)
    return flat_list





