from datenanalyse.formatting.typings import Simulation
from datenanalyse.meta.values import PreVal
from datenanalyse.meta.konstantenCSV import *


def addFirstLine(l):
    """Baut die Headline der csv-Datei."""
    l.append([])
    for item in preVal.values():
        l[0].append(item["name"])


def addSecondLine(l):
    """Schreibt die zweite Zeile der csv-Datei ggf. mit Anfangswerten."""
    l.append([])
    for item in preVal.values():
        if "firstLineValue" in item.keys():
            l[0].append(round(item["firstLineValue"], 6))
        else:
            l[0].append(round(item["value"](0, l), 6))


def addLine(l, i, experience):
    """Führt die eigentliche Berechnung durch."""
    l.append([None for _ in range(len(preVal))])
    for item in preVal.values():
        if item == "V" and experience:
            l[i][item["index"]] = round(item["value"](
                i, l) * fitting * ((30000 - 0.15 * l[i][preVal["h"]["index"]]) / 29000), 6)
        else:
            l[i][item["index"]] = round(item["value"](i, l), 6)


def firstwrite(l, outputFile):
    """Schreibt die erste Zeile in die Datei."""
    csv = '\n'.join([','.join(y) for y in [[str(x) for x in y] for y in l]])
    with open(outputFile, "w", encoding="utf8") as f:
        f.write(csv)
    return []


def write(outputFile, c):
    """Schreibt die Werte in die Datei"""
    csv = '\n'.join([','.join(y) for y in [[str(x) for x in y] for y in c]])
    with open(outputFile, "a", encoding="utf8") as f:
        f.write(csv)


def run(l, simulation):
    """Bestimmt den Schreibzyklus, damit nicht zu viel RAM verbraucht wird und es im Ganzen ressourcenschonender ist. Prüft auch, ob noch weiter gerechnet werden muss."""
    for _ in range(10):
        for i in range(1, 15000):
            addLine(l, i, simulation.experience)
            if simulation.stopByRadius == "Radius":
                if l[i][preVal["r"]["index"]] >= simulation.stopValue:
                    print("Done")
                    return i
            else:
                if l[i][preVal["h"]["index"]] >= simulation.stopValue:
                    print("Done")
                    return i
        write(simulation.outputFile, l[:-1])
        del l[:-1]
    print("overflow error")
    return 1


def calcSimulation(simulation: Simulation):
    """Führt alle Funktionen, die zur Simulation benötigt werden in der richtigen Reihenfolge aus.
    - ```simulation```: Dataclass ```Simulation``` mit allen benötigten Parametern"""
    global preVal
    preVal = PreVal(simulation.heAmount, simulation.mNutzlast).preVal
    l = []
    addFirstLine(l)
    l = firstwrite(l, simulation.outputFile)
    addSecondLine(l)
    rest = run(l, simulation)
    if rest % 9999 != 0:
        write(simulation.outputFile, l)
