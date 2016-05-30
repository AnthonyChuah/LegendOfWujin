import random
import math
import csv
import sys
from collections import OrderedDict

# Method for printing ordered dictionary.
def PrintOD(ordered_dict):
    for k,v in ordered_dict.items():
        print(k + ": " + str(v))

# Method for printing a character's condition.
def PrintStatus(ordered_dict):
    init_string = ""
    for k,v in ordered_dict.items():
        init_string += k + ":" + str(v) + " "
    print(init_string)
    return(None)

### SECTION_OBJECTS ###
class Character(object):
    def __init__(self,name):
        self.name = name
        self.state = "normal"
        self.attributes = attributes
        self.secondary = secondary
        self.condition = condition
        self.statusbar = status_bar
        self.buffs = buffs
        self.posture = 1
        # self.room is an object of class Town or Room.
        self.room = City
        self.inventory = inventory
        self.equipment = equipment
        self.gold = gold
        self.skills = ["atk","def","str"]
        self.spells = list()
        self.combatmoves = OrderedDict()
        self.combatmoves["flee"] = self.Flee
        self.combatmoves["atk"] = self.Attack
        self.combatmoves["def"] = self.Defend
        self.combatmoves["str"] = self.Strong

    def __str__(self):
        return("Object representing the player character in the game. It has a huge number of methods and properties.")

    def Move(self,direction):
        if (direction in self.room.exits):
            from_room = self.room
            to_room = self.room.exitrooms[direction]
            if (from_room.is_town == False):
                # Possible to be attacked while moving from non-town.
                if (random.random() < 0.2 and self.room.killcount < 20):
                    print("You are ambushed by an enemy!")
                    self.room.EnemyEncounter(self)
            # Character is moving from a town, which is safe from ambush.
            print("You travel " + direction + ".")
            self.room = room_dict[to_room]
            self.room.Look()
            return(None)
        else:
            print("You cannot move in that direction.")
            return(None)

    # Rest() function lets the player restore condition.
    # If in town, rest should restore fully. If not, there is
    # a risk of enemy attack and only half restoration. 
    def Rest(self):
        print("You take some time to rest.")
        if self.room.is_town == True:
            if self.gold >= 5:
                print("You spend 5 gold to rest in town, and recover fully.")
                self.gold -= 5
                self.condition = {
                    "state": "normal",
                    "hp": self.attributes["maxhp"],
                    "sta": self.attributes["maxsta"],
                    "mn": self.attributes["maxmn"]
                }
            else:
                # Else you have less than 5 gold. 
                print("You do not have enough gold to rest!")
                return(None)
        else:
            # Else we are not in town. 
            if self.gold >= 5:
                if random.random() > 0.25:
                    print("You spend 5 gold of supplies to rest, and recover partly.")
                    self.condition["hp"] = min(
                        self.attributes["maxhp"],
                        self.condition["hp"] + (0.5 * self.attributes["maxhp"])
                    )
                    self.condition["sta"] = min(
                        self.attributes["maxsta"],
                        self.condition["sta"] + (0.5 * self.attributes["maxsta"])
                    )
                    self.condition["mn"] = min(
                        self.attributes["maxmn"],
                        self.condition["mn"] + (0.5 * self.attributes["maxmn"])
                    )
                    self.gold -= 5
                else:
                    print("Your rest was interrupted by an enemy.")
                    self.room.EnemyEncounter()
            else:
                print("You do not have enough gold for camping supplies!")
                return(None)

    def Attack(self,Enemy):
        if (self.state != "fighting"):
            print("You cannot use this skill outside of combat.")
        else:
            # Check that you have enough stamina.
            if (self.condition["sta"] < 1):
                print("You attempt to attack, but lack the stamina to follow through.")
                return(None)
            # Set to neutral posture.
            self.posture = 1
            # Determine attack roll.
            weaponroll = random.randint(self.equipbonus["weaponmin"],self.equipbonus["weaponmax"])
            base_attack = weaponroll + self.secondary["damroll"] + self.buffs["damroll"]
            attackroll = weaponroll + base_attack
            # Determine enemy defence roll.
            defroll_min = round(0.25 * Enemy.defence)
            defroll = random.randint(defroll_min,Enemy.defence)
            # Determine damage done.
            damage_done = max(0,attackroll - defroll)
            Enemy.hp -= damage_done
            if (damage_done > 0):
                print("Spotting an opening, you strike at " + Enemy.name + " with a vicious blow.")
                print("You deal " + damage_done + ".")
            else:
                print("You fail to breach " + Enemy.name + "'s defences.")

    def Defend(self,Enemy):
        if (self.state != "fighting"):
            print("You cannot use this skill outside of combat.")
        else:
            # Check that you have enough stamina.
            if (self.condition["sta"] < 1):
                print("You attempt to perform a defensive strike, but lack the stamina to follow through.")
                return(None)
            # Set to defensive posture.
            self.posture = 1.25
            # Determine attack roll.
            weaponroll = random.randint(self.equipbonus["weaponmin"],self.equipbonus["weaponmax"])
            base_attack = weaponroll + self.secondary["damroll"] + self.buffs["damroll"]
            attackroll = round((1 / self.posture) * (weaponroll + base_attack))
            # Determine enemy defence roll.
            defroll_min = round(0.25 * Enemy.defence)
            defroll = random.randint(defroll_min,Enemy.defence)
            # Determine damage done.
            damage_done = max(0,attackroll - defroll)
            Enemy.hp -= damage_done
            if (damage_done > 0):
                print("Circling behind your guard, you attack " + Enemy.name + " with a measured jab.")
                print("You deal " + damage_done + ".")
            else:
                print("You fail to breach " + Enemy.name + "'s defences.")

    def Strong(self,Enemy):
        if (self.state != "fighting"):
            print("You cannot use this skill outside of combat.")
        else:
            if (self.condition["sta"] < 1):
                print("You attempt to deliver a powerful attack, but lack the stamina to follow through.")
                return(None)
            # Set to unguarded posture.
            self.posture = 0
            # Determine attack roll.
            weaponroll = random.randint(self.equipbonus["weaponmin"],self.equipbonus["weaponmax"])
            base_attack = weaponroll + self.secondary["damroll"] + self.buffs["damroll"]
            attackroll = round(1.25 * (weaponroll + base_attack))
            # Determine enemy defence roll.
            defroll_min = round(0.25 * Enemy.defence)
            defroll = random.randint(defroll_min,Enemy.defence)
            # Determine damage done.
            damage_done = max(0,attackroll - defroll)
            Enemy.hp -= damage_done
            if (damage_done > 0):
                print("With reckless abandon, you hack into " + Enemy.name + ".")
                print("You deal " + damage_done + ".")
            else:
                print("You fail to breach " + Enemy.name + "'s defences.")

    def HelpSkills(self):
        print("Syntax: skill [skill name]")
        print("\nThis is the list of all skills:")
        PrintOD(skills)
        print("\nThis is the list of the skills you possess.")
        print(self.skills)

    def HelpSpells():
        print("Syntax: cast [spell name]")
        print("\nThis is the list of all spells:")
        PrintOD(spells)

    def Quit(self):
        print("You give up on your life and commit suicide.")
        self.hp = 0

    def LevelUp(self):
        print("You have gained a level! You may increase one of these:")
        print("[str,dex,int,maxhp,maxsta,maxmn]")
        print("For reference, your current attributes are:")
        PrintStatus(self.attributes)
        attribute_chosen = False
        while (attribute_chosen == False):
            print("Please choose an attribute from the list given!")
            selected_attribute = input("> ").lower()
            if (selected_attribute not in self.attributes):
                continue
            else:
                self.attributes[selected_attribute] += levelincrease[selected_attribute]
                self.attributes["level"] += 1
                self.attributes["exp"] = 0
                self.attributes["tnl"] = self.attributes["level"] * 10
                print(
                    "Through hard-won experience, you have become more powerful!",
                    "Your new attributes are:"
                )
                PrintStatus(self.attributes)
                self.secondary = LevelUpSecondary(self.attributes)
                attribute_chosen = True

    def Combat(self,Enemy):
        # Enemy should be an object of class Mob.
        # This method should be a while loop that breaks only when:
        # (1) Player flees, (2) Enemy dies, or (3) Player dies.
        self.state = "fighting"
        while (Enemy.hp > 0):
            # Show the player status bar, enemy name and enemy injuries.
            # Get player input text and show player available commands:
            # Flee, list of skills, and list of spells.
            # If flee, check for success using self speed vs enemy speed.
            # Note: if enemy is Wujin, you will fail to flee.
            # If flee successful, exit the Combat function and reset self state.
            # If in skill list, use the correct skill function.
            # If in spell list, use the correct spell function.
            # Spell Recall cannot be used in fight against Wujin.
            # Else command was not flee, a skill or a spell. Proceed to enemy turn.
            # Call the Enemy's attack method on the Player.
            # Check if player hp is below 0. If so, call Player.Death method.
        # Once the while loop ends it means the enemy is dead. End combat.
        self.state = "normal"
        self.buffs = buffs
        # Just to be sure, set posture to 1.
        self.posture = 1
        print("You have prevailed over " + Enemy.name + "!")
        if (Enemy.name == "Wujin the renegade blademaster"):
            print("You have rid the lands of this awful menace, and are feted as a hero!")
            print("The Emperor personally thanks you and appoints you as his royal guard.")
            print("You delve into intense study of the martial arts to perfect yourself.")
            print("But soon, you begin to lose your grasp on sanity amidst the treacherous court politics.")
            print("In time, you will become a renegade, and the lands will then call for a hero to destroy you...")
            print("Congratulations on winning the game!")
            sys.exit()
        # Gain loot.
        print("You loot " + Enemy.loot + " gold coins.")
        self.gold += Enemy.loot
        # Gain exp.
        print("You gain " + Enemy.expgiven + " experience points.")
        self.attributes["exp"] += Enemy.expgiven
        # If exp exceeds tnl, level up.
        if (self.attributes["exp"] >= self.attributes["tnl"]):
            self.LevelUp(self)
        return(None)

    def Death(self):
        print("You have fallen in the quest for glory.")
        print("Many will follow in your footsteps, but only one hero will emerge victorious.")
        sys.exit()

    def EquipItem(self,item):
        if (self.state == "fighting"):
            print("You cannot equip items during combat.")
            return(None)
        else:
            if (item not in self.inventory):
                print("You do not have that item.")
                return(None)
            else:
                slot = itemstable[item][whichslot]
                if (self.equipment[slot] != None):
                    self.inventory.append(self.equipment[slot])
                self.equipment[slot] = item
                self.inventory.remove(item)
                UpdateEquipBonus()
                print("You equip the " + item + ". You are now wearing:")
                PrintOD(self.equipment)

    def Challenge(self):
        print("You proclaim your challenge for all the lands to hear.")
        print("Within a few days, Wujin the renegade blademaster arrives to slay you.")
        Wujin = mobdict_objects["Wujin the renegade blademaster"]
        self.Combat(self,Wujin)
        

