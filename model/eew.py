from dataclasses import dataclass
from enum import Enum, auto


class EEWStatus(Enum):
    NO_EEW = -1
    NORMAL = 0


class EEWType(Enum):
    kmoni = auto()
    svir = auto()


@dataclass
class ReturnEEW:
    status: EEWStatus
    type: EEWType
    is_plum: bool
    is_cancel: bool
    max_intensity: str
