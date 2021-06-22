import math
from datenanalyse.meta.konstantenCSV import *

def TValue(i, l):
    if l[i][preVal["h"]["index"]] < 11000:
        return 15.04 - 0.00649 * l[i][preVal["h"]["index"]]
    elif l[i][preVal["h"]["index"]] >= 11000 and l[i][preVal["h"]["index"]] <= 25000:
        return -56.35
    else:
        return -131.1 + 0.00299 * l[i][preVal["h"]["index"]]


def pnasaValue(i, l):
    if l[i][preVal["h"]["index"]] < 11000:
        return 101.29 * ((l[i][preVal["T"]["index"]] + 273.15) / 288.08)**5.256
    elif l[i][preVal["h"]["index"]] >= 11000 and l[i][preVal["h"]["index"]] <= 25000:
        return 22.65 * math.exp(1.73 - 0.000157 * l[i][preVal["h"]["index"]])
    else:
        return 2.488 * ((l[i][preVal["T"]["index"]] + 273.15) / 216.6)**-11.388


class PreVal:
    def __init__(self, heAmount, mNutzlast):
        self.heAmount = heAmount
        self.mNutzlast = mNutzlast
        self.NBallon = (heAmount * pHelium)/(boltzmannkonstante * TGas)
        self.mHelium = self.NBallon * 6.6464731 * 10**-27
        self.mges = mBallon + mNutzlast + self.mHelium
        
        self.preVal = {
            "t": {
                "name": "Zeit t $[s]$",
                "index": 0,
                "firstLineValue": 0.0,
                "value": lambda i, l: deltat + l[i-1][preVal["t"]["index"]]
            },
            "v": {
                "name": "Geschwindigkeit v $\\left[\\frac{m}{s}\\right]$",
                "index": 1,
                "firstLineValue": 0,
                "value": lambda i, l: l[i-1][preVal["a"]["index"]] * deltat + l[i-1][preVal["v"]["index"]]
            },
            "h": {
                "name": "Höhe h $[m]$",
                "index": 2,
                "firstLineValue": 100,
                "value": lambda i, l: l[i-1][preVal["h"]["index"]] + l[i-1][preVal["v"]["index"]] * deltat + 0.5 * l[i-1][preVal["a"]["index"]] * deltat**2
            },
            "T": {  # * checked
                "name": "Temperatur T $[°C]$",
                "index": 3,
                "value": lambda i, l: TValue(i, l)
            },
            "p": {
                "name": "Luftdruck $p_{Luft} [Pa]$",
                "index": 4,
                "value": lambda i, l: pnasaValue(i, l) * 1000
            },
            "V": {  # * checked
                "name": "Ballonvolumen $V_{Ballon} \\left[m^3\\right]$",
                "index": 5,
                "value": lambda i, l: (self.NBallon * boltzmannkonstante * (l[i][preVal["T"]["index"]] + 273.15)) / l[i][preVal["p"]["index"]]
            },
            "r": {  # * checked
                "name": "Ballonradius r $[m]$",
                "index": 6,
                "value": lambda i, l: (l[i][preVal["V"]["index"]] / ((4 / 3) * math.pi)) ** (1 / 3)
            },
            "A": {  # * checked
                "name": "Frontfläche Ballon A $\\left[m^2\\right]$",
                "index": 7,
                "value": lambda i, l: (math.pi * l[i][preVal["r"]["index"]] ** 2) * fitting
            },
            "rho": {  # * checked
                "name": "Luftdichte $rho_{Luft} \\left[\\frac{kg}{m^3} \\right]$",
                "index": 8,
                "value": lambda i, l: (l[i][preVal["p"]["index"]] / 1000) / (0.2869 * (l[i][preVal["T"]["index"]] + 273.15))
            },
            "cw": {
                "name": "cW-Wert",
                "index": 9,
                "value": lambda i, l: 0.000333 * l[i][preVal["V"]["index"]] + 0.25
            },
            "g": {  # * checked
                "name": "Erdbeschleunigung g $\\left[ \\frac{m}{s^2} \\right]$",
                "index": 10,
                "value": lambda i, l: (gKonstante * mErde) / (erdradius + l[i][preVal["h"]["index"]]) ** 2
            },
            "FAuftrieb": {
                "name": "Auftriebskraft $F_{Auftrieb} [N]$",
                "index": 11,
                "value": lambda i, l: l[i][preVal["rho"]["index"]] * l[i][preVal["V"]["index"]] * l[i][preVal["g"]["index"]]
            },
            "Fg": {
                "name": "Erdanziehungskraft $F_G [N]$",
                "index": 12,
                "value": lambda i, l:  self.mges * l[i][preVal["g"]["index"]]
            },
            "FLuft": {
                "name": "Luftwiderstandskraft $F_{Luftwiderstand} [N]$",
                "index": 13,
                "value": lambda i, l: 0.5 * l[i][preVal["cw"]["index"]] * l[i][preVal["rho"]["index"]] * l[i][preVal["A"]["index"]] * l[i][preVal["v"]["index"]] ** 2
            },
            "Fges": {
                "name": "Gesamtkraft $F_{ges} [N]$",
                "index": 14,
                "value": lambda i, l: l[i][preVal["FAuftrieb"]["index"]] - l[i][preVal["Fg"]["index"]] - l[i][preVal["FLuft"]["index"]]
            },
            "a": {
                "name": "Beschleunigung a $\\left[ \\frac{m}{s^2} \\right]$",
                "index": 15,
                "value": lambda i, l: l[i][preVal["Fges"]["index"]] / self.mges
            }
        }


