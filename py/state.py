from config import *
from province import Province


class State:
    def __init__(self, id_, name=""):
        self.provinces = []
        if type(id_) == str:
            s = id_.split(SEP)
            self.id = int(s[0])
            self.name = s[1]
        else:
            self.id = id_
            self.name = name

    def __getattr__(self, item):
        def calc(region_id=-1):
            res = 0
            for province in self.provinces:
                if region_id == -1 or province.trade_id == region_id:
                    res += province.get(item)
            return res

        return calc

    def get(self, item):
        return self.__getattribute__(item)

    def __str__(self):
        return SEP.join(map(str, [self.id, self.name])) + ";"

    def __repr__(self):
        return str(self)
