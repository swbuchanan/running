from flask import Flask, request, jsonify
import requests

from config import STRAVA_CLIENT_ID, STRAVA_CLIENT_SECRET, VERIFY_TOKEN, AUTH_CODE


app = Flask(__name__)


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
    # 1) Start ngrok first so you know public_url
    # from pyngrok import ngrok
    # public_url = ngrok.connect(5000, bind_tls=True)
    # print(" * ngrok tunnel:", public_url)

#     public_url = '''
# https://993a-150-203-68-68.ngrok-free.app
# '''

    # 2) Optionally auto-register your webhook:

    # 3) Run your Flask server
    app.run(host='0.0.0.0', port=5000, debug=True)

    # create_subscription(public_url)
