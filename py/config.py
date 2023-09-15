SEP = ";"

ACC = 100      # точность вычисления процентных модификаторов
URB_MUL = 100  # точность вычисления урбанизации
GC_MUL = 100   # точность вычисления стоимости товаров

# для добавления нового здания НЕОБХОДИМО добавить его в этот список, даже если здание не влияет на экономику
BUILDINGS_IMPACT = {
    "city": {"urban": (5, 0), "dev": (5, 0)},
    "block": {"urban": (1, 0)},
    "road": {"dev": (0, 10)},
    "bridge": {"dev": (0, 10)},
    "mine": {"dev": (3, 0)},
    "market": {"goods_cost": (100, 0)},
    "trading_post": {"tv": (0, 10)},
    "port": {"dev": (1, 0)},
    "shipyard": {"dev": (1, 0)},
    "workshop": {"dev": (1, 0)},
    "barracks": {},
    "forge": {"dev": (1, 0)},
    "furnace": {"dev": (2, 0)},
    "stable": {},
    "stock": {"pm_cap": (1000, 0)},
}

BUILDINGS = list(BUILDINGS_IMPACT.keys())
