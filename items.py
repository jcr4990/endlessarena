
class Item():
    """The base class for all items"""
    def __init__(self, name, value):
        self.name = name
        self.value = value
 



class Weapon(Item):
    def __init__(self, name, damage, value):
        self.damage = damage
        super().__init__(name, value)



class Armor(Item):
    def __init__(self, name, slot, ac, value):
        self.ac = ac
        self.slot = slot
        super().__init__(name, value)
 


# Once shop implemented use following code to remove current weapon from inv upon buying new weapon
# for i, x in enumerate(player.inventory):
# 	check_weapon = isinstance(x, Weapon)
# 	if check_weapon is True:
# 		del player.inventory[i]

# following code to replace armor slot when buying new chest item for example
# for i, x in enumerate(player.inventory):
#   if x.slot == "Chest":
#   del player.inventory[i]