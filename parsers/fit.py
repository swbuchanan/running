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
            # print(dir(record))
            # print(record.fields)
            for field in record:
                if field.name == 'type':
                    print(field.value)
            lat = record.get_value("position_lat")
            lon = record.get_value("position_long")
            # heart_rate = record.heart_rate
            # altitude = record.enhanced_altitude
            if lat is not None and abs(lat) > 2**10:
                lat = lat * 180 / 2**31
            if lon is not None and abs(lon) > 2**10:
                lon = lon * 180 / 2**31
            if lat is not None and lon is not None:
                coords.append((lat, lon))  # Convert to degrees

        return coords
