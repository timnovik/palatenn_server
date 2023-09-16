from config import *
from province import Province
from state import State
from trade import TradeRegion
from db import *


states, regions, provinces = load()
prov = provinces[0]
print(prov, prov.pm_base)
prov.buildings += BuildingEnum.city * 2
print(prov, prov.pm_base)
