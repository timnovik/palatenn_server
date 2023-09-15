from config import *
from province import Province
import json


class State:
    def __init__(self, id_, name=""):
        self.provinces = []
        if type(id_) == str:
            s = id_.split(SEP)
            self.id = int(s[0])
            self.name = s[1]
        else:
            self.id = id
            self.name = name

    def __str__(self):
        return SEP.join(map(str, [self.id, self.name])) + ";"

    def __repr__(self):
        return str(self)
