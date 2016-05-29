itemstats = OrderedDict()
# Weapon stats [x,y,z] indicates: minimum dmg x, max dmg y.
# Each die's outcome is a discrete uniform distribution over
# the range 1 to y.
itemstats["weapon"] = OrderedDict()
itemstats["weapon"]
itemstats["weapon"]
itemstats["weapon"]
itemstats["weapon"]
itemstats["weapon"]
itemstats["weapon"]
itemstats["weapon"]
itemstats["weapon"]
itemstats["weapon"]

{
    "knife": [1, 3, 25],
    "dagger": [1, 4, 40],
    "hammer": [2, 4, 55],
    "hatchet": [1, 6, 70],
    "butterfly-sword": [2, 6, 90],
    "axe": [1, 8, 105],
    "da-dao": [1, 9, 115],
    "jian": [2, 9, 140],
    "meteor-hammer": [3, 8, 145]
}
# Shields offer blockvalue, which increase the probability of blocking.
# Blocking consumes stamina.
# If enemy attack value is greater than double the blockvalue, the
# shield breaks completely.
# [x,z] where x is blockvalue and z is cost.
itemstats["shield"] = {
    "wooden buckler": [5, 25],
    "bronze buckler": [7, 35],
    "wooden shield": [8, 40],
    "iron buckler": [9, 48],
    "bronze shield": [10, 55],
    "steel buckler": [12, 80],
    "iron shield": [13, 90],
    "steel shield": [15, 115]
}
# Armour has a slot (feet, body, etc.) and armour value.
# [x,y,z] where x is slot, y is armour value, and z is cost.
itemstats["armour"] = {
    "cloth tunic": ["body", 3, 30],
    "leather jerkin": ["body", 4, 40],
    "ring mail shirt": ["body", 5, 55],
    "chain mail shirt": ["body", 6, 70],
    "light breastplate": ["body", 7, 85],
    "heavy breastplate": ["body", 8, 100],
    "cloth trousers": ["legs", 2, 20],
    "leather leggings": ["legs", 3, 30],
    "mail leggings": ["legs", 4, 40],
    "plate leggings": ["legs", 5, 55],
    "sandals": ["feet", 1, 8],
    "shoes": ["feet", 2, 18],
    "boots": ["feet", 3, 30],
    "reinforced steel boots": ["feet", 4, 40],
    "cloth gloves": ["hands", 1, 8],
    "leather gloves": ["hands", 2, 18],
    "heavy leather gauntlets": ["hands", 3, 30],
    "mail gauntlets": ["hands", 4, 40]
}
itemstats_flat = dict()
for itemtype in itemstats:
    # Each itemtype will be itemstats["weapon"] etc.
    # itemtype is itself a dict nested inside the itemstats dict.
    
    for item in itemstats[itemtype]:
        # Each item is "cloth tunic" for example, and its lookup value is
        # ["body",3,30] for example.
        itemstats_flat[item] = itemstats[itemtype][item]

# print(itemstats)
# print(itemstats_flat)
# sys.exit()