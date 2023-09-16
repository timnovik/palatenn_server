from config import *
from province import Province
from state import State
from trade import TradeRegion
from os import rename


def load_states():
    res = dict()
    for line in open(STATE_DB, "r"):
        state = State(line)
        res[state.id] = state
    return res


def write_states(data):
    with open(STATE_DB + ".new", "w") as db:
        for state in data.values():
            print(state, file=db)
    rename(STATE_DB + ".new", STATE_DB)


def load_regions():
    res = dict()
    for line in open(REGION_DB, "r"):
        region = TradeRegion(line)
        res[region.id] = region
    return res


def write_regions(data):
    with open(REGION_DB + ".new", "w") as db:
        for region in data.values():
            print(region, file=db)
    rename(REGION_DB + ".new", REGION_DB)


def load_provinces(states_data=None, trade_data=None):
    res = dict()
    for line in open(PROVINCE_DB, "r"):
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


def write_provinces(data):
    with open(PROVINCE_DB + ".new", "w") as db:
        for province in data.values():
            print(province, file=db)
    rename(PROVINCE_DB + ".new", PROVINCE_DB)


def load():
    states = load_states()
    regions = load_regions()
    provinces = load_provinces(states, regions)
    return states, regions, provinces


def write(states, regions, provinces):
    write_states(states)
    write_regions(regions)
    write_provinces(provinces)
