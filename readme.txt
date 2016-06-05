Text-based role-playing adventure
The Legend of Wujin



Story

Everyone has heard the tales concerning Wujin, the indomitable blademaster of the Wu-Dang Temple. He was a virtuous student of the sword, and rapidly became the mightiest and most respected swordsman of his era. Undefeated in every duel, it was said that his skin bore not a scratch of the thousands of battles he has fought. He was strong as the bear, swift as the cat, and was equipped with the finest armour of hardened steel and his storied longsword, "Rising Phoenix". 

However, his intense study of the martial arts led him to madness. His fall from grace was as swift as his meteoric rise, and soon he gathered brigands and barbarians to prey on the people of the Empire. Each day, hundreds of peasants lose their homes and possessions as his henchmen ravage the countryside. 

You are a young adventurer, keen to secure yourself a place in the history books, and rid Imperial China of this menace. Will you succeed where others have failed? 



How To Play

Download game.py, items.csv, map.csv, mobs.csv and place them in the same folder. 

You need to set up Python 3, and execute game.py with the python.exe in your operating system. Download Python 3 from www.python.org. Open your OS' terminal (e.g. Windows CMD, Windows Powershell, Mac OS Terminal, etc.), and navigate to the folder containing game.py. 

Call python.exe on game.py like this (if your Python 3 is in C:/Python3/): C:/Python3/python.exe game.py



Controls

When you are not in combat, you can move, shop, train, hunt, etc. 

List of possible commands: 

north/south/east/west: move in cardinal direction to adjoining 'room' (location)
rest: rest and restore hp, stamina, mind
hunt: hunt for enemies in this room
look: look at the room you are in
score: display your attributes, condition, known skills, and known spells
inv: display your inventory and gold
eq: display your equipment
equip: opens the equipping dialogue
shop: opens the shop dialogue which can only be done in town
train: opens the training dialogue only in town
cast: opens the out-of-combat spell dialogue
challenge: start the final boss fight
quit: quits the game

When you are in combat, the list of commands is strongly restricted. You may only follow the prompts in the combat text. 

Shortcuts: 

In all situations except gaining a level, you do not need to type the full command. Useful examples of shortcuts:

"h": "hunt"
"i": "inventory"
"r": "rest"
"n": "north" (same for all other directions)

When equipping items, you can select your desired item with a shortcut too: 
For example, you have the items ["cloth gloves", "wooden buckler"]. When equipping, you can type "c" and it will know to equip "cloth gloves".

List of combat commands:

flee: attempts to flee
[skill name]: uses skill corresponding to [skill name]
[spell name]: uses spell corresponding to [spell name]

Again, shortcuts can be used in combat too.



Navigation

The game features 7 "rooms". Xian City is the central hub connecting 4 wilderness rooms.

South: Pearl River Delta: lowest-level area. 
East: Coast of the Yellow Sea: second-lowest-level area. 
North: Cold Steppes: third area. 
West: Highland Plateau: fourth area. 

Further afield, there are 2 more wilderness rooms which are very dangerous.

West of Highland Plateau: Sky-Burial Ridge: highest level area from which egress is possible only through use of the Recall spell; features highest-level mob, the sinister thunder demon.
South of Pearl River Delta: The Misty Jungle: very high level area featuring monsters more powerful than Highland Plateau's.

All your commands should be in lower case, even though the game should be able to understand upper case versions. 

Type "north" or any cardinal direction to move. You can only move in directions for which exits exist: e.g. you can move north from Pearl River Delta to Xian City but you cannot move in any other direction. 

Moving from a wilderness zone runs the risk of ambush. 



Levelling Up: 

You can HUNT in Xian City to start with killing rats, the weakest enemy. You can HUNT in any of the 4 wilderness zones to kill stronger enemies. Note the level recommendations above. 

When you gain enough experience, you will automatically level-up. You do not have to initiate this process. This will happen after you gain experience past the threshold. Excess experience past the threshold does not count towards your next level. 

You will choose one attribute out of six [str, dex, int, maxhp, maxsta, maxmn] to improve when you gain a level. 



Attributes: 

Strength: increases melee damage and permits wearing heavier armour. 
Dexterity: increases defence, permits learning new skills, and improves the chance of fleeing. 
Intelligence: increases spell power and permits learning new spells. 
Max HP: increases maximum hit points (hp). If hp go down to zero, you die. 
Max Stamina: increases maximum stamina (sta). Stamina is used for performing skills. 
Max Mind: increases maximum mind (mn). Mind is used for casting spells. 
Experience: experience points (exp). 
Level: current experience level. 
To Next Level: the number of exp needed to gain the next level. 



