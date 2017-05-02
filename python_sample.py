# In this file we will be doing the following ....
# 1. Connect to the oauth server and retrieve a token
# 2. Use this token to connect to the API itself
# 3. Get a response from the API
# 4. Wait two minutes and connect again 


import requests
import time
import datetime
from contextlib import suppress


# These values will be given to you once you have registered with NZ Post and requested application access
# Please follow the instruction here
# 
client_id = "<your client id>"
client_secret = "<your client id>"
grant_type = "your grant type"
username = "your username"
password = "your passowrd"

base_oauth_url = "https://oauth.nzpost.co.nz/as/token.oauth2?client_id="


#Once the values above are populated the code will attempt to connect and retrieve an access token 
print ("Fetching an access token ...")
response = requests.request("POST", base_oauth_url + client_id + '&client_secret=' + client_secret + '&grant_type=' + grant_type + '&username=' + username + '&password=' + password)
bearer_token_start = response.text.find(':') + 2
bearer_token_end = response.text.find('"', bearer_token_start)
bearer_token = response.text[bearer_token_start:bearer_token_end]

#The access token is now stored in a variable called bearer_token (both terms are used which is why they are included here)
print ("Access token is " + bearer_token)


#Once we have the token we now setup the variables we will use to call the API
#The payload below is just a sample json paylod - please consult the api docs for all the requirements conerning calling the API's
url = "https://api.uat.nzpost.co.nz:443/parcelredirect/v1/parcelredirect"

payload = "{\"tracking_reference\": \"CT097701231NZ\",	\"receiver_details\": {		\"name\": \"Joe Blogg\",		\"phone\": \"+641234567\",		\"reference\": \"Order 5423\"	},	\"delivery_address\": {		\"company_name\": \"Beta Company\",		\"building_name\": \"Beta Company House\",		\"unit_type\": \"Suite\",		\"unit_value\": \"5\",		\"floor\": \"3\",		\"street\": \"42C Tawa Drive\",		\"suburb\": \"Albany\",		\"city\": \"Auckland\",		\"postcode\": \"0632\",		\"country_code\": \"NZ\"	},	\"redirect_address\": {		\"site_code\": 44111	}}"
headers = {
    'client_id': client_id,
    'authorization': "Bearer " + bearer_token,
    'content-type': "application/json",
    "username": username
    }



#We will now attempt to connect to the API - in this case it is the Parcel Redirect API
def call_api():
   print ("Calling Reirect API ...")
   print('Timestamp: {:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()))
   response = requests.request("POST", url, data=payload, headers=headers)
   print(response.text)        

x = 1
while True:
    call_api()
    time.sleep(120)
    with suppress(Exception):
        call_api()
