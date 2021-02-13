import json

import requests

##Get new/up-to-date client code
client_code = json.loads(requests.get("http://127.0.0.1:5800/update").content)

##write new code to file
with open("Client.py", "w") as client:
    client.write(client_code["update"])