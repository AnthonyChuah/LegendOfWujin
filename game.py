import random
import math
import sys

# Strength str affects melee damage and allows wearing heavier armour.
# Dexterity dex affects success rate of fleeing and allows learning skills.
# Intelligence int affects spell power and allows learning spells.
# Hitpoints hp is your life: once it hits 0 or below you are dead.
# Stamina sta is used to perform skills.
# Mind mn is used for casting spells.
# Experience exp counts progress towards gaining levels.
# Level shows character level.
# To-next-level tnl shows how much exp is needed to gain the next level.
# Tnl = level * 10.
attributes = {
    "str": 10,
    "dex": 10,
    "int": 10,
    "maxhp": 50,
    "maxsta": 40,
    "maxmn": 40,
    "exp": 0,
    "level": 1,
    "tnl": 10
}
levelincrease = {
    "str": 2,
    "dex": 2,
    "int": 2,
    "maxhp": 10,
    "maxsta": 8,
    "maxmn": 8
}
# There are 6 equipment slots.
equipment = {
    "mainhand": "knife",
    "offhand": None,
    "body": "cloth tunic",
    "legs": "cloth trousers",
    "feet": "sandals",
    "hands": None
}
gold = 50
# Inventory space is unlimited.
inventory = [
    "cloth gloves",
    "wooden buckler"
]

# print(attributes)
# print(levelincrease)
# print(equipment)
# print(gold)
# print(inventory)
# sys.exit()

itemstats = dict()
# Weapon stats [x,y,z] indicates: minimum dmg x, max dmg y.
# Each die's outcome is a discrete uniform distribution over
# the range 1 to y.
itemstats["weapon"] = {
    "knife": [1, 3, 25],
    "dagger": [1, 4, 40],
    "hammer": [2, 2, 55],
    "hatchet": [1, 6, 70],
    "butterfly-sword": [2, 3, 90],
    "axe": [1, 8, 105],
    "da-dao": [1, 9, 115],
    "jian": [2, 4, 140],
    "meteor-hammer": [3, 2, 140]
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
    for item in itemtype:
        # Each item is "cloth tunic" for example, and its lookup value is
        # ["body",3,30] for example.
        itemstats_flat[item] = itemtype[item]

print(itemstats)
print(itemstats_flat)
sys.exit()

skills = {
    "atk": "normal attack; 1 stamina",
    "def": "defensive attack has increased block chance; 1 stamina",
    "str": "heavy attack has decreased block chance; 1 stamina",
    "shatter": "ignores enemy defence; 3 stamina; scales with str",
    "bash": "has chance to deny enemy attack; 3 stamina; chance scales with str",
    "sunder": "light attack reduces enemy defence; 4 stamina; reduction scales with dex",
    "weaken": "light attack reduces enemy offence; 4 stamina; reduction scales with dex",
    "charge": "attacks with high offence dealing more damage if enemy hp is high; 5 stamina; scales with str",
    "flurry": "attacks 2 to 4 times; 8 stamina, scales with the sum of str and dex"
}
spelldesc = {
    "mm": "magic missile deals low damage; costs 1 mind; combat only",
    "heal": "heals 10 hp; costs 2 mind",
    "refresh": "restores 10 stamina; costs 3 mind",
    "barrier": "increases defence; 4 mind; fades after combat",
    "enfeeble": "decreases enemy offence; 4 mind; combat only"
}



commands = {
  "north":"go north",
  "south":"go south",
  "east":"go east",
  "west":"go west",
  "quit":"quit the game",
  "shop":"buy or sell items",
  "learn":"learn spells",
  "train":"train in skills, only in town",
  "rest":"rest; more effective in town",
  "inv":"display inventory",
  "eq":"display equipment",
  "hunt":"look for an enemy to fight",
  "cast [spell]":"cast [spell] from your spellbook",
  "skill [skill]":"perform [skill]",
  "flee":"flee from a fight",
  "wear [item]":"equip [item]",
  "look":"looks at your current room"
}

class Creature(object):
  def __init__(self):
    self.name = ""

class Mob(object):
  def __init__(self,name,hp,defence,attack,expgiven):
    self.name = name
    self.hp = hp
    self.defence = defence
    self.attack = attack
    self.expgiven = expgiven

class Player(object):
  def __init__(self):
    Creature.__init__(self)
    self.state = "normal"
    self.stats = attributes
    self.hp = attributes.get("maxhp")
    self.stamina = attributes.get("maxsta")
    self.mind = attributes.get("maxmind")
    self.room = "Town"
    self.inventory = [
      "thin gloves",
      "wooden buckler"
    ]
  def quit(self):
    print("You give up on your life and commit suicide.")
    self.hp = 0
  def help(self):
    print(commands)

class Item(object):
  def __init__(self,name,desc,cost):
    self.name = name
    self.desc = desc
    self.cost = cost

class Weapon(object):
  def __init__(self,name,desc,cost,mindmg,maxdmg):
    Item.__init__(self,name,desc,cost)
    self.mindmg = mindmg
    self.maxdmg = maxdmg

# Armour has deflection value which adds to defence. 
class Armour(object):
  def __init__(self,name,desc,cost,slot,deflect):
    Item.__init__(self,name,desc,cost)
    self.deflect = itemstats["armour"][name][2]
