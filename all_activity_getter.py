from strava2gpx.src.strava2gpx import strava2gpx
import asyncio

from config import STRAVA_CLIENT_ID, STRAVA_CLIENT_SECRET, VERIFY_TOKEN, AUTH_CODE, REFRESH_TOKEN

async def main():
    '''
    put in your Strava Api client_id, refresh_token, and client_secret
    '''

    # create an instance of strava2gpx
    s2g = strava2gpx(STRAVA_CLIENT_ID, STRAVA_CLIENT_SECRET, REFRESH_TOKEN)

    # connect to the Strava API
    await s2g.connect()

    # get a list of all user's Strava activities
    activities_list = await s2g.get_activities_list()  
    print(activities_list)

    for activity in activities_list:
        activity_id = activity[1]
        activity_type = activity[-1].lower()
        timestamp = activity[-2]
        if activity_type == 'run':
            try:
                await s2g.write_to_gpx(activity_id, f"run_{timestamp}")
            except Exception:
                print(f'failed to get activity {activity_id}')
                continue

if __name__ == '__main__':
    asyncio.run(main())