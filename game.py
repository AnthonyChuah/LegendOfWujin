import random
import math
import csv
import sys
from collections import OrderedDict

# Method for printing ordered dictionary.
def PrintOD(ordered_dict):
    for k,v in ordered_dict.items():
        print(k + ": " + str(v))

# Method for printing a character's attributes.
def PrintStatus(ordered_dict):
    init_string = ""
    for k,v in ordered_dict.items():
        init_string += k + ":" + str(v) + " "
    print(init_string)
    return(None)

def UpdateStatusBar(condition_dict):
    statusbar = " ".join([
        "<",
        str(condition_dict["hp"]),
        "hp",
        str(condition_dict["sta"]),
        "sta",
        str(condition_dict["mn"]),
        "mn",
        condition_dict["state"],
        "> "
    ])
    return(statusbar)

### SECTION_OBJECTS ###
class Character(object):
    def __init__(self,name):
        # Never actually used, but let's keep it.
        self.name = name
        # Attributes is ordered dict with str, dex, int, maxhp, maxsta, maxmn, etc.
        self.attributes = attributes.copy()
        # Secondary is dictionary with damroll, speed, spellpower.
        self.secondary = secondary.copy()
        # Condition is dictionary with state, hp, sta, mn.
        self.condition = condition.copy()
        self.statusbar = status_bar
        self.buffs = buffs.copy()
        self.posture = 1
        # self.room is an object of class Town or Room.
        # Do not make a copy because the object should remember its killcount.
        self.room = City
        self.inventory = inventory.copy()
        self.equipment = equipment.copy()
        self.equipbonus = dict()
        self.UpdateEquipBonus()
        self.gold = gold
        self.skills = ["atk","def","str"]
        self.spells = list()
        self.skilldict = OrderedDict()
        self.skilldict["atk"] = self.Attack
        self.skilldict["def"] = self.Defend
        self.skilldict["str"] = self.Strong
        self.skilldict["shatter"] = self.Shatter
        self.skilldict["bash"] = self.Bash
        self.skilldict["sunder"] = self.Sunder
        self.skilldict["weaken"] = self.Weaken
        self.skilldict["charge"] = self.Charge
        self.skilldict["execute"] = self.Execute
        self.skilldict["flurry"] = self.Flurry
        self.spelldict = OrderedDict()
        self.spelldict["blast"] = self.Blast
        self.spelldict["heal"] = self.Heal
        self.spelldict["refresh"] = self.Refresh
        self.spelldict["barrier"] = self.Barrier
        self.spelldict["premonition"] = self.Premonition
        self.spelldict["enfeeble"] = self.Enfeeble
        self.spelldict["freeze"] = self.Freeze
        self.spelldict["vampiric"] = self.Vampiric
        self.spelldict["fireball"] = self.Fireball
        self.spelldict["recall"] = self.Recall

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
                    self.EnemyEncounter()
            # Character is moving from a town, which is safe from ambush.
            print("You travel " + direction + ".")
            self.room = room_dict[to_room]
            self.Look()
            return(None)
        else:
            print("You cannot move in that direction.")
            return(None)

    def Look(self):
        print("\n" + self.room.name + "\n")
        print(self.room.desc + "\n")
        print("Available exits:" + "\n")
        PrintOD(self.room.exitrooms)
        self.statusbar = UpdateStatusBar(self.condition)
        print(self.statusbar)

    def Score(self):
        print("Your attributes are:")
        PrintOD(self.attributes)
        self.statusbar = UpdateStatusBar(self.condition)
        print("Your current condition is:")
        print(self.statusbar)
        print("You know the following skills:")
        print(self.skills)
        print("You know the following spells:")
        print(self.spells)

    def Hunt(self):
        if (self.condition["sta"] < 3):
            print("You do not have enough stamina to hunt.")
            return(None)
        # This should check with random probability success of finding prey.
        # Unsuccessful hunting means loss of stamina.
        # Check room killcount: if >= 90 you should have 10% chance.
        probability = max(0.1, (1 - (self.room.killcount/100)))
        if (random.random() < probability):
            self.EnemyEncounter()
        else:
            print("Your hunt is fruitless.")
            self.condition["sta"] -= 3
            return(None)

    def EnemyEncounter(self):
        # This method should call Combat method on the selected Enemy object.
        # Check how many different mobs are in this room.
        variety_mobs = len(self.room.mobs)
        if (variety_mobs == 0):
            print("There are no monsters here to hunt.")
            return(None)
        else:
            selected_mob_index = random.randint(1,variety_mobs)
            selected_mob = self.room.mobs[selected_mob_index - 1]
            selected_mob_object = mobdict_objects[selected_mob]
            print("You have encountered " + selected_mob + "!")
            self.Combat(selected_mob_object)

    def Shop(self):
        if (self.room.is_town == False):
            print("You can only shop in town.")
            return(None)
        print("You browse the list of available items:\n")
        print(itemstable.keys())
        print("\nRefer to items.csv for detailed information.")
        print("What do you wish to buy? Type the item name, or type 'exit' to exit.")
        print("If you wish to sell, type 'sell'.")
        shopping_choice = input("> ")
        if (shopping_choice.lower() == "exit"):
            print("You leave the shop.")
            return(None)
        if (shopping_choice.lower() == "sell"):
            print("Which item in your inventory would you sell?")
            print(self.inventory)
            sale_item = input("> ")
            if (sale_item not in self.inventory):
                print("You do not have that.")
                print("You leave the shop.")
                return(None)
            else:
                sale_value = round(int(itemstable[sale_item][whichcost]) * 0.2)
                self.inventory.remove(sale_item)
                print("You sell the " + sale_item + " for " + str(sale_value) + " coins.")
                self.gold += sale_value
                print("You leave the shop.")
                return(None)
        if (shopping_choice not in itemstable.keys()):
            print("That item is not in the list of available items.")
            print("You leave the shop.")
            return(None)
        else:
            shopping_cost = int(itemstable[shopping_choice][whichcost])
            if (shopping_cost > self.gold):
                print("You have insufficient coin.")
                print("You leave the shop.")
                return(None)
            else:
                # Decrement Player's gold and append item to inventory.
                self.gold -= shopping_cost
                self.inventory.append(shopping_choice)
                print("You purchase the " + shopping_choice + ".")
                print("You leave the shop.")

    def Train(self):
        if (self.room.is_town == False):
            print("You can only train in town.")
            return(None)
        print("You visit Lijun's Academy for training.")
        print("Zhang-Fei the mighty giant stands ready to train you in the martial arts.")
        print("Zhuge-Liang the brilliant recluse stands ready to instruct you in high sorcery.")
        print("Do you wish to learn a skill or a spell? [skill, spell]")
        train_choice = input("> ").lower()
        if (train_choice not in ["skill","spell"]):
            print("You must choose a skill or a spell. Come back again.")
            return(None)
        elif (train_choice == "skill"):
            print("You may learn the following skills. Choose one.")
            print(skills_req.keys())
            print("Note: if you learn a skill you already know you will not be refunded!")
            train_skillchoice = input("> ").lower()
            if (train_skillchoice not in skills_req.keys()):
                print("No such skill.")
                return(None)
            else:
                train_cost = skills_req[train_skillchoice][1]
                train_skillreq = skills_req[train_skillchoice][0]
            if (self.attributes["dex"] < train_skillreq):
                # Check if you have the dex required to learn this skill.
                print("You need " + str(train_skillreq) + " dexterity to train in this skill. Come back again.")
                return(None)
            elif (self.gold < train_cost):
                # Check if you have the funds required to learn this skill.
                print("You need " + str(train_cost) + " gold to train in this skill. Come back again.")
                return(None)
            else:
                self.skills.append(train_skillchoice)
                self.gold -= train_cost
                print("You spend " + str(train_cost) + " gold.")
                print("You learn the skill: " + train_skillchoice + ".")
                return(None)
        else:
            # The train_choice was spell.
            print("You may learn the following spells. Choose one.")
            print(spells_req.keys())
            print("Note: if you learn a spell you already know you will not be refunded!")
            train_spellchoice = input("> ").lower()
            if (train_spellchoice not in spells_req.keys()):
                print("No such spell.")
                return(None)
            else:
                train_cost = spells_req[train_spellchoice][1]
                train_spellreq = spells_req[train_spellchoice][0]
            if (self.attributes["int"] < train_spellreq):
                print("You need " + str(train_spellreq) + " intelligence to train in this skill. Come back again.")
                return(None)
            elif (self.gold < train_cost):
                print("You need " + (train_cost) + " gold to train in this skill. Come back again.")
                return(None)
            else:
                self.spells.append(train_spellchoice)
                self.gold -= train_cost
                print("You spend " + str(train_cost) + " gold.")
                print("You learn the skill: " + train_spellchoice + ".")
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
                if (random.random() > 0.25 and self.room.killcount < 40):
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
        if (self.condition["state"] != "fighting"):
            print("You cannot use this skill outside of combat.")
        else:
            # Check that you have enough stamina.
            if (self.condition["sta"] < 1):
                print("You attempt to attack, but lack the stamina to follow through.")
                return(None)
            # Set to neutral posture. Use stamina.
            self.posture = 1
            self.condition["sta"] -= 1
            # Determine attack roll.
            weaponroll = random.randint(self.equipbonus["weaponmin"],self.equipbonus["weaponmax"])
            base_attack = 4 + self.secondary["damroll"] + self.buffs["damroll"]
            attackroll = weaponroll + base_attack
            # Determine enemy defence roll.
            base_defence = max(0, Enemy.defence - Enemy.debuffs["defence"])
            defroll_min = round(0.25 * base_defence)
            defroll = random.randint(defroll_min, base_defence)
            # Determine damage done.
            damage_done = max(0,attackroll - defroll)
            Enemy.hp -= damage_done
            if (damage_done > 0):
                print("Spotting an opening, you strike at " + Enemy.name + " with a vicious blow.")
                print("You deal " + str(damage_done) + " damage.")
            else:
                print("You fail to breach " + Enemy.name + "'s defences.")

    def Defend(self,Enemy):
        if (self.condition["state"] != "fighting"):
            print("You cannot use this skill outside of combat.")
        else:
            # Check that you have enough stamina.
            if (self.condition["sta"] < 1):
                print("You attempt to perform a defensive strike, but lack the stamina to follow through.")
                return(None)
            # Set to defensive posture. Use stamina.
            self.posture = 1.25
            self.condition["sta"] -= 1
            # Determine attack roll.
            weaponroll = random.randint(self.equipbonus["weaponmin"],self.equipbonus["weaponmax"])
            base_attack = 3 + self.secondary["damroll"] + self.buffs["damroll"]
            attackroll = round((1 / self.posture) * (weaponroll + base_attack))
            # Determine enemy defence roll.
            base_defence = max(0, Enemy.defence - Enemy.debuffs["defence"])
            defroll_min = round(0.25 * base_defence)
            defroll = random.randint(defroll_min, base_defence)
            # Determine damage done.
            damage_done = max(0,attackroll - defroll)
            Enemy.hp -= damage_done
            if (damage_done > 0):
                print("Circling behind your guard, you attack " + Enemy.name + " with a measured jab.")
                print("You deal " + str(damage_done) + " damage.")
            else:
                print("You fail to breach " + Enemy.name + "'s defences.")

    def Strong(self,Enemy):
        if (self.condition["state"] != "fighting"):
            print("You cannot use this skill outside of combat.")
        else:
            if (self.condition["sta"] < 1):
                print("You attempt to deliver a powerful attack, but lack the stamina to follow through.")
                return(None)
            # Set to unguarded posture. Use stamina.
            self.posture = 0
            self.condition["sta"] -= 1
            # Determine attack roll.
            weaponroll = random.randint(self.equipbonus["weaponmin"],self.equipbonus["weaponmax"])
            base_attack = 5 + self.secondary["damroll"] + self.buffs["damroll"]
            attackroll = round(1.25 * (weaponroll + base_attack))
            # Determine enemy defence roll.
            base_defence = max(0, Enemy.defence - Enemy.debuffs["defence"])
            defroll_min = round(0.25 * base_defence)
            defroll = random.randint(defroll_min, base_defence)
            # Determine damage done.
            damage_done = max(0,attackroll - defroll)
            Enemy.hp -= damage_done
            if (damage_done > 0):
                print("With reckless abandon, you hack into " + Enemy.name + ".")
                print("You deal " + str(damage_done) + " damage.")
            else:
                print("You fail to breach " + Enemy.name + "'s defences.")

    def Shatter(self,Enemy):
        if (self.condition["sta"] < 3):
            print("You attempt to make a shattering blow, but lack the stamina to follow through.")
            return(None)
        else:
            # Use stamina.
            self.condition["sta"] -= 3
            # Determine attack roll.
            weaponroll = random.randint(self.equipbonus["weaponmin"],self.equipbonus["weaponmax"])
            base_attack = weaponroll + self.secondary["damroll"] + self.buffs["damroll"]
            attackroll = weaponroll + base_attack
            print("With inexorable force, you shatter your opponent's defences and strike true.")
            print("You deal " + str(attackroll) + " damage.")
            Enemy.hp -= attackroll
            return(None)

    def Bash(self,Enemy):
        if (self.condition["sta"] < 3):
            print("You attempt to bash your enemy with overbearing momentum, but lack the stamina to follow through.")
            return(None)
        else:
            self.condition["sta"] -= 3
            weaponroll = random.randint(self.equipbonus["weaponmin"],self.equipbonus["weaponmax"])
            base_attack = 4 + self.secondary["damroll"] + self.buffs["damroll"]
            attackroll = weaponroll + base_attack
            base_defence = max(0, Enemy.defence - Enemy.debuffs["defence"])
            defroll_min = round(0.25 * base_defence)
            defroll = random.randint(defroll_min, base_defence)
            damage_done = max(0, attackroll - defroll)
            bash_power = (self.secondary["damroll"] + self.buffs["damroll"]) * 2
            bash_diff = bash_power - (Enemy.attack - Enemy.debuffs["attack"])
            bash_baseprob = (1 / (1 + math.pow(math.exp(1), -bash_diff)))
            bash_prob = min(0.8, bash_baseprob)
            if (random.random() < bash_prob):
                # Then bash skill stuns the enemy successfully.
                print("Like a boar charging down the mountain, you slam your victim to the ground with sheer momentum!")
                print("You deal " + str(damage_done) + " damage.")
                Enemy.hp -= damage_done
                Enemy.stun = True
                return(None)
            else:
                print("You charge wildly at your foe, and connect with a solid blow.")
                print("You deal " + str(damage_done) + " damage.")
                Enemy.hp -= damage_done
                return(None)

    def Sunder(self,Enemy):
        if (self.condition["sta"] < 3):
            print("You attempt to sunder your opponent's armour, but lack the stamina to follow through.")
            return(None)
        else:
            self.condition["sta"] -= 3
            weaponroll = random.randint(self.equipbonus["weaponmin"],self.equipbonus["weaponmax"])
            base_attack = 4 + self.secondary["damroll"] + self.buffs["damroll"]
            attackroll = weaponroll + base_attack
            sunder_power = round(self.secondary["speed"] / 2 + 2)
            base_defence = max(0, Enemy.defence - Enemy.debuffs["defence"])
            defroll_min = round(0.25 * base_defence)
            defroll = random.randint(defroll_min, base_defence)
            damage_done = max(0, attackroll - defroll)
            Enemy.debuffs["defence"] = sunder_power
            print("You spot a clever opportunity to tear down your foe's defences.")
            print("You deal " + str(damage_done) + " damage.")
            Enemy.hp -= damage_done
            return(None)

    def Weaken(self,Enemy):
        if (self.condition["sta"] < 3):
            print("You attempt to weaken your opponent, but lack the stamina to follow through.")
            return(None)
        else:
            self.condition["sta"] -= 3
            weaponroll = random.randint(self.equipbonus["weaponmin"],self.equipbonus["weaponmax"])
            base_attack = 4 + self.secondary["damroll"] + self.buffs["damroll"]
            attackroll = weaponroll + base_attack
            weaken_power = round(self.secondary["speed"] / 2 + 2)
            base_defence = max(0, Enemy.defence - Enemy.debuffs["defence"])
            defroll_min = round(0.25 * base_defence)
            defroll = random.randint(defroll_min, base_defence)
            damage_done = max(0, attackroll - defroll)
            Enemy.debuffs["attack"] = weaken_power
            print("You land a crippling blow, weakening your opponent.")
            print("You deal " + str(damage_done) + " damage.")
            Enemy.hp -= damage_done
            return(None)

    def Charge(self,Enemy):
        if (self.condition["sta"] < 4):
            print("You attempt to surprise your unwary foe with a charging attack, but lack the stamina to follow through.")
            return(None)
        else:
            self.condition["sta"] -= 4
            enemy_fractionhp = Enemy.hp / Enemy.maxhp
            damage_multiplier = 1 + enemy_fractionhp
            weaponroll = random.randint(self.equipbonus["weaponmin"],self.equipbonus["weaponmax"])
            base_attack = 4 + self.secondary["damroll"] + self.buffs["damroll"]
            attackroll = (weaponroll + base_attack) * damage_multiplier
            base_defence = max(0, Enemy.defence - Enemy.debuffs["defence"])
            defroll_min = round(0.25 * base_defence)
            defroll = random.randint(defroll_min, base_defence)
            damage_done = round(max(0, attackroll - defroll))
            Enemy.hp -= damage_done
            print("Taking your opponent by surprise, you devastate it with a mighty charging attack!")
            print("You deal " + str(damage_done) + " damage.")
            return(None)

    def Execute(self,Enemy):
        if (self.condition["sta"] < 6):
            print("You attempt to deliver the coup de grace, but lack the stamina to follow through.")
            return(None)
        else:
            self.condition["sta"] -= 6
            enemy_fractionhp = Enemy.hp / Enemy.maxhp
            damage_multiplier = 1 + (1 - enemy_fractionhp)
            weaponroll = random.randint(self.equipbonus["weaponmin"],self.equipbonus["weaponmax"])
            base_attack = 4 + self.secondary["damroll"] + self.buffs["damroll"] + self.secondary["speed"]
            attackroll = (weaponroll + base_attack) * damage_multiplier
            base_defence = max(0, Enemy.defence - Enemy.debuffs["defence"])
            defroll_min = round(0.25 * base_defence)
            defroll = random.randint(defroll_min, base_defence)
            damage_done = round(max(0, attackroll - defroll))
            Enemy.hp -= damage_done
            print("Weaving through the forms of the legendary Grandmasters of Wu-Dang Temple, you strike a finishing blow to your opponent's vitals!")
            print("You deal " + str(damage_done) + " damage.")
            return(None)

    def Flurry(self,Enemy):
        if (self.condition["sta"] < 8):
            print("You attempt to start a flurry of attacks, but lack the stamina to follow through.")
            return(None)
        else:
            self.condition["sta"] -= 8
            flurries = min(5, round(self.secondary["speed"] / 4) + 1)
            print("You begin a flurry of " + str(flurries) + " consecutive strikes.")
            for _ in range(flurries):
                weaponroll = random.randint(self.equipbonus["weaponmin"],self.equipbonus["weaponmax"])
                base_attack = 4 + self.secondary["damroll"] + self.buffs["damroll"]
                attackroll = weaponroll + base_attack
                base_defence = max(0, Enemy.defence - Enemy.debuffs["defence"])
                defroll_min = round(0.25 * base_defence)
                defroll = random.randint(defroll_min, base_defence)
                damage_done = round(max(0,attackroll - defroll))
                Enemy.hp -= damage_done
                print("Your swift attack deals " + str(damage_done) + " damage.")
            return(None)

    def Heal(self,Enemy=None):
        # Determine amount healed according to spellpower.
        if (self.condition["mn"] < 2):
            print("You do not have enough mind power to heal yourself.")
            return(None)
        else:
            amount_healed = self.secondary["spellpower"] * 2 - 3
            print("Summoning a pillar of silver light, you seal your wounds and recover " + str(amount_healed) + " hp!")
            self.condition["mn"] -= 2

            self.condition["hp"] = min(self.condition["hp"] + amount_healed, self.attributes["maxhp"])
            return(None)

    def Refresh(self,Enemy=None):
        if (self.condition["mn"] < 3):
            print("You do not have enough mental power to restore stamina.")
            return(None)
        else:
            amount_refreshed = self.secondary["spellpower"] * 2 - 4
            print("Drawing upon ambient energy, you reinvigorate yourself and restore " + str(amount_refreshed) + " stamina!")
            self.condition["mn"] -= 3
            self.condition["sta"] = min(self.condition["sta"] + amount_refreshed, self.attributes["maxsta"])
            return(None)

    def Recall(self,Enemy=None):
        if (self.condition["mn"] < 8):
            print("You do not have enough mental power to recall.")
            return(None)
        else:
            print("You utter a word of recall and vanish in a flash of blinding white light! As you re-orient yourself, you find yourself in town.")
            self.condition["mn"] -= 8
            self.room = City
            return(None)

    def Premonition(self,Enemy=None):
        if (self.condition["mn"] < 3):
            print("You do not have enough mental power to grant yourself premonitions.")
            return(None)
        else:
            bonus_block = self.secondary["spellpower"]
            print("Gaining a vision of the immediate future, you enhance your shield blocking skill.")
            self.buffs["block"] = bonus_block
            self.condition["mn"] -= 3
            return(None)

    def Barrier(self,Enemy=None):
        if (self.condition["mn"] < 3):
            print("You do not have enough mental power to weave a barrier around yourself.")
            return(None)
        else:
            bonus_deflect = self.secondary["spellpower"]
            print("You weave a shimmering barrier around yourself to harden yourself against enemy attack.")
            self.condition["mn"] -= 3
            self.buffs["deflect"] = bonus_deflect
            return(None)

    def Enfeeble(self,Enemy):
        if (self.condition["mn"] < 3):
            print("You do not have enough mental power to enfeeble your foe.")
            return(None)
        else:
            enfeeblement = self.secondary["spellpower"]
            Enemy.debuffs["attack"] = enfeeblement
            print("With a wave of your hand, you visit the chill of the grave upon " + Enemy.name + ", making it weak and feeble.")
            self.condition["mn"] -= 3
            return(None)

    def Freeze(self,Enemy):
        if (self.condition["mn"] < 3):
            print("You do not have enough mental power to freeze your foe.")
            return(None)
        else:
            spellpower_coef = (self.secondary["spellpower"] + self.buffs["spellpower"]) * 2
            penetration_coef = spellpower_coef - (Enemy.attack - Enemy.debuffs["attack"])
            prob_threshold = (1 / (1 + math.pow(math.exp(1), -penetration_coef)))
            freeze_prob = min(0.8, prob_threshold)
            freeze_damage = self.secondary["spellpower"] * 2 - 4
            if (random.random() < freeze_prob):
                # Then freeze spell stuns the enemy successfully.
                print("Conjuring the blistering cold of the Arctic floes, you freeze your foe into helplessness!")
                print("You deal " + str(freeze_damage) + " damage.")
                Enemy.stun = True
                Enemy.hp -= freeze_damage
                self.condition["mn"] -= 3
                return(None)
            else:
                print("You blast your foe with the biting cold of the Siberian tundra.")
                print("You deal " + str(freeze_damage) + " damage.")
                Enemy.hp -= freeze_damage
                self.condition["mn"] -= 3
                return(None)

    def Blast(self,Enemy):
        if (self.condition["mn"] < 1):
            print("You do not have enough mental power to blast your foe.")
            return(None)
        else:
            blast_damage = self.secondary["spellpower"] + 3
            print("You raise a clenched fist, and blast your victim with searing flames!")
            print("You deal " + str(blast_damage) + " damage.")
            Enemy.hp -= blast_damage
            self.condition["mn"] -= 3
            return(None)

    def Vampiric(self,Enemy):
        if (self.condition["mn"] < 5):
            print("You do not have enough mental power to drain life from your foe.")
            return(None)
        else:
            vamp_damage = round(self.secondary["spellpower"] * 2.5)
            vamp_heal = self.secondary["spellpower"] * 2
            print("With outstretched hands, you hungrily drain " + Enemy.name + " of its life-force.")
            Enemy.hp -= vamp_damage
            self.condition["hp"] += vamp_heal
            self.condition["mn"] -= 5
            print("You deal " + str(vamp_damage) + " damage and restore " + str(vamp_heal) + " hp.")
            return(None)

    def Fireball(self,Enemy):
        if (self.condition["mn"] < 6):
            print("You do not have enough mental power to conjure the great fireball.")
            return(None)
        else:
            fireball_damage = round(self.secondary["spellpower"] * 3.5) + 1
            print("Concentrating the power of the radiant sun, you forge a crackling ball of incandescent fire. At your command, the fireball surges unerringly towards its victim!")
            print("You deal " + str(fireball_damage) + " damage.")
            Enemy.hp -= fireball_damage
            self.condition["mn"] -= 6
            return(None)

    def HelpSkills(self):
        print("Syntax: skill [skill name]")
        print("\nThis is the list of all skills:")
        PrintOD(skills)
        print("\nThis is the list of the skills you possess.")
        print(self.skills)

    def HelpSpells(self):
        print("Syntax: cast [spell name]")
        print("\nThis is the list of all spells:")
        PrintOD(spells)

    def Quit(self):
        print("You give up on your adventures and retire.")
        sys.exit()

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
        return(None)

    def Combat(self,Enemy):
        # Enemy should be an object of class Mob.
        # This method should be a while loop that breaks only when:
        # (1) Player flees, (2) Enemy dies, or (3) Player dies.
        self.condition["state"] = "fighting"
        while (Enemy.hp > 0):
            # Reset posture to 1.
            self.posture = 1
            # Show the player status bar, enemy name and enemy injuries.
            self.statusbar = UpdateStatusBar(self.condition)
            enemy_fractionhp = Enemy.hp / Enemy.maxhp
            if (enemy_fractionhp > 0.75):
                enemy_injury = "Enemy: healthy"
            elif (enemy_fractionhp > 0.5):
                enemy_injury = "Enemy: injured"
            elif (enemy_fractionhp > 0.25):
                enemy_injury = "Enemy: heavily wounded"
            else:
                enemy_injury = "Enemy: nearly dead"
            prompt = self.statusbar + enemy_injury
            print(prompt)
            print("You may 'flee' or type in the name of a skill or spell to use.")
            print(self.skills)
            print(self.spells)
            combat_move = input("> ").lower()
            # Get player input text and show player available commands:
            # Flee, list of skills, and list of spells.
            if (combat_move == "flee"):
                # If flee, check for success using self speed vs enemy speed.
                # Note: if enemy is Wujin, you will fail to flee.
                speed_diff = self.secondary["speed"] * 3 - Enemy.speed
                speed_coef = speed_diff / 2
                # Probability defined by sigmoid function.
                prob_threshold = (1 / (1 + math.pow(math.exp(1), -speed_coef)))
                if (Enemy.name == "Wujin the renegade blademaster"):
                    prob_threshold = 0
                if (random.random() < prob_threshold):
                    # If flee successful, exit the Combat function and reset self state.
                    # Also reset enemy's hp to maxhp.
                    print("You manage to flee from combat. Whew!")
                    self.condition["state"] = "normal"
                    Enemy.hp = Enemy.maxhp
                    Enemy.debuffs = debuffs.copy()
                    Enemy.stun = False
                    self.buffs = buffs.copy()
                    return(None)
                else:
                    print("Try as you might, you fail to escape " + Enemy.name + "!")
            elif (combat_move in self.skills):
                # Call the appropriate skill function on the Enemy object.
                self.skilldict[combat_move](Enemy)
            elif (combat_move in self.spells):
                # Call the appropriate spell function on the Enemy object.
                if (combat_move == "recall"):
                    if (Enemy.name == "Wujin the renegade blademaster"):
                        print("You cannot recall from this duel!")
                        print("Sensing your distraction, your enemy makes its move!")
                    else:
                        print("Calmly performing your precise prestidigitation, you disappear in a flash and leave the fight!")
                        self.condition["state"] = "normal"
                        Enemy.hp = Enemy.maxhp
                        Enemy.debuffs = debuffs
                        Enemy.stun = False
                        self.buffs = buffs.copy()
                        self.room = City
                        return(None)
                else:
                    # If it's not recall, simply perform the spell.
                    self.spelldict[combat_move](Enemy)
            else:
                # Else command was not flee, a skill or a spell. Proceed to enemy turn.
                print("You fumble and miss your opportunity.")
            # Call the Enemy's attack method on the Player.
            Enemy.Attack(self)
            # Check if player hp is below 0. If so, call Player's Death method.
            if (self.condition["hp"] <= 0):
                self.Death()
        # Once the while loop ends it means the enemy is dead. End combat.
        # Reset enemy's hp to maxhp, so that next fight it will have >0 hp.
        self.condition["state"] = "normal"
        self.buffs = buffs.copy()
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
        print("You loot " + str(Enemy.loot) + " gold coins.")
        self.gold += Enemy.loot
        # Gain exp.
        print("You gain " + str(Enemy.expgiven) + " experience points.")
        self.attributes["exp"] += Enemy.expgiven
        # Record one kill in this room and reset enemy condition.
        self.room.killcount += 1
        Enemy.hp = Enemy.maxhp
        Enemy.debuffs = debuffs.copy()
        Enemy.stun = False
        # If exp exceeds tnl, level up.
        if (self.attributes["exp"] >= self.attributes["tnl"]):
            self.LevelUp()
        return(None)

    def Death(self):
        print("You have fallen in the quest for glory.")
        print("Many will follow in your footsteps, but only one hero will emerge victorious.")
        sys.exit()

    def Equip(self):
        if (self.condition["state"] == "fighting"):
            print("You cannot equip items during combat.")
            return(None)
        else:
            print("Please choose an item from your inventory to equip:")
            print(self.inventory)
            to_equip = input("> ").lower()
            self.EquipItem(to_equip)
            return(None)

    # Inventory needs no method: just print(self.inventory).
    # Equipment needs no method: just PrintOD(self.equipment).

    def Cast(self):
        print("You know the following spells:")
        print(self.spells)
        print("This is the list of all non-combat spells:")
        print(spells_noncombat)
        print("Choose a spell to cast.")
        cast_spell = input("> ")
        # Check that the player has learnt the spell.
        if (cast_spell not in self.spells):
            print("You do not know that spell!")
            return(None)
        # Check that the spell is a valid non-combat spell.
        if (cast_spell in spells_noncombat):
            self.spelldict[cast_spell]()
        return(None)

    def EquipItem(self,item):
        if (self.condition["state"] == "fighting"):
            print("You cannot equip items during combat.")
            return(None)
        else:
            if (item not in self.inventory):
                print("You do not have that item.")
                return(None)
            else:
                slot = itemstable[item][whichslot]
                # Check if you meet strength requirement.
                type = itemstable[item][whichtype]
                if (type == "armour"):
                    str_req = 6 + int(itemstable[item][whichdeflect])
                elif (type == "shield"):
                    str_req = 3 + int(itemstable[item][whichblock])
                else:
                    str_req = 0
                if (self.attributes["str"] < str_req):
                    print("You need at least " + str(str_req) + " strength to equip this.")
                    return(None)
                else:
                    if (self.equipment[slot] != None):
                        self.inventory.append(self.equipment[slot])
                    self.equipment[slot] = item
                    self.inventory.remove(item)
                    self.UpdateEquipBonus()
                    print("You equip the " + item + ". You are now wearing:")
                    PrintOD(self.equipment)
                    return(None)

    def UpdateEquipBonus(self):
        self.equipbonus = dict()
        weapon = self.equipment["mainhand"]
        shield = self.equipment["offhand"]
        if (self.equipment["body"] == None):
            body_deflect = 0
        else:
            body_deflect = int(itemstable[self.equipment["body"]][whichdeflect])
        if (self.equipment["legs"] == None):
            legs_deflect = 0
        else:
            legs_deflect = int(itemstable[self.equipment["legs"]][whichdeflect])
        if (self.equipment["feet"] == None):
            feet_deflect = 0
        else:
            feet_deflect = int(itemstable[self.equipment["feet"]][whichdeflect])
        if (self.equipment["hands"] == None):
            hands_deflect = 0
        else:
            hands_deflect = int(itemstable[self.equipment["hands"]][whichdeflect])
        if (weapon == None):
            self.equipbonus["weaponmax"] = 0
            self.equipbonus["weaponmin"] = 0
        else:
            self.equipbonus["weaponmax"] = int(itemstable[weapon][whichmaxdam])
            self.equipbonus["weaponmin"] = int(itemstable[weapon][whichmindam])
        if (shield == None):
            self.equipbonus["block"] = 0
        else:
            self.equipbonus["block"] = int(itemstable[shield][whichblock])
        self.equipbonus["deflect"] = body_deflect + legs_deflect + feet_deflect + hands_deflect

    def Challenge(self):
        print("You proclaim your challenge for all the lands to hear.")
        print("Within a few days, Wujin the renegade blademaster arrives to slay you.")
        Wujin = mobdict_objects["Wujin the renegade blademaster"]
        self.Combat(Wujin)