class Mob(object):
    def __init__(self,name,hp,defence,attack,speed,expgiven,loot):
        self.name = name
        self.hp = hp
        self.maxhp = hp
        self.defence = defence
        self.attack = attack
        self.speed = speed
        self.expgiven = expgiven
        self.loot = loot
        # Moveset is the list of attacks they can use.
        self.moveset = ["Attack"]
        # Moveprob is the probability of using each attack.
        self.moveprob = [1]
        # Debuffs can be applied by player.
        self.debuffs = debuffs
    def Attack(self,Player):
        # Determine block probability if player has shield.
        if (Player.equipment["offhand"] == None):
            pass
        else:
            enemy_penetration = 0.4 * self.attack + 0.6 * self.speed
            blockvalue = round(Player.posture * (Player.secondary["speed"] + Player.equipbonus["block"] + Player.buffs["block"]))
            blockroll_min = round(0.25 * blockvalue)
            blockroll = random.randint(blockroll_min,blockvalue)
            if (enemy_penetration > (2 * blockroll)):
                # Player shield breaks.
                print("With a decisive blow, " + self.name + " cleaves your shield in twain!")
                Player.equipment["offhand"] = None
                UpdateEquipBonus(Player)
            elif (enemy_penetration > blockroll):
                # Player fails to block enemy attack.
                pass
            else:
                # Player manages to block enemy attack.
                print("Adroitly planting your shield between yourself and the enemy, you block " + self.name + "'s attack.")
                # Reset player posture to neutral.
                Player.posture = 1
                return(None)
        # Blocking has failed.
        # Determine enemy attack roll.
        enemy_attackroll = self.attack
        # Determine character defence roll.
        base_defence = Player.secondary["speed"] + Player.equipbonus["deflect"]
        char_defroll_min = round(0.25 * base_defence)
        char_defroll = random.randint(char_defroll_min,base_defence)
        # Determine enemy damage done.
        enemy_damage_done = max(0,enemy_attackroll - char_defroll)
        if (enemy_damage_done > 0):
            print(self.name + " slips past your defences and savagely wounds you.")
            print("You take " + enemy_damage_done + " damage.")
            Player.hp -= enemy_damage_done
            Player.posture = 1
            return(None)
        else:
            print("With poise and discipline, you deflect " + self.name + "'s attack with your armour.")
            Player.posture = 1
            return(None)

    def Blast(self,Player):
        # Unavoidable fixed-damage spell attack.
        enemy_spell_damage = 0.2 * self.attack
        print(self.name + " blasts you with searing flames.")
        print("You take " + enemy_spell_damage + " damage.")
        Player.hp -= enemy_spell_damage
        return(None)

    def Drain(self,Player):
        # Stamina-draining attack.
        pass

    def Heal(self):
        # Mob heals itself.
        heal_amount = self.expgiven * 5
        print(Enemy.name + " heals its wounds with a pillar of silver light.")
        Enemy.hp += heal_amount
        return(None)

