from config import *


class Buildings:
    def __init__(self, data=()):
        if not data:
            data = [0] * len(BUILDINGS)
        if type(data) == Buildings:
            self.__init__(str(data))
            return
        if type(data) == str:
            data = list(map(int, data.split(SEP)))
        for i in range(len(BUILDINGS)):
            self.__setattr__(BUILDINGS[i], data[i])

    def __iadd__(self, other):
        cnt = 1
        if SEP in other:
            other, cnt = other.split(SEP)
            cnt = int(cnt)
        self.__setattr__(other, self.__getattribute__(other) + cnt)
        return self

    def __add__(self, other):
        res = self.__copy__()
        res += other
        return res

    def __str__(self):
        return SEP.join(map(lambda building: str(self.__getattribute__(building)), BUILDINGS))

    def __copy__(self):
        return Buildings(str(self))

    def impact(self, val, mode):
        res = 0
        for building in BUILDINGS:
            res += self.__getattribute__(building) * BUILDINGS_IMPACT[building].get(val, (0, 0))[mode]
        return res


class Province:
    def __init__(self, val, state_id=0, pop=0, urb=0, goods_cost=0, dev=0, buildings=""):
        self._pm_cap = 0
        if type(val) == list:
            self.id, self.state_id, self._pop, self._urban, self._goods_cost, self._dev = val[:-len(BUILDINGS)]
            self.buildings = Buildings(val[-len(BUILDINGS):])

        elif type(val) == str:
            str_list = val.replace(",", ".").split(SEP)
            if "." in str_list[3]:
                str_list[3] = float(str_list[3]) * URB_MUL
            if "." in str_list[4]:
                str_list[4] = float(str_list[4]) * GC_MUL
            self.id, self.state_id, self._pop, self._urban, self._goods_cost, self._dev, *buildings = map(int, str_list)
            self.buildings = Buildings(buildings)

        else:
            self.id, self.state_id, self._pop, self._urban, self._goods_cost, self._dev, self.buildings = (
                val, state_id, pop, urb, goods_cost, dev, Buildings(buildings))
            if type(self._urban) == float:
                self._urban *= URB_MUL
                self._urban = int(self._urban)
            if type(self._goods_cost) == float:
                self._goods_cost *= GC_MUL
                self._goods_cost = int(self._goods_cost)

    def __str__(self):
        return SEP.join(map(str, [self.id, self.state_id, self._pop, self._urban, self._goods_cost, self._dev])) + ";" + str(self.buildings)

    def __getattr__(self, item):
        # Получение базовых значений
        if item[0] == "_":
            if item == "_pm":
                return self.pop * self.urban * self.dev // URB_MUL
            if item == "_tv":
                return self.pm * self.urban * self.goods_cost // (URB_MUL * GC_MUL)
            return self.__getattribute__(item)

        parsed_args = item.split("_")
        if parsed_args[-1] not in ["base", "add", "mul", "total"]:
            parsed_args.append("total")
        field, mode = "_".join(parsed_args[:-1]), parsed_args[-1]

        if mode == "base":
            return self.__getattr__("_" + field)
        if mode == "add":
            return self.buildings.impact(field, 0)
        if mode == "mul":
            return self.buildings.impact(field, 1)
        if mode == "total":
            return ((self.__getattr__(field + "_base")
                     + self.__getattr__(field + "_add"))
                    * (ACC + self.__getattr__(field + "_mul")) // ACC)
        raise AttributeError("Province attribute error: no attribute " + item)
