# -*- coding: utf-8 -*-
"""DestinyItemTracker.ipynb

Automatically generated by Colab.
"""

#@title Import & Const Def

import json
import os
import requests
import time
import datetime

API_KEY = None # @param {type:"string", placeholder:"API Key"}
CLIENT_ID = None # @param {type:"string", placeholder:"Client ID"}
BASE_URL = "https://www.bungie.net/Platform"
AUTH_TOKEN_URL = "https://www.bungie.net/platform/app/oauth/token/"

KNOWN_IDS = {
    3655393761: "Titan",
    671679327: "Hunter",
    2271682572: "Warlock",
}
BUCKET_Consumables = 1469714392
BUCKET_Modifications = 1469714392
BUCKET_General = 138197802 # Vault

#@title OAuth2 Step 1
token_state = os.urandom(16).hex()
print("Auth using the following url, then paste the code of redirected url in the next cell")
print(f"https://www.bungie.net/en/oauth/authorize?client_id={CLIENT_ID}&response_type=code&state={token_state}")

#@title OAuth2 Step 2
AUTH_CODE = "None" # @param {type:"string", placeholder:"code=<value> part of the url"}

resp = requests.post(AUTH_TOKEN_URL,
    headers= {
      "Content-Type": "application/x-www-form-urlencoded",
      "X-API-Key": API_KEY,
    },
    data = {"grant_type":"authorization_code","client_id":f"{CLIENT_ID}","code":f"{AUTH_CODE}"}
)
AUTH_INFO = resp.json()
AUTH_TOKEN = AUTH_INFO["access_token"]
AUTH_TOKEN_TYPE = AUTH_INFO["token_type"]

#@title Load characters

def bungie_get(apipath):
  resp = requests.get(BASE_URL + apipath,
    headers= {
      "Content-Type": "application/x-www-form-urlencoded",
      "X-API-Key": API_KEY,
      "Authorization": f"{AUTH_TOKEN_TYPE} {AUTH_TOKEN}"
    })
  if resp.status_code != 200:
    print("Auth expired?", resp)
  return resp

def load_membership():
  resp = bungie_get("/User/GetMembershipsForCurrentUser/").json()
  membership_id = resp["Response"]["primaryMembershipId"]
  for m in resp["Response"]["destinyMemberships"]:
    if m["membershipId"] == resp["Response"]["primaryMembershipId"]:
      return m["membershipType"], membership_id

MEMBERSHIP_TYPE, MEMBERSHIP_ID = load_membership()
print(f"/Destiny2/{MEMBERSHIP_TYPE}/Profile/{MEMBERSHIP_ID}")
CHARACTERS_DATA = bungie_get(f"/Destiny2/{MEMBERSHIP_TYPE}/Profile/{MEMBERSHIP_ID}/?components=200").json()["Response"]["characters"]["data"]
CHARACTERS = tuple(CHARACTERS_DATA.keys())
for cid, c in CHARACTERS_DATA.items():
  print(KNOWN_IDS[c["classHash"]], f"/Destiny2/{MEMBERSHIP_TYPE}/Profile/{MEMBERSHIP_ID}/Character/{cid}/")

#@title Tracking data
items_log = []
all_items, all_items_ts = None, 0.0

#@title Utils

def get_ts(s):
  return datetime.datetime.strptime(s, "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=datetime.timezone.utc).timestamp()

def get_all_items():
  items = []
  resp = bungie_get(f"/Destiny2/{MEMBERSHIP_TYPE}/Profile/{MEMBERSHIP_ID}/?components=102").json()
  ts = get_ts(resp["Response"]["responseMintedTimestamp"])
  items.extend(resp["Response"]["profileInventory"]["data"]["items"])
  for cid in CHARACTERS:
    resp = bungie_get(f"/Destiny2/{MEMBERSHIP_TYPE}/Profile/{MEMBERSHIP_ID}/Character/{cid}/?components=201,205").json()
    items.extend(resp['Response']['inventory']['data']['items'])
    items.extend(resp['Response']['equipment']['data']['items'])
  return items, ts

def to_item_instance_dict(items):
  return {item['itemInstanceId']:item for item in items if 'itemInstanceId' in item}

def refresh_tracked(items, ts):
  now = datetime.datetime.now().timestamp()
  new_items, new_ts = get_all_items()
  if new_ts < ts:
    print(f"# Ignoring new response, new ts {new_ts} < old ts {ts}")
    return items, ts
  print(f"# Update at {now}")
  prev = to_item_instance_dict(items)
  curr = to_item_instance_dict(new_items)
  for iid in curr.keys() - prev.keys():
    items_log.append(("new", now, curr[iid]))
    item = curr[iid]
    print(now, "new", {"item":iid, "hash":item.get('itemHash', None)})
  for iid in prev.keys() - curr.keys():
    items_log.append(("deleted", now, prev[iid]))
    item = prev[iid]
    print(now, "deleted", {"item":iid, "hash":item.get('itemHash', None)})
  return new_items, new_ts

QUERY_INTERVAL = 30
while True:
  if all_items is None:
    all_items, all_items_ts = get_all_items()
    time.sleep(QUERY_INTERVAL)
  all_items, all_items_ts = refresh_tracked(all_items, all_items_ts)
  time.sleep(QUERY_INTERVAL)