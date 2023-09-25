from helpers import *
from controller import *
from db import *
from helpers import *
from province import *
from state import *
from trade import *


controller = Controller()
province = controller.provinces[0]
print(province.get("pm_cap"))
