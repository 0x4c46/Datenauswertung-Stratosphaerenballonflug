from datenanalyse.formatting.typings import Arduino, Strato
from math import sin, cos, radians, sqrt


def getData(inputfile: str):
    """Liest die rohe Datei und gibt diese als ```String``` zurück.\n
    - inputfile: Absoluter Dateipfad oder Dateiname, wenn die Datei im Ordner ```input``` abgelegt ist."""
    with open(inputfile) as f:
        return f.read()


def prepareStrato(raw: str, delimiter: str):
    """Entfernt ungewollte Zeichen im rohen ```String``` und ersetzt den Separator der einzelnen Spalten, gibt einen ```String``` zurück. \n
    - raw: Der rohe String, der von ```getData()``` zurückgegeben wird.
    - delimiter: Trennzeichen der formatierten CSV-Datei; Standardmäßig ```delimiter = ','```."""
    raw = raw.replace(";", delimiter)
    raw = raw.replace("$,", "")
    raw = raw.replace("#,", "")
    return raw


def prepareArduino(raw: str, delimiter: str):
    """Entfernt ungewollte Zeichen im rohen ```String``` und ersetzt den Separator der einzelnen Spalten, gibt einen ```String``` zurück. \n
    - raw: Der rohe String, der von ```getData()``` zurückgegeben wird.
    - delimiter: Trennzeichen der formatierten CSV-Datei; Standardmäßig ```delimiter = ','```."""
    raw = raw.replace(";", delimiter)
    return raw


def splitRaw(raw: str, delimiter: str):
    """Trennt den rohen ```String``` in die einzelnen Zeilen und separiert diese am Trennzeichen. ```splitRaw()``` gibt die ```Liste``` ```data``` zurück.
    - raw: Vorbereiteter ```String```"""
    data = []
    for row in raw.split("\n"):
        data.append(row.split(delimiter))
    return data


def timeToSec(row: list):
    """Rechnet die Zeit seit Aufzeichnungsbeginn in Sekunden um. \n
    - row: Ein Element der Liste ```data```, ebenfalls eine Liste."""
    time = row[0].split(":")
    time = int(time[0]) * 60 ** 2 + int(time[1]) * 60 + int(time[2])
    row[0] = str(time)


def utcToHours(row):
    """Rechnet die Zeit vom ```hh:mm:ss```-Format in Stunden um. \n
    - row: Ein Element der Liste ```data```, ebenfalls eine Liste."""
    time = row[1].split(":")
    time = float(time[0]) + float(time[1]) / 60 + float(time[2]) / 60 ** 2
    time = round(time, 4)
    row[1] = str(time)


def coordsToDecDegree(row, column: int):
    """Migriert das ```Grad Minuten.Dezimalminuten```-Format auf ```Grad.Dezimalgrad```. Da der Ballon sich nicht aus dem Nord-Ost-Quadranten bewegt, werden die Himmelsrichtungen vernachlässigt. \n
    - row: Ein Element der Liste ```data```, ebenfalls eine Liste.
    - column: Index der Spalte, in der sich die die Koordinaten befinden. Entspricht der Wert ```"NA"```, wird dieser durch einen leeren String ersetzt."""
    if row[column] == "NA":
        row[column] = ""
    else:
        raw = row[column].split(" ")
        coords = []
        coords = (float(raw[1]) / 60) + float(raw[0])
        coords = round(coords, 5)
        row[column] = str(coords)


def convertPressure(row):
    """Rechnet Hektopascal in Pascal um. \n
    - row: Ein Element der Liste ```data```, ebenfalls eine Liste."""
    if row[14] == "NA":
        row[14] = ""
    else:
        row[14] = float(row[14])
        row[14] = round(row[14] * 100, 6)
        row[14] = str(row[14])


def checkStarted(csv, startTime):
    """Berechnet den Startzeitpunkt. ```strattime == 25``` heißt, dass es automatisch berechnet werden soll."""
    if float(startTime) == 25:
        for i in range(31, len(csv)):
            if csv[i][10] != "NA" and csv[i - 30][10] != "NA":
                now = float(csv[i][10])
                previous = float(csv[i - 30][10])
                diff = abs(now - previous)
                if diff >= 200:
                    del csv[1:i - 30]
                    break
    else:
        line = 0
        for i in csv:
            if "UTC" not in i and "utc" not in i:
                if float(i[1]) <= startTime:
                    line += 1
                else:
                    del csv[1:line]
                    break


def checkLanded(csv, landTime):
    """Berechnet den Landezeitpunkt. ```strattime == 25``` heißt, dass es automatisch berechnet werden soll."""
    if float(landTime) == 25:
        height = False
        for i in range(len(csv) - 50):
            if csv[i+1][10] != "NA" and float(csv[i+1][10]) >= 20000 and not height:
                height = True
            if csv[i][10] != "NA" and csv[i + 50][10] != "NA" and csv[i][10] != 'Altitude NN [m]' and height:
                now = float(csv[i][10])
                previous = float(csv[i + 50][10])
                diff = abs(now - previous)
                if diff <= 100 and float(csv[i][10]) <= 2000:
                    del csv[i + 50:]
                    break
    else:
        line = 0
        for i in csv:
            if "UTC" not in i and "utc" not in i:
                if float(i[1]) <= landTime:
                    line += 1
                else:
                    del csv[line:]
                    break


