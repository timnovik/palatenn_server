from config import *
from province import Province
from state import State
from trade import TradeRegion
from os import rename


class DB:
    def __init__(self, db_path):
        self.db_path = db_path

    def load_states(self):
        res = dict()
        for line in open(self.db_path + "/" + STATE_PATH, "r"):
            state = State(line)
            res[state.id] = state
        return res

    def write_states(self, data):
        with open(self.db_path + "/new/" + STATE_PATH, "w") as db:
            for state in data.values():
                print(state, file=db)

    def commit_states(self):
        rename(self.db_path + "/new/" + STATE_PATH, self.db_path + "/" + STATE_PATH)

    def load_regions(self):
        res = dict()
        for line in open(self.db_path + "/" + REGION_PATH, "r"):
            region = TradeRegion(line)
            res[region.id] = region
        self.connect_regions(res)
        return res

    def write_regions(self, data):
        with open(self.db_path + "/new/" + REGION_PATH, "w") as db:
            for region in data.values():
                print(region, file=db)

    def commit_regions(self):
        rename(self.db_path + "/new/" + REGION_PATH, self.db_path + "/" + REGION_PATH)

    def connect_regions(self, data):
        for region in data.values():
            for i in region.neighbor_ids:
                region.neighbors.append(data[i])

    def load_provinces(self, states_data=None, trade_data=None):
        res = dict()
        for line in open(self.db_path + "/" + PROVINCE_PATH, "r"):
            province = Province(line)
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

    def write_provinces(self, data):
        with open(self.db_path + "/new/" + PROVINCE_PATH, "w") as db:
            for province in data.values():
                print(province, file=db)

    def commit_provinces(self):
        rename(self.db_path + "/new/" + PROVINCE_PATH, PROVINCE_PATH)

    def load(self):
        states = self.load_states()
        regions = self.load_regions()
        provinces = self.load_provinces(states, regions)
        return states, regions, provinces

    def write(self, states, regions, provinces):
        self.write_states(states)
        self.write_regions(regions)
        self.write_provinces(provinces)

    def commit(self):
        self.commit_states()
        self.commit_regions()
        self.commit_provinces()
