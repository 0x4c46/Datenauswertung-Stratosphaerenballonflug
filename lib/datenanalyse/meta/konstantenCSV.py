from datenanalyse.formatting.typings import Simulation

rhoLuft = 1.225  # [kg/m^3] Dichte von Luft stratoflights.com: 1.2050
rhoHelium = 0.1855  # [kg/m^3] Dichte von Helium
# VHelium = Simulation.heAmount  # [m^3] im Ballon
pHelium = 101300 # [pa] am Boden
TGas = 293.15 # [K] in der Flasche
MHelium = 4*10**(-3)  # [g/mol] Molare Masse Helium
mBallon = 1.6  # [kg] Masse Ballon
# mNutzlast = Simulation.mNutzlast  # [kg] Masse Nutzlast
cwWert = 0.25  # von stratoflights.com; CW = 0,45 für Kugel, könnte für den Ballon etwas geringer sein …
H = 7238.3 # [m] von stratoflights.com oder 7990 laut Wikipedia, Wert für T = 15°C    https://de.wikipedia.org/wiki/Barometrische_H%C3%B6henformel
h = 100  # [m] Höhe Lützenkirchen
avogadroscheZahl = 6.0221415 * 10**23
boltzmannkonstante = 1.3806503 * 10**-23  # [J*K^-1] aka k
# NBallon = (VHelium * pHelium)/(boltzmannkonstante * TGas)
# mHelium = NBallon * 6.6464731 * 10**-27
# mges = mBallon + mNutzlast + mHelium  # [kg] Gesamtmasse Ballon
erdradius = 6371000  # [m] Erdradius auf Meereshöhe
deltat = 0.05  # [s]
fitting = 0.87  # Faktor zur Berechn. von V
gKonstante = 6.673 * 10**-11  # [m^3 * kg^-1 * s^-2] Gravitationskonstante
mErde = 5.97 * 10**24  # [kg] Erdmasse