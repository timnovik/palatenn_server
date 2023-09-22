from helpers import *
from controller import *
from db import *
from helpers import *
from province import *
from state import *
from trade import *


controller = Controller()
controller.add_action(Action(ActionEnum.build, BuildActionData(BuildingEnum.block, 1, 0)))
status, index = controller.commit()
print(status)