class Room(object):
    def __init__(self,name,desc):
        self.is_town = False
        self.name = name
        self.desc = desc
        self.roomnumber = roomlist.index(self.name)
        self.exits = roomexits[self.name]
        self.exitrooms = OrderedDict()
        self.killcount = 0
        # Identify each available exit and corresponding connecting room.
        for index,element in enumerate(self.exits):
            if (element not in cardinal_directions):
                pass
            else:
                self.exitrooms[element] = roomlist[index]
        self.mobs = list()
        self.mobs_prob = list()
    def __str__(self):
        return(self.desc)
    def Look(self):
        print("\n" + self.name + "\n")
        print(self.desc + "\n")
        print("Available exits:" + "\n")
        PrintOD(self.exitrooms)
    def Hunt(self,Player):
        if (Player.condition["sta"] < 3):
            print("You do not have enough stamina to hunt.")
            return(None)
        # This should check with random probability success of finding prey.
        # Unsuccessful hunting means loss of stamina.
        # Check room killcount: if >= 90 you should have 10% chance.
        probability = max(0.1, (1 - (self.killcount/100)))
        if (random.random() < probability):
            self.EnemyEncounter(self,Player)
        else:
            print("Your hunt is fruitless.")
            Player.condition["sta"] -= 3
            return(None)
    def EnemyEncounter(self,Player):
        # This method should call Combat method on the selected Enemy object.
        # Check how many different mobs are in this room.
        variety_mobs = len(self.mobs)
        if (variety_mobs == 0):
            print("There are no monsters here to hunt.")
            return(None)
        else:
            selected_mob_index = random.randint(1,variety_mobs)
            selected_mob = self.mobs[selected_mob_index]
            selected_mob_object = mobdict_objects[selected_mob]
            print("You have encountered " + selected_mob + "!")
            Player.Combat(selected_mob_object)