Shopping: 

You can shop in town. Type "shop" when in Xian City to initiate the shopping process. Follow the instructions on screen. For a list of items and their statistics, see "items.csv". 



Equipment: 

When you buy an item, it goes into your Inventory. Type "equip" to initiate the equipment process. You will then select the item you wish to equip. 



Training: 

You can train in town. Type "train" when in Xian City to initiate the training process. Follow the instructions on screen. If you type something that is not recognized by the training process, then it will put you out of the training process. You may try again by entering "train" again. 

You start with only the three basic attack skills: [atk, def, str]. To learn more, you must train. 

This is the list of skills, their stamina cost, dexterity requirement, and description. 

atk: 1 sta 0 dex: normal attack
def: 1 sta 0 dex: defensive attack has higher block chance
str: 1 sta 0 dex: aggressive attack has no block chance
shatter: 3 sta 12 dex: ignores enemy defence and scales with Strength
bash: 3 sta 14 dex: has a chance to deny enemy attack and chance scales with Strength
sunder: 3 sta 16 dex: light attack reduces enemy defence and reduction scales with Dexterity
weaken: 3 sta 18 dex: light attack reduces enemy offence and reduction scales with Dexterity
charge: 4 sta 20 dex: heavy attack more effective if enemy hp high and damage scales with Strength
execute: 6 sta 22 dex: heavy attack more effective if enemy hp low and damage scales with Dexterity
flurry: 8 sta 24 dex: attacks 2 to 5 times and number of attacks scales with Dexterity

You start with no spells. To learn spells, you must train. 

This is the list of spells, their mind cost, intelligence requirement, and description. 

blast: 1 mn 10 int: basic attack
heal: 2 mn 14 int: heals hp and usable out of combat
refresh: 3 mn 16 int: heals stamina and usable out of combat
barrier: 3 mn 14 int: increases defence for present or next combat but fades after fight ends, usable out of combat
premonition: 3 mn 12 int: increases block chance for present or next combat but fades after fight ends, usable out of combat
enfeeble: 3 mn 12 int: damages and decreases enemy offence
freeze: 3 mn 14 int: damages with chance to deny enemy attack
vampiric: 5 mn 18 int: vampiric touch damages enemy and heals self
fireball: 6 mn 24 int: deals great damage
recall: 8 mn 24 int: sends you to town, usable out of combat



Fighting: 

Combat is turn-based, and you can either flee, use a skill, or use a spell. 

Fleeing depends on your speed vs enemy speed. If you fail to flee, you miss your turn and enemy will attack you. 



Resting: 

Using "rest" in town will safely restore your status to maximum for 5 gold. 

Using "rest" out of town still requires 5 gold due to cost of supplies, and will restore 50% of your status, provided that you do not get ambushed. 

Rest in town! Keep in mind, however, that moving from a wilderness zone carries the risk of being ambushed. 



Victory: 

Once you believe yourself to be ready, type "challenge" in Xian City and you will seek out Wujin for a duel. You cannot flee from this duel. 

If you defeat Wujin in combat, then you win the game! 



Please send me any suggestions for improving or balancing the game and I will take them into account for the next game update! 



Changelog: 

Implemented 1. Made the game not allow you to train a skill or spell you already know. 
Implemented 2. Made the prompt show if you are in the training hall, or exploring the world, or in levelling up, etc. 
Implemented 3. Shortened commands that are frequently used: n/s/e/w, h for hunt, sc for score. 
Decided not to 4. Allow equipping items in one line "equip cloth gloves" instead of having to open the equip dialogue. 
Decided not to 5. Allow casting spells in one line. 
Implemented 6. More flavour text for zones. 
Balance 8. Gameplay balance by increasing exp given by higher level mobs. 
Bugfix 9. Fixed Blast so that it uses 1 mind instead of 3. 
Implemented 10. Gameplay balance by reducing likelihood of shield being destroyed by mobs. 
Bugfix 11. Added coercion to string for the message that comes when you do not have the gold for training a spell. 
Bugfix 12. Fixed function call Character.Room.EnemyEncounter() to Character.EnemyEncounter () inside Character.Rest() function.
Implemented 13. Two more zones, more mobs, several legendary items, and increased strength of boss.
Implemented 14. Balanced high-level mobs exp given to match the difficulty and time requirement.
Implemented 15. Fully-generalized acceptance of any substring of a command ("shortcut") in place of command.

Future Features List:

DONE 1. Make generalized acceptance of any substring of a command instead of hard-coded shortcuts.
2. Make a GUI with status bar, inventory, equipment, location all displayed along with the console.