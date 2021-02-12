"""
MS Teams Config
The configuration file would look like this:
{
    "authority": "https://login.microsoftonline.com/common",
    "client_id": "your_client_id",
    "scope": ["User.ReadBasic.All"],
    "endpoint": "https://graph.microsoft.com/v1.0/users"
}
    # You can find the other permission names from this document
    # https://docs.microsoft.com/en-us/graph/permissions-reference
    # To restrict who can login to this app, you can find more Microsoft Graph API endpoints from Graph Explorer
    # https://developer.microsoft.com/en-us/graph/graph-explorer
You can then run this sample with a JSON configuration file:

    python sample.py parameters.json
"""

import sys  # For simplicity, we'll read config file from 1st CLI param sys.argv[1]
import json
import logging
import time
import requests
import msal
import ledshim

# Optional logging
logging.basicConfig(level=logging.INFO)
logging.info(time.ctime() + " Starting" )

# set led colors:
green = (0,255,0,.5)
red = (255,0,0,.5)
blue = (0,0,255,.5)
none = (24,255,255,255,.25)


# led blink so we know we've started
ledshim.set_all(255,255,255,.5)
ledshim.show()
time.sleep(0.5)
ledshim.clear()
ledshim.set_pixel(24,255,255,255,.5)
ledshim.show()

logging.info(time.ctime() + " Loading config" )
config = json.load(open(sys.argv[1]))

# Create a preferably long-lived app instance which maintains a token cache.
logging.info(time.ctime() + " Getting token" )
app = msal.PublicClientApplication(
    config["client_id"], authority=config["authority"],
    # token_cache=...  # Default cache is in memory only.
                       # You can learn how to use SerializableTokenCache from
                       # https://msal-python.rtfd.io/en/latest/#msal.SerializableTokenCache
    )


result = app.acquire_token_by_username_password(
    config["username"],
    config["password"],
    config["scope"],
    claims_challenge=None
    )

logging.info(time.ctime() + " Starting status checks" )
try:
    oldstatus = "nope"
    while "access_token" in result:
        # Calling graph using the access token
        graph_data = requests.get(config["endpoint"], headers={'Authorization': 'Bearer ' + result['access_token']},).json()
        status = graph_data.get('availability') 

        if status in [ 'Available' ]:
            ledshim.set_all(0,255,0,.5)
        elif status in [ 'Busy', 'DoNotDisturb']:
            ledshim.set_all(255,0,0,.5)
        elif status in [ 'Idle', 'Away', 'AvailableIdle', 'Offline' ]:
            ledshim.clear()
            ledshim.set_pixel(24,255,255,255,.25)
        else:
            ledshim.set_all(0,0,255,.5)
            result = app.acquire_token_by_username_password(
                config["username"],
                config["password"],
                config["scope"],
                claims_challenge=None
                )
        ledshim.show()
        if oldstatus != status:
            logging.info(time.ctime() + " Teams status is: " + str(status) )
        oldstatus = status
        time.sleep(10)




        # elif status == "Idle":        
        #     ledshim.set_all(0,255,0,.5)
        #     ledshim.show()
        #     if oldstatus != status:
        #         logging.info(time.ctime() + " Teams status is: " + str(status) )
        #     oldstatus = status
        #     time.sleep(10)
        # elif status == "Away":        
        #     ledshim.set_pixel(24,255,255,255,.5)
        #     ledshim.show()
        #     if oldstatus != status:
        #         logging.info(time.ctime() + " Teams status is: " + str(status) )
        #     oldstatus = status
        #     time.sleep(10)
        # elif status == "AvailableIdle":        
        #     ledshim.set_pixel(24,255,255,255,.5)
        #     ledshim.show()
        #     if oldstatus != status:
        #         logging.info(time.ctime() + " Teams status is: " + str(status) )
        #     oldstatus = status
        #     time.sleep(10)
        # elif status == "Offline":        
        #     ledshim.set_pixel(24,255,255,255,.5)
        #     ledshim.show()
        #     if oldstatus != status:
        #         logging.info(time.ctime() + " Teams status is: " + str(status) )
        #     oldstatus = status
        #     time.sleep(10)
        # elif status == "None":        
        #     ledshim.set_pixel(24,255,255,255,.5)
        #     ledshim.show()
        #     if oldstatus != status:
        #         logging.info(time.ctime() + " Teams status is: " + str(status) )
        #     oldstatus = status
        #     time.sleep(10)
        # elif status == "":        
        #     ledshim.set_pixel(24,255,255,255,.5)
        #     ledshim.show()
        #     if oldstatus != status:
        #         logging.info(time.ctime() + " Teams status is: " + str(status) )
        #     oldstatus = status
        #     time.sleep(10)
        # else:
        #     ledshim.set_all(0,0,255,.5)
        #     ledshim.show()
        #     if oldstatus != status:
        #         logging.warning(time.ctime() + " Teams status is: '" + str(status) +"'" )
        #     oldstatus = status
        #     ## assume if we're here that something went wrong and get a new token
        #     result = app.acquire_token_by_username_password(
        #         config["username"],
        #         config["password"],
        #         config["scope"],
        #         claims_challenge=None
        #         )
        #     time.sleep(10)

except KeyboardInterrupt:
    logging.info("Exiting due to keyboard interrupt")
    ledshim.clear()
    ledshim.show()