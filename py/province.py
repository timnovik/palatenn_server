from helpers import *
from controller import *
from db import *
from helpers import *
from province import *
from state import *
from trade import *


class Buildings:
    def __init__(self, data=()):
        if not data:
            data = [0] * len(BuildingEnum)
        if type(data) == Buildings:
            self.__init__(str(data))
            return
        if type(data) == str:
            if data[-1] == SEP:
                data = data[:-1]
            data = list(map(int, data.split(SEP)))
        for i in range(len(BuildingEnum)):
            self.__setattr__(list(BuildingEnum)[i], data[i])

    def __iadd__(self, other):
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

    def __add__(self, other):
        res = self.__copy__()
        res += other
        return res

    def __getitem__(self, item):
        return self.__getattr__(item)

    def __str__(self):
        return SEP.join(map(lambda building: str(self[building]), BuildingEnum))

    def __repr__(self):
        return str(self)

    def __copy__(self):
        return Buildings(str(self))

    def __getattr__(self, item):
        if type(item) == BuildingEnum:
            item = item.name
        return self.__getattribute__(item)

    def __setattr__(self, key, value):
        if type(key) == BuildingEnum:
            key = key.name
        self.__dict__[key] = value

    def impact(self, val, mode):
        if type(val) != ProvinceFieldEnum:
            val = Province.Field(val)
        res = 0
        for building_type, building in BUILDINGS.items():
            res += building.impact(self.__getattr__(building_type), val, mode)
        return res


class Province:
    Field = ProvinceFieldEnum
    Query = ProvinceQueryEnum

    def __init__(self, val, id=0, state_id=0, trade_id=0, pop=0, urb=0, goods_cost=0, dev=0, buildings=""):
        self.state = None
        self.region = None
        self._pm_cap = 0
        if type(val) == list:
            self.name = val[0]
            self.id, self.state_id, self.trade_id, self._pop, self._urban, self._goods_cost, self._dev = val[1:-len(BuildingEnum)]
            self.buildings = Buildings(val[-len(BuildingEnum):])

        elif type(val) == str and SEP in val:
            val = val.strip()
            if val[-1] == SEP:
                val = val[:-1]
            str_list = val.replace(",", ".").split(SEP)
            self.name = str_list[0]
            str_list.pop(0)
            if "." in str_list[URB_POS]:
                str_list[URB_POS] = float(str_list[URB_POS]) * URB_MUL
            if "." in str_list[GC_POS]:
                str_list[GC_POS] = float(str_list[GC_POS]) * GC_MUL
            self.id, self.state_id, self.trade_id, self._pop, self._urban, self._goods_cost, self._dev, *buildings = map(int, str_list)
            self.buildings = Buildings(buildings)

        else:
            self.name = val
            self.id, self.state_id, self.trade_id, self._pop, self._urban, self._goods_cost, self._dev, self.buildings =\
                (id, state_id, trade_id, pop, urb, goods_cost, dev, Buildings(buildings))
            if type(self._urban) == float:
                self._urban *= URB_MUL
                self._urban = int(self._urban)
            if type(self._goods_cost) == float:
                self._goods_cost *= GC_MUL
                self._goods_cost = int(self._goods_cost)

    def __str__(self):
        return SEP.join(map(str, [self.name, self.id, self.state_id, self.trade_id, self._pop, self._urban, self._goods_cost, self._dev, self.buildings])) + SEP

    def __repr__(self):
        return str(self)

    def __getattr__(self, item):
        if item[0] == "_":
            item = item[1:]
            if item == Province.Field.pm.name:
                return self.pop * self.urban * self.dev // URB_MUL
            if item == Province.Field.tv.name:
                return self.pm_base * self.urban * self.goods_cost // (URB_MUL * GC_MUL)
            if item == ProvinceFieldEnum.ap.name:
                return 0
            return self.__getattribute__("_" + item)

        try:
            parsed_args = item.split("_")
            field, mode = Province.Field("_".join(parsed_args[:-1])), Province.Query(parsed_args[-1])
        except:
            field, mode = Province.Field(item), Province.Query.total

        if mode == Province.Query.base:
            return self.get(field)
        if mode == Province.Query.add:
            return self.buildings.impact(field, 0)
        if mode == Province.Query.mul:
            mod = 0
            if field == Province.Field.pm:
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
        if mode == Province.Query.total:
            return int((self.get(field, Province.Query.base)
                        + self.get(field, Province.Query.add))
                       * (ACC + self.get(field, Province.Query.mul)) // ACC)
        raise AttributeError("Province attribute error: no attribute " + item)

    def get(self, field, query=ProvinceQueryEnum.base):
        if type(field) == str:
            try:
                return self.__getattribute__(field)
            except AttributeError:
                return self.__getattr__(field)
        if query == ProvinceQueryEnum.base:
            return self.__getattr__("_" + field.name)
        return self.__getattr__(field.name + "_" + query.name)
