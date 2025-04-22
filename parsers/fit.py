from fitparse import FitFile
from pathlib import Path
from .base import RouteParser, Coords

class FitParser(RouteParser):
    def can_parse(self, path: Path) -> bool:
        return path.suffix.lower() == ".fit"

    def parse(self, source: Path) -> Coords:
        fitfile = FitFile(source)
        coords = []

        for record in fitfile.get_messages("record"):
            lat = record.get_value("position_lat")
            lon = record.get_value("position_long")
            if lat is not None and lon is not None:
                coords.append((lat, lon))  # Convert to degrees

        return coords
