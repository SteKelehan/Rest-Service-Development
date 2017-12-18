#!/usr/local/bin/python3

# This check the number of access has not gone over your daily lim!
import requests
import json

with open ("Tokens.txt", "r") as f:
    token = f.read().split()[0]
payload = {"access_token" : token}
address = "https://api.github.com/rate_limit"
r = json.loads(requests.get(address, params=payload).text)
if "resources" in r:
    core = r["resources"]["core"]
    for key in core:
        print ("{}: {}".format(key, core[key]))
else:
    print ("r:", r)
