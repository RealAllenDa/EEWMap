from dataclasses import dataclass
from typing import Literal

from dataclasses_json import DataClassJsonMixin


@dataclass
class ReturnShakeLevelJSON(DataClassJsonMixin):
    status: Literal[0]
    shake_level: int
    green: int
    yellow: int
    red: int


@dataclass
class ShakeLevelJSON(DataClassJsonMixin):
    l: int  # shake level
    g: int  # green points
    y: int  # yellow points
    r: int  # red points
    t: str  # time elapsed from last hour
    e: int  # status
