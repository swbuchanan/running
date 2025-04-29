from pathlib import Path
import folium
from parsers import get_parser_for

DIR = 'gpx'

def plot_route(coords, out_html):
    avg_lat = sum(lat for lat, _ in coords) / len(coords)
    avg_lon = sum(lon for _, lon in coords) / len(coords)
    m = folium.Map(location=(avg_lat, avg_lon), zoom_start=13)
    folium.PolyLine(coords, weight=5, opacity=0.7).add_to(m)
    m.save(out_html)

def main():

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

        coords = parser.parse(path)
        try:
            folium.PolyLine(
                coords,
                color=colors[idx % len(colors)],
                weight=3,
                opacity=0.7,
                tooltip=path.name
            ).add_to(m)
            print(f'parsed {path}')
        except ValueError: # not sure what this is but one time I got ValueError("Locations is empty")
            print('valueerror')
            pass
# 5. (Optional) Add a layer control if you split into FeatureGroups
#    from folium import FeatureGroup, LayerControl
#    # inside loop use fg = FeatureGroup(name=path.name); fg.add_child(...); m.add_child(fg)
#    m.add_child(LayerControl())

# 6. Save single HTML
    m.save('all_routes.html')
    print("All routes plotted → all_routes.html")

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

