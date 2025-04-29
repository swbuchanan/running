from flask import Flask
from server.routes import live, map, webhook

def create_app():
    app = Flask(__name__)

    print(f'app created at {__name__}')

    # the app builds a URL-to-function map
    # that is, a routing table so that when an http request comes in, it knows exactly which view function to call
    # app.register_blueprint(live.bp)
    app.register_blueprint(map.bp)
    app.register_blueprint(webhook.bp)
    return app
