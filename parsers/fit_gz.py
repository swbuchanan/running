import gzip
from pathlib import Path
from .base import RouteParser, Coords
from .fit import FitParser

class FitGzParser(RouteParser):
    def can_parse(self, path: Path) -> bool:
        return path.suffix == ".gz"

    def parse(self, source: Path) -> Coords:
        with gzip.open(source, "rb") as fh:
            return FitParser().parse(fh)
