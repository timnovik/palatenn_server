from config import *
from state import State
from province import Province


class TradeRegion:
    def __init__(self, id_, name=""):
        self.states = []
        self.provinces = []
        if type(id_) == str:
            s = id_.split(SEP)
            self.name = s[1]
            self.id = int(s[0])
        else:
            self.name = name
            self.id = id_

    def __str__(self):
        return SEP.join(map(str, [self.id, self.name])) + ";"

    def __repr__(self):
        return str(self)

    def tv(self):
        if self.provinces is None:
            return 0
        res = 0
        for province in self.provinces:
            res += province.tv
        return res
