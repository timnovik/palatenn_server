from config import *
from state import State
from province import Province


class TradeRegion:
    def __init__(self, name, id=0):
        self.states = []
        self.provinces = []
        if ";" not in name:
            self.name = name
            self.id = id
        else:
            s = name.split(SEP)
            self.name = s[1]
            self.id = int(s[0])

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
