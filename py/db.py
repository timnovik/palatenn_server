from controller import *
from db import *
from helpers import *
from province import *
from state import *
from trade import *

from os import rename


class DB:
    def __init__(self, db_path: str) -> Self:
        self.db_path = db_path

    def load_states(self) -> dict[int, State]:
        res = dict()
        for line in open(self.db_path + "/" + STATE_PATH, "r"):
            state = State.load(line)
            res[state.id] = state
        return res

    def write_states(self, data: dict[int, State]) -> None:
        with open(self.db_path + "/new/" + STATE_PATH, "w") as db:
            for state in data.values():
                print(state.save(), file=db)

    def commit_states(self) -> None:
        rename(self.db_path + "/new/" + STATE_PATH, self.db_path + "/" + STATE_PATH)

    def load_regions(self) -> None:
        res = dict()
        for line in open(self.db_path + "/" + REGION_PATH, "r"):
            region = TradeRegion.load(line)
            res[region.id] = region
        self.connect_regions(res)
        return res

    def write_regions(self, data: dict[int, TradeRegion]) -> None:
        with open(self.db_path + "/new/" + REGION_PATH, "w") as db:
            for region in data.values():
                print(region.save(), file=db)

    def commit_regions(self) -> None:
        rename(self.db_path + "/new/" + REGION_PATH, self.db_path + "/" + REGION_PATH)

    def connect_regions(self, data: dict[int, TradeRegion]) -> None:
        for region in data.values():
            for i in region.neighbor_ids:
                region.neighbors.append(data[i])

    def load_provinces(self, states_data: dict[int, State] | None = None, trade_data: dict[int, TradeRegion] | None = None) -> dict[int, Province]:
        res = dict()
        for line in open(self.db_path + "/" + PROVINCE_PATH, "r"):
            province = Province.load(line)
            res[province.id] = province
            if states_data is not None:
                state = states_data[province.state_id]
                province.state = state
                state.provinces.append(province)
            if trade_data is not None:
                region = trade_data[province.trade_id]
                province.region = region
                region.provinces.append(province)
                if province.state not in region.states:
                    region.states.append(province.state)
        return res

    def write_provinces(self, data: dict[int, Province]) -> None:
        with open(self.db_path + "/new/" + PROVINCE_PATH, "w") as db:
            for province in data.values():
                print(province.save(), file=db)

    def commit_provinces(self) -> None:
        rename(self.db_path + "/new/" + PROVINCE_PATH,  self.db_path + "/" + PROVINCE_PATH)

    def load_actions(self) -> dict[int, Action]:
        res = dict()
        for line in open(self.db_path + "/" + ACTION_PATH, "r"):
            action = Action.load(line)
            res[action.data.id] = action
        return res

    def write_actions(self, data: dict[int, Action]) -> None:
        with open(self.db_path + "/new/" + ACTION_PATH, "w") as db:
            for action in data.values():
                print(action.save(), file=db)

    def commit_actions(self) -> None:
        rename(self.db_path + "/new/" + ACTION_PATH, self.db_path + "/" + ACTION_PATH)

    def load(self) -> tuple[dict[int, State], dict[int, TradeRegion], dict[int, Province], dict[int, Action]]:
        states = self.load_states()
        regions = self.load_regions()
        provinces = self.load_provinces(states, regions)
        actions = self.load_actions()
        return states, regions, provinces, actions

    def write(self, states: dict[int, State], regions: dict[int, TradeRegion], provinces: dict[int, Province], actions: dict[int, Action]) -> None:
        self.write_states(states)
        self.write_regions(regions)
        self.write_provinces(provinces)
        self.write_actions(actions)
        self.commit()

    def commit(self) -> None:
        self.commit_states()
        self.commit_regions()
        self.commit_provinces()
        self.commit_actions()
