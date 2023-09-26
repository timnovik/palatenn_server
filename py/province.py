from helpers import *
from controller import *
from db import *
from helpers import *
from province import *
from state import *
from trade import *
from typing import Iterable, Self


class Buildings:
    def load(data: str) -> str:
        if not data:
            return Buildings()
        if data[-1] == SEP:
            data = data[:-1]
        data = list(map(int, data.split(SEP)))
        return Buildings(data)

    def __init__(self, data: Iterable = ()) -> Self:
        if not data:
            data = [0] * len(BuildingEnum)
        if type(data) == Buildings:
            self.__init__(str(data))
            return
        for building, val in zip(BuildingEnum, data):
            self.__setattr__(building, val)

    def __iadd__(self, other: Self | BuildingEnum | str) -> Self:
        if type(other) == Buildings:
            for building in BuildingEnum:
                self.__setattr__(building, self[building] + other[building])
            return self
        cnt = 1
        if type(other) == str and SEP in other:
            other, cnt = other.split(SEP)
            cnt = int(cnt)
        other = BuildingEnum(other)
        if other == BuildingEnum.city:
            self += BuildingEnum.block * cnt
        self.__setattr__(other, self[other] + cnt)
        return self

    def __add__(self, other: Self | BuildingEnum | str) -> Self:
        res = self.__copy__()
        res += other
        return res

    def __getitem__(self, item: str) -> int:
        return self.__getattr__(item)

    def save(self) -> str:
        return SEP.join(map(lambda building: str(self[building]), BuildingEnum))

    def __str__(self) -> str:
        return self.save()

    def __repr__(self) -> str:
        return str(self)

    def __copy__(self) -> str:
        return Buildings(str(self))

    def __getattr__(self, item: BuildingEnum | str) -> int:
        if type(item) == BuildingEnum:
            item = item.name
        return self.__getattribute__(item)

    def __setattr__(self, key: BuildingEnum | str, value: int) -> None:
        if type(key) == BuildingEnum:
            key = key.name
        self.__dict__[key] = value

    def impact(self, val: ProvinceFieldEnum, mode: int) -> int:
        if type(val) != ProvinceFieldEnum:
            val = ProvinceFieldEnum(val)
        res = 0
        for building_type, building in BUILDINGS.items():
            res += building.impact(self.__getattr__(building_type), val, mode)
        return res


class Province:
    def load(data: str) -> str:
        data = data.strip()
        if data[-1] == SEP:
            data = data[:-1]
        str_list = data.replace(",", ".").split(SEP)
        name = str_list[0]
        if "." in str_list[URB_POS]:
            str_list[URB_POS] = float(str_list[URB_POS]) * URB_MUL
        if "." in str_list[GC_POS]:
            str_list[GC_POS] = float(str_list[GC_POS]) * GC_MUL
        values = str_list[1:-len(BuildingEnum)]
        return Province(name, *map(int, values), SEP.join(str_list[-len(BuildingEnum):]))

    def __init__(self, val: Iterable | str, id: int = 0, state_id: int = 0, trade_id: int = 0, pop: int = 0, urb: int | float = 0, goods_cost: int | float = 0, dev: int = 0, buildings: Buildings | str = "") -> Self:
        self.state = None
        self.region = None
        self._pm_cap = 0
        if type(val) == Iterable:
            self.name = val[0]
            self.id, self.state_id, self.trade_id, self._pop, self._urban, self._goods_cost, self._dev = val[1:-len(BuildingEnum)]
            self.buildings = Buildings(val[-len(BuildingEnum):])
        else:
            self.name = val
            self.id, self.state_id, self.trade_id, self._pop, self._urban, self._goods_cost, self._dev, self.buildings =\
                (id, state_id, trade_id, pop, urb, goods_cost, dev, Buildings.load(buildings))
            if type(self._urban) == float:
                self._urban *= URB_MUL
                self._urban = int(self._urban)
            if type(self._goods_cost) == float:
                self._goods_cost *= GC_MUL
                self._goods_cost = int(self._goods_cost)

    def save(self) -> str:
        return SEP.join(map(str, [self.name, self.id, self.state_id, self.trade_id, self._pop, self._urban, self._goods_cost, self._dev, self.buildings])) + SEP

    def __str__(self) -> str:
        return self.save()

    def __repr__(self) -> str:
        return str(self)

    def __getattr__(self, item: ProvinceFieldEnum | str) -> int | str:
        if item[0] == "_":
            item = item[1:]
            if item == ProvinceFieldEnum.pm.name:
                return self.pop * self.urban * self.dev // URB_MUL
            if item == ProvinceFieldEnum.tv.name:
                return self.pm_base * self.urban * self.goods_cost // (URB_MUL * GC_MUL)
            if item == ProvinceFieldEnum.ap.name:
                return 0
            return self.__getattribute__("_" + item)

        try:
            parsed_args = item.split("_")
            field, mode = ProvinceFieldEnum("_".join(parsed_args[:-1])), ProvinceQueryEnum(parsed_args[-1])
        except:
            field, mode = ProvinceFieldEnum(item), ProvinceQueryEnum.total

        if mode == ProvinceQueryEnum.base:
            return self.get(field)
        if mode == ProvinceQueryEnum.add:
            return self.buildings.impact(field, 0)
        if mode == ProvinceQueryEnum.mul:
            mod = 0
            if field == ProvinceFieldEnum.pm:
                this_tv = self.region.tv()
                avg_tv = self.region.avg_neighbors_tv()
                mod = PM_FROM_TRADE_MOD * (1 - min(this_tv, avg_tv) / max(this_tv, avg_tv))
                if mod > MAX_FLOW:
                    mod = MAX_FLOW
                if this_tv < avg_tv:
                    mod *= -1
                part = self.state.tv(self.trade_id) / this_tv
                mod *= part ** 0.5
            return mod + self.buildings.impact(field, 1)
        if mode == ProvinceQueryEnum.total:
            return int((self.get(field, ProvinceQueryEnum.base)
                        + self.get(field, ProvinceQueryEnum.add))
                       * (ACC + self.get(field, ProvinceQueryEnum.mul)) // ACC)
        raise AttributeError("Province attribute error: no attribute " + item)

    def get(self, field: ProvinceFieldEnum | str, query: ProvinceQueryEnum = ProvinceQueryEnum.base) -> int | str:
        if type(field) == str:
            try:
                return self.__getattribute__(field)
            except AttributeError:
                return self.__getattr__(field)
        if query == ProvinceQueryEnum.base:
            return self.__getattr__("_" + field.name)
        return self.__getattr__(field.name + "_" + query.name)