class Town(object):
    def __init__(self,name,desc):
        Room.__init__(self,name,desc)
        self.is_town = True
    def __str__(self):
        return(self.desc)
    def Look(self):
        Room.Look(self)
    def Hunt(self,Player):
        Room.Hunt(self,Player)
    def EnemyEncounter(self,Player):
        Room.EnemyEncounter(self,Player)
    def Shop(self,Player):
        print("You browse the list of available items:\n")
        print(itemstable.keys())
        print("\nRefer to items.jpg for detailed information.")
        print("What do you wish to buy? Type the item name, or type 'exit' to exit.")
        print("If you wish to sell, type 'sell'.")
        shopping_choice = input("> ")
        if (shopping_choice.lower() == "exit"):
            print("You leave the shop.")
            return(None)
        if (shopping_choice.lower() == "sell"):
            print("Which item in your inventory would you sell?")
            print(Player.inventory)
            sale_item = input("> ")
            if (sale_item not in Player.inventory):
                print("You do not have that.")
                print("You leave the shop.")
                return(None)
            else:
                sale_value = itemstable[sale_item][whichcost] * 0.2
                Player.inventory.remove(sale_item)
                print("You sell the " + sale_item + " for " + sale_value + " coins.")
                Player.gold += sale_value
                print("You leave the shop.")
                return(None)
        if (shopping_choice not in itemstable.keys()):
            print("That item is not in the list of available items.")
            print("You leave the shop.")
            return(None)
        else:
            shopping_cost = itemstable[shopping_choice][whichcost]
            if (shopping_cost > Player.gold):
                print("You have insufficient coin.")
                print("You leave the shop.")
                return(None)
            else:
                # Decrement Player's gold and append item to inventory.
                Player.gold -= shopping_cost
                Player.inventory.append(shopping_choice)
                print("You purchase the " + shopping_choice + ".")
                print("You leave the shop.")
    def Train(self,Player):
        print("You visit Lijun's Academy for training.")
        print("Zhang-Fei the mighty giant stands ready to train you in the martial arts.")
        print("Zhuge-Liang the crafty mystic stands ready to instruct you in high sorcery.")
        print("Do you wish to learn a skill or a spell? [skill, spell]")
        train_choice = input("> ").lower()
        if (train_choice not in ["skill","spell"]):
            print("You must choose a skill or a spell. Come back again.")
            return(None)
        elif (train_choice == "skill"):
            print("You may learn the following skills. Choose one.")
            print(skills.keys())
            print("Note: if you learn a skill you already know you will not be refunded!")
            

            
        



