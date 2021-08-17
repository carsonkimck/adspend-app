from requests_oauthlib import OAuth2Session
from sqlalchemy.sql.expression import text
import etsyauth, main, config 
import requests
from flask import session
import json

sheet_template_id = config.sheet_template_id 

def createNewSheet():
    user = main.current_user 
    charges = etsyauth.getEtsyCharges(user.etsy_key, user.etsy_secret)

    oauth = OAuth2Session(config.goog_api_creds["api_key"], token=session.get("google_token"))
    
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
        spreadsheetId=sheet_template_id, sheetId=0), data=request_body)
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
    print(r.text)
    result = json.loads(r.text)
    print(result)

    # return spreadsheet url 
    sheetURL = result['updatedSpreadsheet']['spreadsheetUrl']
    return sheetURL


# add charges to sheet, pull from Etsy, Pinterest, Google, etc.
def updateSheet(spreadsheet_id):
    pass




