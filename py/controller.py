from helpers import *
from db import *
from helpers import *
from province import *
from state import *
from trade import *


class Action:
    def __init__(self, action_type, action_data):
        self.type = action_type
        self.data = action_data


class Controller:
    def __init__(self, db_path=DB_PATH):
        self.actions = []
        self.data = DB(db_path)
        self.load()
        self.spent = {state_id: Cost() for state_id in self.states.keys()}

    def write(self):
        self.data.write(self.states, self.regions, self.provinces)

    def load(self):
        self.states, self.regions, self.provinces = self.data.load()

    def add_action(self, action):
        self.actions.append(action)
        if self.actions[-1].data.id == -1:
            self.actions[-1].data.id = len(self.actions) - 1
        if action.type == ActionEnum.build:
            self.spent[self.provinces[action.data.province_id].state_id] += action.data.calc_cost()

    def costs(self):
        try:
            raise AttributeError
            return self._costs
        except AttributeError:
            self._costs = dict()
            for state in self.states.values():
                self._costs[state.id] = round(self.spent[state.id].money * max(MIN_DISC, self.spent[state.id].pm / state.pm()) ** 2)
            return self._costs

    def check(self):
        for state in self.states.values():
            if state.ap() < self.spent[state.id].ap:
                return ControllerStatusEnum.bad_ap, state.id
            if state.money < self.costs()[state.id]:
                return ControllerStatusEnum.money_overdraft, state.id
        return ControllerStatusEnum.ok, -1

    def commit(self):
        try:
            status, index = self.check()
            if status != ControllerStatusEnum.ok:
                return status, index
            for state in self.states.values():
                state.money -= self.costs()[state.id]
            for action in self.actions:
                if action.type == ActionEnum.build:
                    self.provinces[action.data.province_id].buildings += action.data.build_type * action.data.count
            del self._costs
            self.write()
            self.load()
            return ControllerStatusEnum.ok, -1
        except:
            return ControllerStatusEnum.unknown, -1    
