from config import *
from province import Province
from state import State
from trade import TradeRegion
from db import *


states = load_states()
regions = load_regions()
provinces = load_provinces(states, regions)

print(sum([p.tv for p in provinces.values()]))
print(regions[0].tv())