### SECTION_MAP ###
cardinal_directions = ["north","south","east","west"]
roomexits = dict()
with open("map.csv","r") as mapfile:
    for rownum,line in enumerate(mapfile):
        line = line.strip("\n")
        if (rownum == 0):
            roomlist = line.split(",")
            roomlist.remove("")
        else:
            linelist = line.split(",")
            roomname = linelist[0]
            linelist.remove(roomname)
            roomexits[roomname] = linelist

# print(roomexits)
# print(roomlist)
# sys.exit()
City = Town(
    "Xian City",
    "You are in Xian City. You may train and shop here."
    )
City.mobs.append("a giant rat")

Steppes = Room(
    "Cold Steppes",
    "You are in the cold steppes. You may hunt here."
    )
Steppes.mobs.append("a tundra leopard")
Steppes.mobs.append("a savage horseman")

Delta = Room(
    "Pearl River Delta",
    "You are in the Pearl River Delta. You may hunt here."
    )
Delta.mobs.append("a mottled goblin")
Delta.mobs.append("a giant rat")

Coast = Room(
    "Coast of the Yellow Sea",
    "You are at the coast of the Yellow Sea. You may hunt here."
    )
Coast.mobs.append("a mangy brigand")
Coast.mobs.append("a feral hyena")

Plateau = Room(
    "Highland Plateau",
    "You are at the highland plateau. You may hunt here."
    )
Plateau.mobs.append("the highland ravager")
Plateau.mobs.append("an elite mountain ranger")

room_dict = {
    "Xian City": City,
    "Cold Steppes": Steppes,
    "Pearl River Delta": Delta,
    "Coast of the Yellow Sea": Coast,
    "Highland Plateau": Plateau
    }

# print(room_dict)
# City.Look()
# Steppes.Look()
# Delta.Look()
# Coast.Look()
# Plateau.Look()


### SECTION_MOBS ###
mobdict_objects = dict()
# MobDict is a dictionary of dictionaries: key will be mob names,
# values will be dictionaries for lookup of mob attributes.
mobdict = dict()
with open("mobs.csv","r") as mobsfile:
    for rownum,line in enumerate(mobsfile):
        line = line.strip("\n")
        if (rownum == 0):
            mobs_header = line.split(",")
        else:
            linelist = line.split(",")
            mobname = linelist[0]
            mobdict[mobname] = linelist

