from helpers import *
from controller import *
from db import *
from helpers import *
from province import *
from trade import *

from copy import copy
from typing import Callable


class State:
    def load(data: str) -> str:
        s = data.split(SEP)
        return State(int(s[0]), s[1], int(s[2]))

    def __init__(self, id: int, name: str = "", money: int = 0) -> Self:
        self.provinces = []
        self.id = id
        self.name = name
        self.money = money

    def __getattr__(self, item: str) -> Callable[[int], str]:
        def calc(region_id: int = -1):
            res = None
            for province in self.provinces:
                if region_id == -1 or province.trade_id == region_id:
                    if res is None:
                        res = copy(province.get(item))
                    else:
                        res += province.get(item)
            return res

        return calc

    def get(self, item: str) -> list | str | int:
        try:
            return self.__getattribute__(item)
        except AttributeError:
            return self.__getattr__(item)

    def save(self) -> str:
        return SEP.join(map(str, [self.id, self.name, self.money])) + SEP

    def __str__(self) -> str:
        return self.save()

    def __repr__(self) -> str:
        return str(self)
