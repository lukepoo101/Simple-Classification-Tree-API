import json

import requests

##Get new/up-to-date client code
client_code = json.loads(requests.get("https://nameless-harbor-82110.herokuapp.com/update").content)

##write new code to file
with open("Client.py", "w") as client:
    client.write(client_code["update"])