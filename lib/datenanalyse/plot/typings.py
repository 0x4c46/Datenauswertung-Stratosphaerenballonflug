from dataclasses import dataclass
from typing import Optional


@dataclass
class Datastream:
    xunit: dict
    yunit: dict
    label: str
    filepath: str
    color: str
    size: float
    scatterPlot: bool
    zunit: Optional[dict] = None
    skip: int = 1
    delimiter: str = ","
    isStrato: bool = False


@dataclass
class WindowOptions:
    windowTitle: str


@dataclass
class GraphOptions:
    title: str
    graph3D: bool
    onlyUp: bool = True
    autoscale: bool = True
    makePgf: bool = False
    docName: str = ""