whichmobhp = mobs_header.index("hp")
whichmobdef = mobs_header.index("defence")
whichmobatk = mobs_header.index("attack")
whichmobspeed = mobs_header.index("speed")
whichmobexp = mobs_header.index("expgiven")
whichmobloot = mobs_header.index("loot")
whichmobmoveset = mobs_header.index("moveset")
whichmobmoveprob = mobs_header.index("moveprob")

for k,v in mobdict.items():
    mobdict_objects[k] = Mob(v[0],v[1],v[2],v[3],v[4],v[5],v[6])

# print(mobdict)
# print(mobs_header)
# print(moblist_objects)
# sys.exit()


### SECTION_ATTRIBUTES ###
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

# These are initial secondary attributes, subject to change during game. 
def LevelUpSecondary(attributes):
    secondary = {
        "damroll": round(attributes["str"] / 2.5),
        "speed": round(attributes["dex"] / 2.5),
        "spellpower": round(attributes["int"] / 2.5)
    }
    return(secondary)
# Initialize by first setting according to initial attributes. 
secondary = LevelUpSecondary(attributes)

# Base magic buffs, these re-set to 0 after each combat.
# Some spells can grant buffs for the next combat.
buffs = {
    "damroll": 0,
    "speed": 0,
    "deflect": 0,
    "block": 0,
    "spellpower": 0
}
# Debuffs on mobs. These initialize at 0.
debuffs = {
    "attack": 0,
    "defence": 0,
    "speed": 0
}

# print(secondary)
# sys.exit()

# This is invariant throughout entire game. 
levelincrease = {
    "str": 2,
    "dex": 2,
    "int": 2,
    "maxhp": 10,
    "maxsta": 8,
    "maxmn": 8,
    "level": 1
}

# These are initial conditions, subject to change during game. 
condition = {
    "state": "normal",
    "hp": attributes["maxhp"],
    "sta": attributes["maxsta"],
    "mn": attributes["maxmn"]
}

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

# LevelUp()
# sys.exit()



### SECTION_ITEMS ###

# Read the items.csv file and make the items data.
itemstable_header = list()
itemstable = OrderedDict()

with open("items.csv","r") as itemsfile:
    for rownum,line in enumerate(itemsfile):
        line = line.strip("\n")
        if (rownum == 0):
            itemstable_header = line.split(",")
        else:
            linelist = line.split(",")
            itemname = linelist[0]
            itemstable[itemname] = linelist

whichname = itemstable_header.index("item_name")
whichtype = itemstable_header.index("type")
whichslot = itemstable_header.index("slot")
whichmindam = itemstable_header.index("min_dam")
whichmaxdam = itemstable_header.index("max_dam")
whichdeflect = itemstable_header.index("deflect")
whichblock = itemstable_header.index("block")
whichcost = itemstable_header.index("cost")

# There are 6 equipment slots.
equipment = OrderedDict()
equipment["mainhand"] = "knife"
equipment["offhand"] = None
equipment["body"] = "cloth tunic"
equipment["legs"] = "cloth trousers"
equipment["feet"] = "sandals"
equipment["hands"] = None

# Calculate the bonuses from equipment.
def UpdateEquipBonus(Character):
    Character.equipbonus = dict()
    weapon = Character.equipment["mainhand"]
    shield = Character.equipment["offhand"]

    if (Character.equipment["body"] == None):
        body_deflect = 0
    else:
        body_deflect = itemstable[Character.equipment["body"]][whichdeflect]

    if (Character.equipment["legs"] == None):
        legs_deflect = 0
    else:
        legs_deflect = itemstable[Character.equipment["legs"]][whichdeflect]

    if (Character.equipment["feet"] == None):
        feet_deflect = 0
    else:
        feet_deflect = itemstable[Character.equipment["feet"]][whichdeflect]

    if (Character.equipment["hands"] == None):
        hands_deflect = 0
    else:
        hands_deflect = itemstable[Character.equipment["hands"]][whichdeflect]

    if (weapon == None):
        Character.equipbonus["weaponmax"] = 0
        Character.equipbonus["weaponmin"] = 0
    else:
        Character.equipbonus["weaponmax"] = itemstable[weapon][whichmaxdam]
        Character.equipbonus["weaponmin"] = itemstable[weapon][whichmindam]

    if (shield == None):
        Character.equipbonus["block"] = 0
    else:
        Character.equipbonus["block"] = itemstable[shield][whichblock]

    Character.equipbonus["deflect"] = int(body_deflect) + int(legs_deflect) + int(feet_deflect) + int(hands_deflect)