class Mob(object):
    def __init__(self,name,hp,defence,attack,speed,expgiven,loot):
        self.name = name
        self.hp = int(hp)
        self.maxhp = int(hp)
        self.defence = int(defence)
        self.attack = int(attack)
        self.speed = int(speed)
        self.expgiven = int(expgiven)
        self.loot = int(loot)
        self.stun = False
        # Moveset is the list of attacks they can use.
        self.moveset = ["Attack"]
        # Moveprob is the probability of using each attack.
        self.moveprob = [1]
        # Debuffs can be applied by player.
        self.debuffs = debuffs.copy()
    def Attack(self,Player):
        # If the mob is stunned, set stun to False and mob misses turn.
        if (self.stun == True):
            print(self.name + " is stunned and unable to act.")
            self.stun = False
            Player.posture = 1
            return(None)
        # Determine block probability if player has shield.
        if (Player.equipment["offhand"] == None):
            pass
        else:
            enemy_penetration = 0.5 * self.attack + 0.5 * self.speed
            blockvalue = round(Player.posture * (Player.secondary["damroll"] + Player.equipbonus["block"] + Player.buffs["block"]))
            blockroll_min = round(0.25 * blockvalue)
            blockroll = random.randint(blockroll_min,blockvalue)
            if (self.attack > (2 * blockroll + blockroll_min) and Player.posture > 0):
                # Player shield breaks.
                print("With a decisive blow, " + self.name + " cleaves your shield in twain!")
                Player.equipment["offhand"] = None
                Player.UpdateEquipBonus()
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
        enemy_attackroll = self.attack - self.debuffs["attack"]
        # Determine character defence roll.
        base_defence = Player.secondary["speed"] + Player.equipbonus["deflect"] + Player.buffs["deflect"]
        char_defroll_min = round(0.25 * base_defence)
        char_defroll = random.randint(char_defroll_min,base_defence)
        # Determine enemy damage done.
        enemy_damage_done = max(0,enemy_attackroll - char_defroll)
        if (enemy_damage_done > 0):
            print(self.name + " slips past your defences and savagely wounds you.")
            print("You take " + str(enemy_damage_done) + " damage.")
            Player.condition["hp"] -= enemy_damage_done
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

