from pathlib import Path
from .gpx import GPXParser
from .fit import FitParser
from .fit_gz import FitGzParser

PARSERS = [
    GPXParser(),
    FitParser(),
    FitGzParser(),
]

def get_parser_for(path: Path):
    for parser in PARSERS:
        if parser.can_parse(path):
            return parser

    raise ValueError(f"No parser found for {path}")
