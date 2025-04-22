from pathlib import Path
import folium
from parsers import get_parser_for

def plot_route(coords, out_html):
    avg_lat = sum(lat for lat, _ in coords) / len(coords)
    avg_lon = sum(lon for _, lon in coords) / len(coords)
    m = folium.Map(location=(avg_lat, avg_lon), zoom_start=13)
    folium.PolyLine(coords, weight=5, opacity=0.7).add_to(m)
    m.save(out_html)

def main():
    for file in Path("gpx").iterdir():
        if not file.is_file():
            continue
        try:
            parser = get_parser_for(file)
        except ValueError:
            print(f"Cannot parse {file.name}")
            continue

        coords = parser.parse(file)
        out_html = file.with_suffix(".html")
        plot_route(coords, out_html)
        print(f"Plotted {file} -> {out_html}")

if __name__ == "__main__":
    main()
