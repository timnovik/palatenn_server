from config import *
from province import Province, Buildings
from state import State
from trade import TradeRegion
from db import *


data = DB(DB_PATH)
states, regions, provinces = data.load()
prov = provinces[0]
prov.buildings += BuildingEnum.city * 2
prov.buildings += Buildings("2;1;0;0;0;0;0;0;0;0;0;0;0;0;0;")
provinces[1].buildings += BuildingEnum.city
provinces[1].buildings += BuildingEnum.barracks
data.write(states, regions, provinces)
