from config import *
from province import Province
from state import State

state = State(0)
provinces = [
    Province(0, 0, 16000, .22, 2.1, 6),
    Province(1, 0, 10000, .17, 1.7, 4)
]

with open("data/provinces.csv", "w") as province_db:
    for province in provinces:
        print(province, file=province_db)

with open("data/provinces.csv", "r") as province_db:
    for line in province_db.readlines():
        print(Province(line))
