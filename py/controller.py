from helpers import *
from db import *
from helpers import *
from province import *
from state import *
from trade import *


class Controller:
    def __init__(self, db_path: str = DB_PATH) -> Self:
        self.data = DB(db_path)
        self._costs = dict()
        self.load()
        self.spent = {state_id: Cost() for state_id in self.states.keys()}

    def write(self) -> None:
        self.data.write(self.states, self.regions, self.provinces, self.actions)

    def load(self) -> None:
        self.states, self.regions, self.provinces, self.actions = self.data.load()

    def add_action(self, action: Action) -> None:
        if action.data.id == -1:
            action.data.id = len(self.actions)
        self.actions[action.data.id] = action
        if action.type == ActionEnum.build:
            self.spent[self.provinces[action.data.province_id].state_id] += action.data.calc_cost()
        self.write()

    def calc_costs(self) -> None:
        for state in self.states.values():
            self._costs[state.id] = round(self.spent[state.id].money * max(MIN_DISC, self.spent[state.id].pm / state.pm()) ** 2)

    def check(self) -> tuple[ControllerStatusEnum, int]:
        for state in self.states.values():
            if state.ap() < self.spent[state.id].ap:
                return ControllerStatusEnum.bad_ap, state.id
            if state.money < self._costs[state.id]:
                return ControllerStatusEnum.money_overdraft, state.id
        return ControllerStatusEnum.ok, -1

    def clear(self) -> None:
        self._costs.clear()
        self.actions.clear()

    def commit(self) -> tuple[ControllerStatusEnum, int]:
        try:
            self.calc_costs()
            status, index = self.check()
            if status != ControllerStatusEnum.ok:
                return status, index
            for state in self.states.values():
                state.money -= self._costs[state.id]
            for id_, action in self.actions.items():
                if action.type == ActionEnum.build:
                    self.provinces[action.data.province_id].buildings += action.data.build_type * action.data.count
            self.clear()
            self.write()
            self.load()
            return ControllerStatusEnum.ok, -1
        except:
            return ControllerStatusEnum.unknown, -1