class Town(object):
    def __init__(self,name,desc):
        Room.__init__(self,name,desc)
        self.is_town = True
    def __str__(self):
        return(self.desc)

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

# Debuffs on mobs. These initialize at 0.
debuffs = {
    "attack": 0,
    "defence": 0,
    "speed": 0
}

def ReinstantiateMobs():
    for k,v in mobdict.items():
        mobdict_objects[k] = Mob(v[0],v[1],v[2],v[3],v[4],v[5],v[6])

ReinstantiateMobs()

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
skills_req["shatter"] = [12, 36]
skills_req["bash"] = [14, 42]
skills_req["sunder"] = [16, 64]
skills_req["weaken"] = [18, 72]
skills_req["charge"] = [20, 80]
skills_req["execute"] = [22, 66]
skills_req["flurry"] = [24, 96]

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
spells_req["blast"] = [10, 30]
spells_req["heal"] = [14, 56]
spells_req["refresh"] = [16, 64]
spells_req["barrier"] = [14, 56]
spells_req["premonition"] = [12, 36]
spells_req["enfeeble"] = [12, 36]
spells_req["freeze"] = [14, 42]
spells_req["vampiric"] = [18, 72]
spells_req["fireball"] = [24, 96]
spells_req["recall"] = [24, 78]

