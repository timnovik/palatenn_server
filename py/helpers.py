from enum import Enum
from typing import Self
from host import *

# AUTH CONFIG
ADMIN_KEY_HASH = "21095e62f04a16b069b02ae0b8d6ec404b502a232f1d73b275642569de3fbe85"

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

    def __mul__(self, other: Self) -> str:
        return self.name + SEP + str(other)


class ActionData:
    def __init__(self, id: int) -> Self:
        self.id = id


class Cost:
    def __init__(self, money: int = 0, pm: int = 0, ap: int = 0) -> Self:
        self.money = money
        self.pm = pm
        self.ap = ap

    def __iadd__(self, other: Self) -> Self:
        self.money += other.money
        self.pm += other.pm
        self.ap += other.ap
        return self

    def __add__(self, other: Self) -> Self:
        res = Cost(self.money, self.pm, self.ap)
        res += other
        return res
    
    def __imul__(self, other: int) -> Self:
        self.money *= other
        self.pm *= other
        self.ap *= other
        return self

    def __mul__(self, other: int) -> Self:
        res = Cost(self.money, self.pm, self.ap)
        res *= other
        return res

    def save(self) -> str:
        return SEP.join(map(str, [self.money, self.pm, self.ap])) + SEP

    def __str__(self) -> str:
        return f"money - {self.money}, pm - {self.pm}, ap - {self.ap}"

    def __repr__(self) -> str:
        return str(self)


class BuildActionData(ActionData):
    def __init__(self, build_type: BuildingEnum, count: int, province_id: int, id: int = -1) -> Self:
        ActionData.__init__(self, id)
        self.build_type = build_type
        self.count = count
        self.province_id = province_id

    def calc_cost(self) -> Cost:
        return BUILDINGS[self.build_type].cost * self.count

    def save(self) -> str:
        return SEP.join([self.build_type.name, str(self.count), str(self.province_id)])

    def __str__(self) -> str:
        return f"{self.id}: {self.count}*{self.build_type} in prov #{self.province_id}"

    def __repr__(self) -> str:
        return str(self)


class BuildingType:
    def __init__(self, building: BuildingEnum, impact: dict[ProvinceFieldEnum, tuple[int, int]], cost: Cost = Cost()) -> Self:
        self.building = building
        self.cost = cost
        self._impact = {field: impact.get(field, (0, 0)) for field in ProvinceFieldEnum}

    def impact(self, cnt: int, field: ProvinceFieldEnum, mode: int) -> int:
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
