#!/usr/bin/env python3
import os, requests, time

# Load CLIENT_ID, CLIENT_SECRET, VERIFY_TOKEN from os.environ
from config import STRAVA_CLIENT_ID, STRAVA_CLIENT_SECRET, VERIFY_TOKEN, AUTH_CODE

# 1) Wait until your app is up
time.sleep(1)

# 2) Discover your ngrok URL
info = requests.get("http://127.0.0.1:4040/api/tunnels").json()
public_url = next(t["public_url"] for t in info["tunnels"] if t["proto"]=="https")

print('trying to auth')
resp = requests.post('https://www.strava.com/oauth/token', data={
    'client_id':     STRAVA_CLIENT_ID,
    'client_secret': STRAVA_CLIENT_SECRET,
    'code':          AUTH_CODE,
    'grant_type':    'authorization_code'
}).json()
print(resp)
access_token = resp['access_token']
print(f'access_token: {access_token}')



# 3) POST to Strava
resp = requests.post(
  "https://www.strava.com/api/v3/push_subscriptions",
  json={
    "client_id": STRAVA_CLIENT_ID,
    "client_secret": STRAVA_CLIENT_SECRET,
    "callback_url": f"{public_url}/webhook",
    "verify_token": VERIFY_TOKEN
  }
)
print("Status:", resp.status_code, resp.text)
resp.raise_for_status()
