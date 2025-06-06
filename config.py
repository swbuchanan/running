
# here we load the ENV vars: STRAVA_CLIENT_ID, CLIENT

from dotenv import load_dotenv
import os

load_dotenv()
STRAVA_CLIENT_ID    = os.environ['STRAVA_CLIENT_ID']
STRAVA_CLIENT_SECRET= os.environ['STRAVA_CLIENT_SECRET']
VERIFY_TOKEN        = os.environ['STRAVA_VERIFY_TOKEN']
AUTH_CODE           = os.environ['AUTH_CODE']
ACCESS_TOKEN        = os.environ['ACCESS_TOKEN']
REFRESH_TOKEN       = os.environ['REFRESH_TOKEN']
