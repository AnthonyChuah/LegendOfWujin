import random
import math
import sys
from collections import OrderedDict

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

# These are initial attributes, subject to change when gaining exp and levelling up. 

attributes = OrderedDict()
attributes["str"] = 10
attributes["dex"] = 10
attributes["int"] = 10
attributes["maxhp"] = 50
attributes["maxsta"] = 40
attributes["maxmn"] = 40
attributes["exp"] = 0
attributes["level"] = 1
attributes["tnl"] = 10

def PrintOD(ordered_dict):
    init_string = ""
    for k,v in ordered_dict.items():
        init_string += k + ":" + str(v) + " "
    print(init_string)
    return(None)

# PrintOD(attributes)
# sys.exit()

# These are initial conditions, subject to change during game. 
def LevelUpSecondary(attributes):
    secondary = {
        "damroll": round(attributes["str"] / 2.5),
        "speed": round(attributes["dex"] / 2.5),
        "spellpower": round(attributes["int"] / 2.5)
    }
    return(secondary)
# Initialize by first setting according to initial attributes. 
secondary = LevelUpSecondary(attributes)

# print(secondary)
# sys.exit()

# This is invariant throughout entire game. 
levelincrease = {
    "str": 2,
    "dex": 2,
    "int": 2,
    "maxhp": 10,
    "maxsta": 8,
    "maxmn": 8
}

# These are initial conditions, subject to change during game. 
condition = {
    "state": "normal",
    "hp": attributes["maxhp"],
    "sta": attributes["maxsta"],
    "mn": attributes["maxmn"]
}

# Character object should inherit this attribute as Player.condition. 
# Rest() function should restore condition to max. 
def Rest():
    print("You take some time to rest.")
    if CurrentRoom.is_town == True:
        if gold >= 5:
            print("You spend 5 gold to rest in town, and recover fully.")
            gold -= 5
            condition = {
                "state": "normal",
                "hp": attributes["maxhp"],
                "sta": attributes["maxsta"],
                "mn": attributes["maxmn"]
            }
        else:
            # Else you have less than 5 gold. 
            print("You do not have enough gold to rest!")
            return(None)
    else:
        # Else we are not in town. 
        if gold >= 5:
            if random.random() > 0.25:
                print("You spend 5 gold of supplies to rest, and recover partly.")
            else:
                print("Your rest was interrupted by an enemy.")
                EnemyEncounter()
        else:
            print("You do not have enough gold for camping supplies!")
            return(None)


# print(condition)
# sys.exit()

def UpdateStatusBar(condition):
    status_bar = " ".join([
        "<",
        str(condition["hp"]),
        "hp",
        str(condition["sta"]),
        "sta",
        str(condition["mn"]),
        "mn",
        condition["state"],
        "> "
    ])
    return(status_bar)

# Initialize the status bar. 
status_bar = UpdateStatusBar(condition)

# print(status_bar)
# sys.exit()

def LevelUp():
    print("You have gained a level! Choose an attribute to increase.")
    print("[str,dex,int,maxhp,maxsta,maxmn]")
    print("For reference, your current attributes are:")
    print(attributes)
    selected_attribute = input("> ").lower()
    attributes[selected_attribute] += levelincrease[selected_attribute]
    print("Through hard-won experience, you have become more powerful! Your new attributes are:")
    print(attributes)

# LevelUp()
# sys.exit()

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



### SECTION_SKILLS ####
skills = {
    "atk": "normal attack; 1 stamina",
    "def": "defensive attack has increased block chance; 1 stamina",
    "str": "heavy attack has decreased block chance; 1 stamina",
    "shatter": "ignores enemy defence; 3 stamina; scales with str",
    "bash": "has chance to deny enemy attack; 3 stamina; chance scales with str",
    "sunder": "light attack reduces enemy defence; 4 stamina; reduction scales with dex",
    "weaken": "light attack reduces enemy offence; 4 stamina; reduction scales with dex",
    "charge": "attacks with high offence dealing more damage if enemy hp is high; 5 stamina; scales with str",
    "execute": "attacks with high offence dealing more damage if enemy hp low; 6 stamina; scales with dex",
    "flurry": "attacks 2 to 5 times; 8 stamina, number of attacks scales with dex"
}



### SECTION_SPELLS ###
spells = {
    "blast": "magical blast deals basic damage; costs 1 mind",
    "heal": "heals hp; 2 mind; usable out of combat",
    "refresh": "restores stamina; costs 3 mind",
    "barrier": "increases defence; 2 mind; fades after combat",
    "premonition": "increased block; 2 mind; fades after combat",
    "enfeeble": "damages and decreases enemy offence; 3 mind",
    "freeze": "damage with chance to deny enemy attack; 3 mind",
    "vampiric": "damage enemy and heal self; 5 mind",
    "fireball": "deals great damage; costs 6 mind",
    "recall": "sends you to town; 8 mind"
}



### SECTION_COMMANDS ###
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
    def __init__(self,name):
        self.name = name

class Mob(object):
    def __init__(self,name,hp,defence,attack,speed,expgiven):
        self.name = name
        self.hp = hp
        self.defence = defence
        self.attack = attack
        self.speed = speed
        self.expgiven = expgiven

class Character(object):
    def __init__(self):
        Creature.__init__(self)
        self.state = "normal"
        self.attributes = attributes
        self.hp = attributes.get("maxhp")
        self.stamina = attributes.get("maxsta")
        self.mind = attributes.get("maxmind")
        self.room = None
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

class Room(object):
	  def __init__(self,name,desc,exits):
		    self.is_town = False
		    self.name = name
		    self.desc = desc
		    self.exits = exits

class Town(object):
	  def __init__(self,name,desc,exits):
		    self.is_town = True
		    self.name = name
		    self.desc = desc
		    self.exits = exits

exits = {
		"north": "Cold Steppes",
		"south": "Pearl River Delta",
		"east": "Coast of the Yellow Sea",
		"west": "Highland Plateau"
}

