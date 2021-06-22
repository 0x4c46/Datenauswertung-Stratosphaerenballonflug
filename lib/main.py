from datenanalyse.formatting.simulation import *
from datenanalyse.formatting.format import *
from datenanalyse.plot.graph import *
from datenanalyse.meta.values import *
import sys

def raw_input():
    out = b''
    while (c:=sys.stdin.buffer.read(1)) != b'\n':
        out = out + c
    return out

raw = raw_input()
data = raw.decode("utf-8")
print("PYTHON" + data)
args = data.split("!!")


if args[0] == "simulate":
    calcSimulation(
        Simulation(
            args[1],
            float(args[2]),
            float(args[3]),
            args[4],
            float(args[5]),
            args[6] == "true",
            ","
        )
    )


elif args[0] == "format":
    if args[1] == "true":
        formatStrato(
            Strato(
                args[2],
                args[3],
                float(args[4]),
                float(args[5]),
                args[6]
            )
        )
    else:
        formatArduino(
            Arduino(
                args[2],
                args[3],
                float(args[4]),
                float(args[5]),
                args[6]
            )
        )


elif args[0] == "plot":
    type = {
        "stratVal": stratVal,
        "ardVal": ardVal,
        "preVal": preVal,
        "null": None
    }

    datastreams = []
    for i in range(5, len(args), 11):
        if args[i] == "true":
            datastreams.append(Datastream(
                type[args[i+1]][args[i+2]] if type[args[i+1]
                                                   ] != None and args[i+2] != "null" else None,
                type[args[i+1]][args[i+3]] if type[args[i+1]
                                                   ] != None and args[i+3] != "null" else None,
                args[i+4],
                args[i+5],
                args[i+6],
                float(args[i+7]),
                args[i+8] == "true",
                type[args[i+1]][args[i+9]] if type[args[i+1]
                                                   ] != None and args[i+9] != "null" else None,
                float(args[i+10]),
                ",",
                args[i+1] == "stratVal",
            )
            )

    graph(
        GraphOptions(
            args[1],
            args[2] == "true",
            args[3] == "true",
            args[4] == "true",
            None,
            None
        ),
        WindowOptions(
            "Plot"
        ),
        datastreams
    )
