from flask import Flask, render_template
from pyngrok import ngrok
import folium
from folium.plugins import LocateControl

app = Flask(__name__)

@app.route("/")
def index():
    m = folium.Map(location=[0,0], zoom_start=2)
    LocateControl(auto_start=True).add_to(m)
    return render_template("map.html", map_html=m.get_root().render())

if __name__ == "__main__":
    # 1) Open an ngrok tunnel on port 5000
    public_url = ngrok.connect(5000, bind_tls=True)
    print(" * ngrok tunnel:", public_url)

    # 2) Run Flask as usual
    app.run(host="0.0.0.0", port=5000, debug=True)

