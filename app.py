from flask import Flask, render_template
from pyngrok import ngrok
import folium
from folium.plugins import LocateControl

app = Flask(__name__)

# this is a decorator that turns a regular python function into a Flask "view function"
# which converts the functions return value into an http response to be displayed by an http client,
# such as a web browser
# the argument '/' signifies that this function will respond to web requests for the url '/',
# which is the main url
@app.route("/")
def index():
    m = folium.Map(location=(0,0))

    LocateControl(auto_start=True,
                  circleStyle = {'interactive': True},
                    locateOptions={
                        'watch': True,
                        'enableHighAccuracy': True,
                        'timeout': 10000,
                        'maximumAge': 0
                        }
                  ).add_to(m) #
    
    return render_template("map.html", map_html=m.get_root().render())



if __name__ == "__main__":
    ngrok.kill()
    # 1) Open an ngrok tunnel on port 5000
    # for some reason this gives an error; instead I just start in manually from the command line
    # ngrok http 5000
    # public_url = ngrok.connect(5000, bind_tls=True)
    # print(" * ngrok tunnel:", public_url)

    # 2) Run Flask as usual
    app.run(host="0.0.0.0", port=5000, debug=True)

