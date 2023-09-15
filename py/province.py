from config import URB_MUL, GC_MUL, SEP, BUILDINGS


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


class Province:
    def __init__(self, val, urb=0, goods_cost=0, dev=0, buildings=""):
        if type(val) == list:
            self._pop, self._urban, self._goods_cost, self._dev = val[:-len(BUILDINGS)]
            self.buildings = Buildings(val[-len(BUILDINGS):])

        elif type(val) == str:
            str_list = val.replace(",", ".").split(SEP)
            if "." in str_list[1]:
                str_list[1] = float(str_list[1]) * URB_MUL
            if "." in str_list[2]:
                str_list[2] = float(str_list[2]) * GC_MUL
            self._pop, self._urban, self._goods_cost, self._dev, _buildings = map(int, str_list)
            self.buildings = Buildings(_buildings)

        else:
            self._pop, self._urban, self._goods_cost, self._dev, self.buildings = val, urb, goods_cost, dev, Buildings(buildings)
            if type(self._urban) == float:
                self._urban *= URB_MUL
                self._urban = int(self._urban)
            if type(self._goods_cost) == float:
                self._goods_cost *= GC_MUL
                self._goods_cost = int(self._goods_cost)

    def __str__(self):
        return SEP.join(map(str, [self._pop, self._urban, self._goods_cost, self._dev])) + ";" + str(self.buildings)

    def __getattr__(self, item):
        if item == "pop_add_mod":
            return 0
        if item == "pop_mul_mod":
            return 0
        if item == "pop":
            return (self._pop + self.pop_add_mod) * (1 + self.pop_mul_mod)

        if item == "urban_add_mod":
            return 0
        if item == "urban_mul_mod":
            return 0
        if item == "urban":
            return (self._urban + self.urban_add_mod) * (1 + self.urban_mul_mod)

        if item == "goods_cost_add_mod":
            return 0
        if item == "goods_cost_mul_mod":
            return 0
        if item == "goods_cost":
            return (self._goods_cost + self.goods_cost_add_mod) * (1 + self.goods_cost_mul_mod)

        if item == "dev_add_mod":
            return 0
        if item == "dev_mul_mod":
            return 0
        if item == "dev":
            return (self._dev + self.dev_add_mod) * (1 + self.dev_mul_mod)

        if item == "pm_add_mod":
            return 0
        if item == "pm_mul_mod":
            return 0
        if item == "pm":
            return self.pop * self.urban * self.dev // URB_MUL


if __name__ == "__main__":
    province = Province(16000, .22, 2.1, 6)
    print(province.pm)
