from flask import Flask, request, jsonify, render_template
import requests
from pyngrok import ngrok
import folium
from folium.plugins import LocateControl


from config import STRAVA_CLIENT_ID, STRAVA_CLIENT_SECRET, VERIFY_TOKEN, AUTH_CODE


app = Flask(__name__)


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
    print('trying to verify')
    mode      = request.args.get('hub.mode')
    token     = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')

    if mode == 'subscribe' and token == VERIFY_TOKEN:
        app.logger.info("WEBHOOK_VERIFIED")
        # Echo back the challenge string:
        return jsonify({'hub.challenge': challenge})
    else:
        return ("", 403)

@app.route('/webhook', methods=['POST'])
def webhook():
    """
    Strava will POST events here once verified.
    Just ACK with 200 + text 'EVENT_RECEIVED'.
    """
    event = request.get_json()
    app.logger.info("Event received: %s", event)
    print(f"Event uploaded: {event}")
    return ("EVENT_RECEIVED", 200)

def create_subscription(callback_url):
    """
    Call Strava's API to subscribe your app.  You only need
    to run this once (or whenever you restart ngrok's URL).
    """

    print('trying to create subscription')
    resp = requests.post(
        "https://www.strava.com/api/v3/push_subscriptions",
        data={
            'client_id': STRAVA_CLIENT_ID,
            'client_secret': STRAVA_CLIENT_SECRET,
            'callback_url': f'{callback_url}/webhook',
            'verify_token': VERIFY_TOKEN,
        }
    )
    print(resp.status_code, resp.text)
    resp.raise_for_status()
    print("Subscription created:", resp.json())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)