def correctTime(csv):
    """Setzt die Flugzeit zurück, sodass der Flug bei 0s started"""
    for i in range(1, len(csv)):
        csv[i][0] = str(i * 2)


def calcXYAndXyV(row):
    """Berechnet die Geschwindigkeit über Grund, die x- und die y-Geschwindigkeit in m/s."""
    if "UTC" not in row and "utc" not in row:
        if row[8] != "":
            vges = float(row[8]) / 3.6
            row.append(str(round(vges, 6)))
            if row[9] != "":
                if float(row[9]) <= 180:
                    vx = str(round(vges * sin(radians(abs(90 - float(row[9])))), 6))
                    vy = str(round(vges * cos(radians(abs(90 - float(row[9])))), 6))
                else:
                    vx = str(round(vges * sin(radians(abs(270 - float(row[9])))), 6))
                    vy = str(round(vges * cos(radians(abs(270 - float(row[9])))), 6))
                row.append(vx)
                row.append(vy)
            else:
                row.append("")
                row.append("")
        else:
            if row[8] == "":
                row.append("")
            row.append("")
            row.append("")


def calcVUp(csv):
    """Berechnet die Aufstiegsgeschwindigkeit des Ballons im 40s Mittel."""
    for i in range(len(csv) - 1):
        i += 1
        if i <= 10:
            difference = []
            for line in range(10):
                difference.append(
                    float(csv[i + line + 1][10]) - float(csv[i + line][10]))
            summe = sum(difference)
            csv[i].append(
                str(round(summe / abs((float(csv[i][0]) - float(csv[i + 9][0]))), 6)))
        elif i - 10 > 1 and i + 10 < len(csv) - 1:
            difference = []
            for line in range(-10, 10):
                difference.append(
                    float(csv[i + line + 1][10]) - float(csv[i + line][10]))
            summe = sum(difference)
            csv[i].append(
                str(round(summe / abs((float(csv[i - 10][0]) - float(csv[i + 9][0]))), 6)))
        else:
            difference = []
            for line in range(-9, 0):
                difference.append(
                    float(csv[i + line + 1][10]) - float(csv[i + line][10]))
            summe = sum(difference)
            csv[i].append(
                str(round(summe / abs((float(csv[i - 10][0]) - float(csv[i][0]))), 6)))


def calcVges(row):
    """Berechnet die Gesamtgeschwindigkeit des Ballons horizontal und vertikal."""
    if "UTC" not in row and "utc" not in row:
        vges = str(round(sqrt(float(row[17]) ** 2 + float(row[20]) ** 2), 6))
        row.insert(17, vges)


def validTemp(row):
    """Prüft und filtert die Messfehler des Innentemperatursensors des Arduinos."""
    if row[3] == "":
        return
    row[3] = float(row[3])
    if row[3] >= 500:
        row[3] = ""
    row[3] = str(row[3])


def storeData(formattedFile, csv):
    """Fügt die Liste zu einem String zusammen und schreibt sie in ```formattedFile```."""
    with open(formattedFile, "w") as f:
        data = "\n".join(",".join(row) for row in csv)
        f.write(data)


def formatStrato(strato: Strato):
    """Führt alle Funktionen, die zur Formatierung der Rohdatei vom Strato benötigt werden in der richtigen Reihenfolge aus.
    - ```strato```: Dataclass ```Strato``` mit allen benötigten Parametern"""
    raw = getData(strato.rawFile)
    raw = prepareStrato(raw, strato.delimiter)
    data = splitRaw(raw, strato.delimiter)
    csv = []
    gpsStatus = False
    for row in data:
        if "Y" not in row and "UTC" not in row and gpsStatus == False or row == [""]:
            del row
        elif "UTC" in row:
            row[14] = "Extern: Press [Pa]"
            row.append("vges [m/s]")
            row.append("vxy [m/s]")
            row.append("vx [m/s]")
            row.append("vy [m/s]")
            row.append("vz [m/s]")
            csv.append(row)
        else:
            timeToSec(row)
            utcToHours(row)
            coordsToDecDegree(row, 5)
            coordsToDecDegree(row, 6)
            convertPressure(row)
            csv.append(row)
            gpsStatus = True
    checkStarted(csv, strato.startTime)
    checkLanded(csv, strato.landTime)
    correctTime(csv)
    csv = list(filter(lambda x: "NA" not in x, csv))
    for row in csv:
        calcXYAndXyV(row)
    calcVUp(csv)
    for row in csv:
        calcVges(row)
    storeData(strato.formattedFile, csv)
    print("Done")


def formatArduino(arduino: Arduino):
    """Führt alle Funktionen, die zur Formatierung der Rohdatei vom Arduino benötigt werden in der richtigen Reihenfolge aus.
    - ```arduino```: Dataclass ```Arduino``` mit allen benötigten Parametern"""
    raw = getData(arduino.rawFile)
    raw = prepareArduino(raw, arduino.delimiter)
    data = splitRaw(raw, arduino.delimiter)
    csv = []
    for row in data:
        if "utc" in row or "UTC" in row:
            csv.append(row)
        elif row == [""]:
            del row
        else:
            utcToHours(row)
            validTemp(row)
            if row is not None:
                csv.append(row)
    checkStarted(csv, arduino.startTime)
    checkLanded(csv, arduino.landTime)
    correctTime(csv)
    storeData(arduino.formattedFile, csv)
    print("Done")