stratVal = {
    "t": {
        "index": 0,
        "name": "Aufzeichnungsdauer t $[s]$"
    },
    "UTC": {
        "index": 1,
        "name": "Uhrzeit (UTC) $[h]$",
    },
    "date": {
        "index": 2,
        "name": "Datum $[day]$"
    },
    "signal": {
        "index": 3,
        "name": "Empfang $[bool]$"
    },
    "sats": {
        "index": 4,
        "name": "Satelliten"
    },
    "lat": {
        "index": 5,
        "name": "Breitengrad $[Grad]$"
    },
    "lon": {
        "index": 6,
        "name": "Längengrad $[Grad]$"
    },
    "vkn": {
        "index": 7,
        "name": "Steiggeschwindigkeit $[kn]$"
    },
    "vkm": {
        "index": 8,
        "name": "Waagerechte Geschwindigkeit $\\left[ \\frac{km}{h}\\right]$"
    },
    "course": {
        "index": 9,
        "name": "Kurs $[Grad]$"
    },
    "h": {
        "index": 10,
        "name": "Höhe $[m]$"
    },
    "intemp": {
        "index": 11,
        "name": "Boardtemperatur $[°C]$"
    },
    "exttemp": {
        "index": 12,
        "name": "Außentemperatur $[°C]$"
    },
    "exthum": {
        "index": 13,
        "name": "Außenluftfeuchtigkeit $[%]$"
    },
    "extpress": {
        "index": 14,
        "name": "Außenluftdruck $[Pa]$"
    },
    "battu": {
        "index": 15,
        "name": "Batteriespannung $[V]$"
    },
    "code": {
        "index": 16,
        "name": "Statuscode"
    },
    "vges": {
        "index": 17,
        "name": "Gesamtgeschwindigkeit $\\left[ \\frac{m}{s}\\right]$"
    },
    "vxy": {
        "index": 18,
        "name": "Waagerechte Geschwindigkeit $\\left[ \\frac{m}{s}\\right]$"
    },
    "vx": {
        "index": 19,
        "name": "x-Geschwindigkeit $\\left[ \\frac{m}{s}\\right]$"
    },
    "vy": {
        "index": 20,
        "name": "y-Geschwindigkeit $\\left[ \\frac{m}{s}\\right]$"
    },
    "vz": {
        "index": 21,
        "name": "Steiggeschwindigkeit $\\left[ \\frac{m}{s}\\right]$"
    }
}

ardVal = {
    "t": {
        "index": 0,
        "name": "Aufzeichnungsdauer t $[s]$"
    },
    "UTC": {
        "index": 1,
        "name": "Uhrzeit (UTC) $[h]$"
    },
    "exttemp": {
        "index": 2,
        "name": "Außentemperatur $[°C]$"
    },
    "intemp": {
        "index": 3,
        "name": "Onboardtemperatur $[°C]$"
    },
    "incltemp": {
        "index": 4,
        "name": "Temperatur Neigungs- und Beschleunigungssensor $[°C]$"
    },
    "ax": {
        "index": 5,
        "name": "Vertikale Beschleunigung $\\left[\\frac{m}{s^2}\\right]$"
    },
    "ay": {
        "index": 6,
        "name": "Horizontale Beschleunigung $\\left[\\frac{m}{s^2}\\right]$"
    },
    "rot": {
        "index": 7,
        "name": "Rotation $[Grad]$"
    },
    "incx": {
        "index": 8,
        "name": "Neigung $[Grad]$"
    },
    "incy": {
        "index": 9,
        "name": "Neigung $[Grad]$"
    },
    "battu": {
        "index": 10,
        "name": "Batteriespannung $[V]$"
    },
}

spotVal = {
    "UTC": {
        "index": 0,
        "name": "Uhrzeit UTC $[h]$"
    },
    "lat": {
        "index": 1,
        "name": "Breitengrad $[Grad]$"
    },
    "lon": {
        "index": 2,
        "name": "Längengrad $[Grad]$"
    },
    "trash": {
        "index": 3,
        "name": "Uhrzeit UTC $[h]$"
    },
    "trash": {
        "index": 4,
        "name": "Uhrzeit UTC $[h]$"
    },
    "trash": {
        "index": 5,
        "name": "Uhrzeit UTC $[h]$"
    },
    "h": {
        "index": 6,
        "name": "Höhe $[m]$"
    },
    "trash": {
        "index": 7,
        "name": "Uhrzeit UTC $[h]$"
    },
    "diffh": {
        "index": 8,
        "name": "Höhendifferenz zum Strato $[m]$"
    },
    "tDiffStrato": {
        "index": 9,
        "name": "Zeitdifferenz zum Strato $[h]$"
    },
    "tStrato": {
        "index": 10,
        "name": "Uhrzeit Strato UTC $[h]$"
    },
}
preVal = PreVal(0,0).preVal