spells_noncombat = ["heal","refresh","barrier","premonition","recall"]

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

# Player = Character("DevTest")

print("Welcome to the Legend of Wujin!")
print("Please read the readme.txt file for instructions.")
print("Is this debug mode? If so, supply the code.")
debugcode = input("> ")
player_name = "Placeholder"
# Create player object of class Character.
player = Character(player_name)

# Debug mode: make character very high stats and high gold.
if (debugcode == "debug"):
    player.gold = 5000
    player.attributes["str"] = 34
    player.attributes["dex"] = 34
    player.attributes["int"] = 24
    player.attributes["maxhp"] = 100
    player.attributes["maxmn"] = 80
    player.attributes["maxsta"] = 80
    player.equipment["mainhand"] = "meteor hammer"
    player.equipment["offhand"] = "steel shield"
    player.equipment["legs"] = "plate leggings"
    player.equipment["feet"] = "reinforced boots"
    player.equipment["hands"] = "mail gauntlets"
    player.equipment["body"] = "heavy platemail"
    player.secondary = LevelUpSecondary(player.attributes)
    player.spells = ["blast","heal","refresh","barrier","premonition","enfeeble","freeze","vampiric","fireball","recall"]
    player.skills = ["atk","def","str","shatter","bash","sunder","weaken","charge","execute","flurry"]
else:
    pass

print("You begin your adventure in Xian City.")
# Game is a while loop that continues until player dies, or wins.
rounds_taken = 0
while (True):
    # rounds_taken records the number of rounds you took to win the game.
    rounds_taken += 1
    command = input("> ").lower()
    player.UpdateEquipBonus()
    if (command in cardinal_directions):
        # Player is moving.
        player.Move(command)
    elif (command == "rest"):
        player.Rest()
    elif (command == "hunt"):
        player.Hunt()
    elif (command == "look"):
        player.Look()
    elif (command == "score"):
        player.Score()
    elif (command == "inv"):
        print("You have the following items:")
        print(player.inventory)
        print("Gold: " + str(player.gold))
    elif (command == "eq"):
        PrintOD(player.equipment)
    elif (command == "equip"):
        player.Equip()
    elif (command == "shop"):
        player.Shop()
    elif (command == "train"):
        player.Train()
    elif (command == "cast"):
        player.Cast()
    elif (command == "challenge"):
        player.Challenge()
    elif (command == "quit"):
        player.Quit()
    else:
        print("I do not understand what you want to do. Look at readme.txt for help.")
