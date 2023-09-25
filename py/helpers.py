from enum import Enum

# NETWORK CONFIG
HOST_IP = "127.0.0.1"
HOST_PORT = 5000

# DATABASE CONFIG
SEP = ";"
URB_POS = 4
GC_POS = 5

DB_PATH = "data"
PROVINCE_PATH = "provinces.csv"
STATE_PATH = "states.csv"
REGION_PATH = "regions.csv"

# ACCURACY CONFIG
ACC = 100      # точность вычисления процентных модификаторов
URB_MUL = 100  # точность вычисления урбанизации
GC_MUL = 100   # точность вычисления стоимости товаров

# PM IMPACT CONFIG
MIN_DISC = 0.9

# QUERIES CONFIG
class ControllerStatusEnum(Enum):
    ok = 0
    bad_ap = 1
    money_overdraft = 2
    unknown = -666


class ActionEnum(Enum):
    build = "build"


class ProvinceFieldEnum(Enum):
    pop = "pop"
    urban = "urban"
    goods_cost = "goods_cost"
    dev = "dev"
    pm = "pm"
    pm_cap = "pm_cap"
    tv = "tv"
    ap = "ap"


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


class ActionData:
    def __init__(self, id):
        self.id = id


class BuildActionData(ActionData):
    def __init__(self, build_type, count, province_id, id=-1):
        ActionData.__init__(self, id)
        self.build_type = build_type
        self.count = count
        self.province_id = province_id

    def calc_cost(self):
        return BUILDINGS[self.build_type].cost * self.count


class Cost:
    def __init__(self, money=0, pm=0, ap=0):
        self.money = money
        self.pm = pm
        self.ap = ap

    def __iadd__(self, other):
        self.money += other.money
        self.pm += other.pm
        self.ap += other.ap
        return self

    def __add__(self, other):
        res = Cost(self.money, self.pm, self.ap)
        res += other
        return res
    
    def __imul__(self, other):
        self.money *= other
        self.pm *= other
        self.ap *= other
        return self

    def __mul__(self, other):
        res = Cost(self.money, self.pm, self.ap)
        res *= other
        return res


class BuildingType:
    def __init__(self, building, impact, cost=Cost()):
        self.building = building
        self.cost = cost
        self._impact = {field: impact.get(field, (0, 0)) for field in ProvinceFieldEnum}

    def impact(self, cnt, field, mode):
        return cnt * self._impact[field][mode]


BUILDINGS = {
    BuildingEnum.city: 
        BuildingType(
            BuildingEnum.city, 
            {
                ProvinceFieldEnum.urban: (5, 0), 
                ProvinceFieldEnum.dev: (5, 0)
            }, 
            Cost(0, 0, 0)
        ),
    BuildingEnum.block: 
        BuildingType(
            BuildingEnum.block, 
            {
                ProvinceFieldEnum.dev: (1, 0), 
                ProvinceFieldEnum.ap: (1, 0)
            }, 
            Cost(0, 0, 0)
        ),
    BuildingEnum.road: 
        BuildingType(
            BuildingEnum.road, 
            {
                ProvinceFieldEnum.dev: (0, 10)
            }, 
            Cost(0, 0, 0)
        ),
    BuildingEnum.bridge: 
        BuildingType(
            BuildingEnum.bridge, 
            {
                ProvinceFieldEnum.dev: (0, 10)
            }, 
            Cost(0, 0, 0)
        ),
    BuildingEnum.mine: 
        BuildingType(
            BuildingEnum.mine, 
            {
                ProvinceFieldEnum.dev: (3, 0)
            }, 
            Cost(0, 0, 0)
        ),
    BuildingEnum.market: 
        BuildingType(
            BuildingEnum.market, 
            {
                ProvinceFieldEnum.goods_cost: (100, 0)
            }, 
            Cost(0, 0, 0)
        ),
    BuildingEnum.trading_post: 
        BuildingType(
            BuildingEnum.trading_post, 
            {
                ProvinceFieldEnum.tv: (0, 10)
            }, 
            Cost(0, 0, 0)
        ),
    BuildingEnum.port: 
        BuildingType(
            BuildingEnum.port, 
            {
                ProvinceFieldEnum.dev: (1, 0)
            }, 
            Cost(0, 0, 0)
        ),
    BuildingEnum.shipyard: 
        BuildingType(
            BuildingEnum.shipyard, 
            {
                ProvinceFieldEnum.dev: (1, 0)
            }, 
            Cost(0, 0, 0)
        ),
    BuildingEnum.workshop: 
        BuildingType(
            BuildingEnum.workshop, 
            {
                ProvinceFieldEnum.dev: (1, 0)
            }, 
            Cost(0, 0, 0)
        ),
    BuildingEnum.barracks: 
        BuildingType(
            BuildingEnum.barracks, 
            {
            }, 
            Cost(0, 0, 0)
        ),
    BuildingEnum.forge: 
        BuildingType(
            BuildingEnum.forge, 
            {
                ProvinceFieldEnum.dev: (1, 0)
            }, 
            Cost(0, 0, 0)
        ),
    BuildingEnum.furnace: 
        BuildingType(
            BuildingEnum.furnace, 
            {
                ProvinceFieldEnum.dev: (2, 0)
            }, 
            Cost(0, 0, 0)
        ),
    BuildingEnum.stable: 
        BuildingType(
            BuildingEnum.stable, 
            {
            }, 
            Cost(0, 0, 0)
        ),
    BuildingEnum.stock: 
        BuildingType(
            BuildingEnum.stock, 
            {
                ProvinceFieldEnum.pm_cap: (1000, 0)
            }, 
            Cost(0, 0, 0)
        ),
}

# TRADE CONFIG
MAX_FLOW = 0.5
PM_FROM_TRADE_MOD = 1.3
