import etsyauth
import main


def getSheet():
# server gets oauth creds, makes requests to platforms and gets ad spend data
    print("hello buddy!")
    user = main.current_user 
    charges = etsyauth.getEtsyCharges(user.etsy_key, user.etsy_secret)

    print(charges.text)

    # ad spend data is then sent to a new google sheet that is created (or updates one that already exists)




