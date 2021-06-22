import csv
from datenanalyse.plot.typings import *
import matplotlib
import matplotlib.pyplot as plt
from ..meta.values import stratVal


def isValidNumber(text):
    try:
        float(text)
        return True
    except ValueError:
        return False


def extractCoords(inputfile, xunit, yunit, skip, zunit, delimiter, onlyUp, isStrato):
    """Ließt die Datei ein und extrahiert die Koordinaten einer Datenreihe"""
    with open(inputfile, 'r') as csvfile:
        x = []
        y = []
        z = []
        datareader = csv.reader(csvfile, delimiter=delimiter)
        for index, row in enumerate(datareader):
            if index != 0 and index % skip == 0 or index <= 100:
                if not isValidNumber(row[xunit["index"]]) or not isValidNumber(row[yunit["index"]]) or (zunit != None and (not isValidNumber(row[zunit["index"]]) or row[zunit["index"]] == None)):
                    continue
                elif float(row[stratVal["h"]["index"]]) > 37700 and onlyUp and isStrato:
                    break
                else:
                    x.append(float(row[xunit["index"]]))
                    y.append(float(row[yunit["index"]]))
                    if zunit != None:
                        z.append(float(row[zunit["index"]]))
        return x, y, z


def graph(graphOptions: GraphOptions, windowOptions: WindowOptions, datastreams:list[Datastream]):
    """Führt alle Funktionen, die zur Darstellung des Graphen benötigt werden in der richtigen Reihenfolge aus. Übergeben werden die Einstellungen des Graphens und des Fensters und eine Liste an Einstellungen der Datenreihen."""
    if graphOptions.makePgf:
        matplotlib.use("pgf")
        matplotlib.rcParams.update({
            "pgf.texsystem": "lualatex",
            'font.family': 'serif',
            'text.usetex': True,
            'pgf.rcfonts': False,
        })
    plt.figure().canvas.set_window_title(windowOptions.windowTitle)


    for i in datastreams:
        if graphOptions.graph3D:
            ax = plt.axes(projection='3d')
            ax.set_autoscalex_on(graphOptions.autoscale)
            ax.set_autoscaley_on(graphOptions.autoscale)
            x, y, z = extractCoords(i.filepath, i.xunit, i.yunit, i.skip, i.zunit, i.delimiter, graphOptions.onlyUp, i.isStrato)
            if i.scatterPlot:
                ax.scatter(x, y, z, label=i.label, c=i.color, s=[i.size for _ in x])
            else:
                ax.plot(x, y, z, c=i.color, label=i.label)
        else:
            plt.autoscale(graphOptions.autoscale)
            x, y, z = extractCoords(i.filepath, i.xunit, i.yunit, i.skip, i.zunit, i.delimiter, graphOptions.onlyUp, i.isStrato)
            if i.scatterPlot:
                plt.scatter(x, y, label=i.label, color=i.color, s=[i.size for _ in x])
            else:
                plt.plot(x, y, c=i.color, label=i.label, linewidth=i.size)
    plt.xlabel(datastreams[0].xunit["name"])
    plt.ylabel(datastreams[0].yunit["name"])
    if graphOptions.graph3D:
        ax.set_zlabel(datastreams[0].zunit["name"])
    plt.title(graphOptions.title)
    plt.legend()
    plt.grid(True)
    if graphOptions.makePgf:
        plt.savefig(graphOptions.docName + ".pgf")
    else:
        plt.show()