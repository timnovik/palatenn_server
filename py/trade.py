from helpers import *
from controller import *
from db import *
from helpers import *
from province import *
from state import *
from trade import *

from typing import Iterable, Self


class TradeRegion:
    def load(data: str) -> str:
        s = data.split(SEP)
        return TradeRegion(int(s[0]), s[1], tuple(map(int, s[2].split(","))))

    def __init__(self, id: int, name: str = "", neighbor_ids: Iterable = ()) -> Self:
        self.states = []
        self.provinces = []
        self.neighbors = []
        self.id = id
        self.name = name
        self.neighbor_ids = neighbor_ids

    def save(self) -> str:
        return SEP.join(map(str, [self.id, self.name, ",".join(map(str, self.neighbor_ids))])) + SEP

    def __str__(self) -> str:
        return self.save()

    def __repr__(self) -> str:
        return str(self)

    def tv(self) -> int:
        if self.provinces is None:
            return 0
        res = 0
        for province in self.provinces:
            res += province.tv
        return res

    def avg_neighbors_tv(self) -> int:
        n = len(self.neighbor_ids)
        total = 0
        for neighbor in self.neighbors:
            total += neighbor.tv()
        return total // n

    def get(self, item: str) -> Iterable | str | int:
        return self.__getattribute__(item)
