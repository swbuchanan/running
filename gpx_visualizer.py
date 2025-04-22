import gpxpy
import glob
import folium

runs = {}

for gpx_path in glob.glob("gpx/*.gpx"):
    print("Found GPX file:", gpx_path)
    


# 1. Parse your GPX file
    with open(gpx_path, "r") as gpx_file:
        gpx = gpxpy.parse(gpx_file)

# 2. Extract all track‑point coordinates
    coords = []
    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                coords.append((point.latitude, point.longitude))

    runs[gpx_path] = coords

    # 3. Compute a center for the initial map view
    avg_lat = sum(lat for lat, lon in coords) / len(coords)
    avg_lon = sum(lon for lat, lon in coords) / len(coords)

# 4. Build the Folium map
    m = folium.Map(location=(avg_lat, avg_lon), zoom_start=13)

# 5. Add the route as a polyline
    for gpx_path, coords in runs.items():
        # Add the GPX route as a polyline
        folium.PolyLine(coords, weight=5, opacity=0.7).add_to(m)

# (Optional) Mark start/end
# folium.Marker(coords[0], tooltip="Start").add_to(m)
# folium.Marker(coords[-1], tooltip="Finish").add_to(m)

# 6. Save out to HTML
m.save("gpx_route.html")
print("Map saved to gpx_route.html")

