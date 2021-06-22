from dataclasses import dataclass
from typing import Optional


@dataclass
class Strato:
    rawFile: str
    formattedFile: str
    startTime: float = 25
    landTime: float = 25
    delimiter: str = ","


@dataclass
class Arduino:
    rawFile: str
    formattedFile: str
    startTime: float
    landTime: float
    delimiter: str = ","


@dataclass
class Simulation:
    outputFile: str
    heAmount: float
    mNutzlast: float
    stopByRadius: str
    stopValue: float = 5.25
    experience: bool = False
    delimiter: str = ","
