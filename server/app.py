from flask import Flask
from server.routes import live, map, webhook

def create_app():
    app = Flask(__name__)
    app.register_blueprint(live.bp)
    app.register_blueprint(map.bp)
    app.register_blueprint(webhook.bp)
    return app
