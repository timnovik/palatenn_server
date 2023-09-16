from config import *
from province import Province
from state import State
from trade import TradeRegion
from db import *


states, regions, provinces = load()

print([province.tv for province in provinces.values()])
print([state.tv() for state in states.values()])
print(regions[0].tv())
