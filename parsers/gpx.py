import gpxpy
from pathlib import Path
from .base import RouteParser, Coords

class GPXParser(RouteParser):
    def can_parse(self, path: Path) -> bool:
        return path.suffix.lower() == ".gpx"

    def parse(self, source: Path) -> Coords:
        with open(source, "r") as gpx_file:
            gpx = gpxpy.parse(gpx_file)

        coords = []
        for track in gpx.tracks:
            print(track.type)
            for segment in track.segments:
                for point in segment.points:
                    coords.append((point.latitude, point.longitude))

        return coords
