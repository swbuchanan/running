from flask import Flask, request, jsonify, render_template
import requests
from pyngrok import ngrok
import folium
from folium.plugins import LocateControl
from register_webhook import authorize
from strava2gpx import strava2gpx
import _asyncio


from config import STRAVA_CLIENT_ID, STRAVA_CLIENT_SECRET, VERIFY_TOKEN, AUTH_CODE, REFRESH_TOKEN


app = Flask(__name__)

# TODO: consider moving this and related to another file
def get_activity_data(activity_id, access_token):
    url = f"https://www.strava.com/api/v3/activities/{activity_id}/streams"
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {
        "keys":     "time, latlng",
        "key_by_type": True
    }
    resp = requests.get(url, headers=headers, params=params)
    resp.raise_for_status()
    return resp.json()


def fetch_activity_summary(activity_id, access_token):
    url = f"https://www.strava.com/api/v3/activities/{activity_id}"
    headers = {"Authorization": f"Bearer {access_token}"}
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    return resp.json()



@app.route("/")
def index():
    """
    This creates the map with the live view.
    """

    # m = folium.Map(location=(0,0),prefer_canvas=True)

    # LocateControl(auto_start=True,
    #               circleStyle = {'interactive': True},
    #                 locateOptions={
    #                     'watch': True,
    #                     'enableHighAccuracy': True,
    #                     'timeout': 10000,
    #                     'maximumAge': 0,
    #                     'prefer_canvas': True
    #                     }
    #               ).add_to(m) #
    # # html = m.get_root().render()
    # # html = html.replace(
    # #     'L.map(',
    # #     'L.map( /* injected */ {preferCanvas: true,},'
    # # )
    # # with open('all_routes.html','w') as f:
    # #     f.write(html)
    # return render_template("all_routes.html", map_html=html)
    return render_template("live.html")



@app.route('/webhook', methods=['GET'])
def verify():
    """
    Strava calls this GET to verify your endpoint.
    You must echo back the hub.challenge when they
    send hub.mode=subscribe & hub.verify_token matches.
    """
    print('Trying to verify')
    mode      = request.args.get('hub.mode')
    token     = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')

    if mode == 'subscribe' and token == VERIFY_TOKEN:
        app.logger.info("WEBHOOK_VERIFIED")
        # Echo back the challenge string:
        return jsonify({'hub.challenge': challenge})
    else:
        return ("", 403)

# this is called when an event is uploaded
@app.route('/webhook', methods=['POST'])
def webhook():
    """
    Strava will POST events here once verified.
    Just ACK with 200 + text 'EVENT_RECEIVED'.
    """
    event = request.get_json()
    app.logger.info("Event received: %s", event)
    print(f"Event uploaded: {event}")

    if event.get('object_type') == 'activity' and event.get('aspect_type') == 'create':
        activity_id = event['object_id']

        token = authorize()

        summary = fetch_activity_summary(activity_id, token)
        app.logger.info(f"New activity of type {summary['type']}: {summary}")

        streams = get_activity_data(activity_id, token)
        print(f'got the activity streams: {streams}')
        coords = streams['latlng']['data']
        times = streams['time']['data']

        print("attempting to save activity")
        save_gpx(activity_id)

        # print(f"coords: {coords}")

    return ("EVENT_RECEIVED", 200)


# def get_tunnel_url():
#     data = requests.get("http://127.0.0.1:4040/api/tunnels").json()
#     # find the HTTPS tunnel
#     for t in data["tunnels"]:
#         if t["proto"] == "https":
#             print(f'Found {t}')
#             return t["public_url"]
#     raise RuntimeError("No HTTPS ngrok tunnel found")

# # this is done in register_webhook.py
# # @app.before_request
# def ensure_strava_subscription():
#     print('debug')
#     app.before_request_funcs[None].remove(ensure_strava_subscription) # remove the decorator so this function is actually only called before the very first request
#     public_url = get_tunnel_url()
#     create_subscription(public_url)   # your function that POSTS to Strava

# def create_subscription(callback_url):
#     """
#     Call Strava's API to subscribe your app.  You only need
#     to run this once (or whenever you restart ngrok's URL).
#     """

#     print('trying to create subscription')
#     resp = requests.post(
#         "https://www.strava.com/api/v3/push_subscriptions",
#         data={
#             'client_id': STRAVA_CLIENT_ID,
#             'client_secret': STRAVA_CLIENT_SECRET,
#             'callback_url': f'{callback_url}/webhook',
#             'verify_token': VERIFY_TOKEN,
#         }
#     )
#     print(resp.status_code, resp.text)
#     resp.raise_for_status()
#     print("Subscription created:", resp.json())

async def save_gpx(activity_id):
    s2g = strava2gpx(STRAVA_CLIENT_ID, STRAVA_CLIENT_SECRET, REFRESH_TOKEN)
    s2g.connect()
    s2g.write_to_gpx(activity_id, "s2gtestoutput")

if __name__ == '__main__':

    app.run(host='0.0.0.0', port=5000, debug=True)