# Inventory space is unlimited.
inventory = ["cloth gloves","wooden buckler"]
gold = 50

# Update the equipment bonus
# UpdateEquipBonus(Player)
# print(Player.equipbonus)
# sys.exit()

# print(equipbonus)
# print(inventory)
# sys.exit()

### SECTION_SKILLS ###
skills = OrderedDict()
skills["atk"] = "normal attack; 1 stamina"
skills["def"] = "defensive attack has increased block chance; 1 stamina"
skills["str"] = "heavy attack has zero block chance; 1 stamina"
skills["shatter"] = "ignores enemy defence; 3 stamina; scales with str"
skills["bash"] = "has chance to deny enemy attack; 3 stamina; chance scales with str"
skills["sunder"] = "light attack reduces enemy defence; 3 stamina; reduction scales with dex"
skills["weaken"] = "light attack reduces enemy offence; 3 stamina; reduction scales with dex"
skills["charge"] = "heavy attack more effective if enemy hp high; 4 stamina; scales with str"
skills["execute"] = "heavy attack more effective if enemy hp low; 6 stamina; scales with dex"
skills["flurry"] = "attacks 2 to 5 times; 8 stamina; number scales with dex"

# skills_req shows the Dex requirement and the gold cost of learning the skill. 
skills_req = OrderedDict()
skills_req["atk"] = [0, 10]
skills_req["def"] = [0, 10]
skills_req["str"] = [0, 10]
skills_req["shatter"] = [12, 24]
skills_req["bash"] = [14, 28]
skills_req["sunder"] = [16, 42]
skills_req["weaken"] = [18, 45]
skills_req["charge"] = [20, 50]
skills_req["execute"] = [24, 48]
skills_req["flurry"] = [26, 52]

# PrintOD(skills)
# sys.exit()

# Player = Character("Wujin")
# Player.skill_list = ["atk","def","str"]



# Player = Character("Wujin")
# HelpSkills()
# sys.exit()


### SECTION_SPELLS ###
allspells = {
    "blast": "magical blast deals basic damage; costs 1 mind",
    "heal": "heals hp; 2 mind; usable out of combat",
    "refresh": "restores stamina; costs 3 mind",
    "barrier": "increases defence; 3 mind; fades after combat",
    "premonition": "increased block; 3 mind; fades after combat",
    "enfeeble": "damages and decreases enemy offence; 3 mind",
    "freeze": "damage with chance to deny enemy attack; 3 mind",
    "vampiric": "damage enemy and heal self; 5 mind",
    "fireball": "deals great damage; costs 6 mind",
    "recall": "sends you to town; 8 mind"
}
# spells_req shows the Int requirement and gold cost of learning a spell. 
spells_req = OrderedDict()
spells_req["blast"] = [10, 20]
spells_req["heal"] = [14, 42]
spells_req["refresh"] = [16, 48]
spells_req["barrier"] = [14, 42]
spells_req["premonition"] = [12, 24]
spells_req["enfeeble"] = [12, 24]
spells_req["freeze"] = [14, 28]
spells_req["vampiric"] = [18, 36]
spells_req["fireball"] = [24, 48]
spells_req["recall"] = [26, 52]

### SECTION_COMMANDS ###
commands = {
    "north":"go north",
    "south":"go south",
    "east":"go east",
    "west":"go west",
    "quit":"quit the game",
    "shop":"buy or sell items",
    "learn":"learn spells; only in town",
    "train":"train in skills; only in town",
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

### SECTION_GAME ###

Player = Character("Wujin")
print(Player)
