from enum import Enum

# NETWORK CONFIG
HOST_IP = "127.0.0.1"
HOST_PORT = 5000

# DATABASE CONFIG
SEP = ";"
URB_POS = 4
GC_POS = 5

PROVINCE_DB = "data/provinces.csv"
STATE_DB = "data/states.csv"
REGION_DB = "data/regions.csv"

# ACCURACY CONFIG
ACC = 100      # точность вычисления процентных модификаторов
URB_MUL = 100  # точность вычисления урбанизации
GC_MUL = 100   # точность вычисления стоимости товаров


# QUERIES CONFIG
class ProvinceFieldEnum(Enum):
    pop = "pop"
    urban = "urban"
    goods_cost = "goods_cost"
    dev = "dev"
    pm = "pm"
    pm_cap = "pm_cap"
    tv = "tv"


class ProvinceQueryEnum(Enum):
    base = "base"
    add = "add"
    mul = "mul"
    total = "total"


# BUILDINGS CONFIG
class BuildingEnum(Enum):
    city = "city"
    block = "block"
    road = "road"
    bridge = "bridge"
    mine = "mine"
    market = "market"
    trading_post = "trading_post"
    port = "port"
    shipyard = "shipyard"
    workshop = "workshop"
    barracks = "barracks"
    forge = "forge"
    furnace = "furnace"
    stable = "stable"
    stock = "stock"

    def __mul__(self, other):
        return self.name + SEP + str(other)


class BuildingType:
    def __init__(self, building, impact):
        self.building = building
        self._impact = {field: impact.get(field, (0, 0)) for field in ProvinceFieldEnum}

    def impact(self, cnt, field, mode):
        return cnt * self._impact[field][mode]


BUILDINGS = {
    BuildingEnum.city: BuildingType(BuildingEnum.city, {ProvinceFieldEnum.urban: (5, 0), ProvinceFieldEnum.dev: (5, 0)}),
    BuildingEnum.block: BuildingType(BuildingEnum.block, {ProvinceFieldEnum.dev: (1, 0)}),
    BuildingEnum.road: BuildingType(BuildingEnum.road, {ProvinceFieldEnum.dev: (0, 10)}),
    BuildingEnum.bridge: BuildingType(BuildingEnum.bridge, {ProvinceFieldEnum.dev: (0, 10)}),
    BuildingEnum.mine: BuildingType(BuildingEnum.mine, {ProvinceFieldEnum.dev: (3, 0)}),
    BuildingEnum.market: BuildingType(BuildingEnum.market, {ProvinceFieldEnum.goods_cost: (100, 0)}),
    BuildingEnum.trading_post: BuildingType(BuildingEnum.trading_post, {ProvinceFieldEnum.tv: (0, 10)}),
    BuildingEnum.port: BuildingType(BuildingEnum.port, {ProvinceFieldEnum.dev: (1, 0)}),
    BuildingEnum.shipyard: BuildingType(BuildingEnum.shipyard, {ProvinceFieldEnum.dev: (1, 0)}),
    BuildingEnum.workshop: BuildingType(BuildingEnum.workshop, {ProvinceFieldEnum.dev: (1, 0)}),
    BuildingEnum.barracks: BuildingType(BuildingEnum.barracks, {}),
    BuildingEnum.forge: BuildingType(BuildingEnum.forge, {ProvinceFieldEnum.dev: (1, 0)}),
    BuildingEnum.furnace: BuildingType(BuildingEnum.furnace, {ProvinceFieldEnum.dev: (2, 0)}),
    BuildingEnum.stable: BuildingType(BuildingEnum.stable, {}),
    BuildingEnum.stock: BuildingType(BuildingEnum.stock, {ProvinceFieldEnum.pm_cap: (1000, 0)}),
}

# TRADE CONFIG
MAX_FLOW = 0.5
PM_FROM_TRADE_MOD = 1.3
