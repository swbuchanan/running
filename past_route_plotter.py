from pathlib import Path
import folium
from parsers import get_parser_for
from gpxpy.gpx import GPXXMLSyntaxException
import random
import pandas as pd
import json

DIR = 'gpx'

df = pd.DataFrame(columns=['name', 'id', 'coords']) # TODO: I also want to store the date


try:
    df = pd.read_csv('all_routes.csv')
except FileNotFoundError:
    print("Could not find list of past routes. Starting with a new list.")

def plot_route(coords, out_html):
    avg_lat = sum(lat for lat, _ in coords) / len(coords)
    avg_lon = sum(lon for _, lon in coords) / len(coords)
    m = folium.Map(location=(avg_lat, avg_lon), zoom_start=13)
    folium.PolyLine(coords, weight=5, opacity=0.7).add_to(m)
    m.save(out_html)

def main():
    global df

    routes_list = []

    # 1. Collect all GPX, FIT, FIT.GZ files in cwd
    files = [p for p in Path(DIR).iterdir() if p.is_file()]

    # 2. Pick one file to seed the map center
    #    (or just pick a fixed location)
    first = None
    for p in files:
        try:
            # if this succeeds, p is supported
            get_parser_for(p)
            first = p
            break
        except ValueError:
            # unsupported file – skip
            continue
    coords0 = get_parser_for(first).parse(first)
    avg_lat = sum(lat for lat, _ in coords0) / len(coords0)
    avg_lon = sum(lon for _, lon in coords0) / len(coords0)

    # 3. Create one map
    m = folium.Map(location=(avg_lat, avg_lon), zoom_start=12)

    # 4. Overlay each route
    colors = ['red','blue','green','purple','orange','darkred','cadetblue']
    for idx, path in enumerate(files):
        try:
            parser = get_parser_for(path)
        except ValueError:
            continue  # skip unsupported extensions

        try:
            coords = parser.parse(path)
        except GPXXMLSyntaxException:
            print(f"I think there are no coordinates in activity {path}. This may be a treadmill workout.")
            continue

        try:
            folium.PolyLine(
                coords,
                # color=colors[idx % len(colors)],
                color = f'rgb({random.randint(0, 70)}, {random.randint(0, 70)}, {random.randint(200, 255)})',
                weight=3,
                opacity=0.7,
                tooltip=path.name
            ).add_to(m)
            print(f'parsed {path}')
            new_route = {
                'name': path,
                'id': path.name,
                'coords': coords
            }
            # df.append(new_route, ignore_index=True)
            routes_list.append(new_route)
            print(f'added {path} to dataframe')
        except ValueError: # not sure what this is but one time I got ValueError("Locations is empty")
            print('valueerror')
            pass
# 5. (Optional) Add a layer control if you split into FeatureGroups
#    from folium import FeatureGroup, LayerControl
#    # inside loop use fg = FeatureGroup(name=path.name); fg.add_child(...); m.add_child(fg)
#    m.add_child(LayerControl())

# 6. Save single HTML
    m.save('all_routes.html')
    new_routes = pd.DataFrame(routes_list)
    df = pd.concat([df, new_routes])
    df.to_csv('all_routes.csv', index=False)
    print("All routes plotted → all_routes.html")
    print("All routes saved → all_routes.csv")


if __name__ == "__main__":
       main()
    # test_file = Path("test.fit.gz")
    # parser = get_parser_for(test_file)
    # coords = parser.parse(test_file)
    # # raw_semicircles is the int from rec.get_raw_value('position_lat')
    # converted_coords = [ tuple( [ x * 180 / 2**31 for x in coord] ) for coord in coords ]

    # # print(converted_coords)
    # plot_route(converted_coords, "testing.html")
    # 

