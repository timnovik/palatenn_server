from config import *
from state import State
from province import Province


class TradeRegion:
    def __init__(self, id_, name="", neighbor_ids=()):
        self.states = []
        self.provinces = []
        self.neighbors = []
        if type(id_) == str:
            s = id_.split(SEP)
            self.id = int(s[0])
            self.name = s[1]
            self.neighbor_ids = tuple(map(int, s[2].split(",")))
        else:
            self.id = id_
            self.name = name
            self.neighbor_ids = neighbor_ids

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

    def avg_neighbors_tv(self):
        n = len(self.neighbor_ids)
        total = 0
        for neighbor in self.neighbors:
            total += neighbor.tv()
        return total // n

    def get(self, item):
        return self.__getattribute__(item)
