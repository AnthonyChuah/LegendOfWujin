Text-based role-playing adventure


World should consist of 5 rooms with one central connecting room. 
From central room (Town) you can go [north south east west] to zones. 


Program Classes: 

* Character, Mob
* Item, Weapon, Armour, Shield
* Room, Town (special Room)

Functions: 

* Hunt - reference Room to lookup monster
* Generally, all character commands! 
* Also Fighting function. 


Note: 

* Python DOES NOT DO LAZY EVALUATION. Therefore in class creation, for Room please define all attributes that Town should have. 