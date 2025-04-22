# parsers/base.py
from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Tuple, Union, BinaryIO

Coords = List[Tuple[float, float]]

class RouteParser(ABC):
    @abstractmethod
    def can_parse(self, path: Path) -> bool:
        """Return True if this parser knows how to handle this file."""
        ...

    @abstractmethod
    def parse(self, source: Union[Path, BinaryIO]) -> Coords:
        """
        Read the file (or file‑like) and return a list of (lat, lon) pairs.
        """
        ...
