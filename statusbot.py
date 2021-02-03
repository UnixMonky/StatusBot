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
# logging.basicConfig(level=logging.DEBUG)

# led blink so we know we've started
ledshim.set_all(255,255,255,.5)
ledshim.show()
time.sleep(0.5)
ledshim.clear()
ledshim.set_pixel(1,255,255,255,.5)
ledshim.show()

config = json.load(open(sys.argv[1]))

# Create a preferably long-lived app instance which maintains a token cache.
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
try:
    oldstatus = "nope"
    while "access_token" in result:
        # Calling graph using the access token
        graph_data = requests.get(config["endpoint"], headers={'Authorization': 'Bearer ' + result['access_token']},).json()
        status = graph_data.get('availability') 
        #print(status)
        if status == "Available":
            # print("Setting to green")
            ledshim.set_all(0,255,0,.5)
            ledshim.show()
            if oldstatus != status:
                print(time.ctime() + " Teams status is: " + str(status) )
            oldstatus = status
            time.sleep(10)
        elif status == "Busy":        
            # print("Setting to red")
            ledshim.set_all(255,0,0,.5)
            ledshim.show()
            if oldstatus != status:
                print(time.ctime() + " Teams status is: " + str(status) )
            oldstatus = status
            time.sleep(10)
        elif status == "DoNotDisturb":        
            # print("Setting to red")
            ledshim.set_all(255,0,0,.5)
            ledshim.show()
            if oldstatus != status:
                print(time.ctime() + " Teams status is: " + str(status) )
            oldstatus = status
            time.sleep(10)
        elif status == "Idle":        
            # print("Setting to red")
            ledshim.set_all(0,255,0,.5)
            ledshim.show()
            if oldstatus != status:
                print(time.ctime() + " Teams status is: " + str(status) )
            oldstatus = status
            time.sleep(10)
        elif status == "Away":        
            # print("Setting to red")
            ledshim.clear()
            ledshim.show()
            if oldstatus != status:
                print(time.ctime() + " Teams status is: " + str(status) )
            oldstatus = status
            time.sleep(10)
        elif status == "Offline":        
            # print("Setting to red")
            ledshim.clear()
            ledshim.show()
            if oldstatus != status:
                print(time.ctime() + " Teams status is: " + str(status) )
            oldstatus = status
            time.sleep(10)
        else:
            ledshim.set_all(0,0,255,.5)
            ledshim.show()
            if oldstatus != status:
                print(time.ctime() + " Teams status is: " + str(status) )
            oldstatus = status
            time.sleep(10)

except KeyboardInterrupt:
    logging.info("Exiting due to keyboard interrupt")
    ledshim.clear()
    ledshim.show()














# if "access_token" in result:
#     # Calling graph using the access token
#     graph_data = requests.get(  # Use token to call downstream service
#         config["endpoint"],
#         headers={'Authorization': 'Bearer ' + result['access_token']},).json()
#     print("Graph API call result: %s" % json.dumps(graph_data, indent=2))
# else:
#     print(result.get("error"))
#     print(result.get("error_description"))
#     print(result.get("correlation_id"))  # You may need this when reporting a bug