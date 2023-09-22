from helpers import *
from controller import *
from db import *
from helpers import *
from province import *
from trade import *

from copy import copy


class State:
    def __init__(self, id, name="", money=0):
        self.provinces = []
        if type(id) == str:
            s = id.split(SEP)
            self.id = int(s[0])
            self.name = s[1]
            self.money = int(s[2])
        else:
            self.id = id
            self.name = name
            self.money = money

    def __getattr__(self, item):
        def calc(region_id=-1):
            res = None
            for province in self.provinces:
                if region_id == -1 or province.trade_id == region_id:
                    if res is None:
                        res = copy(province.get(item))
                    else:
                        res += province.get(item)
            return res

        return calc

    def get(self, item):
        try:
            return self.__getattribute__(item)
        except AttributeError:
            return self.__getattr__(item)

    def __str__(self):
        return SEP.join(map(str, [self.id, self.name, self.money])) + SEP

    def __repr__(self):
        return str(self)
