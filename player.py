

class Player:
    """Represents the player in the game."""
    def __init__(self, name, level, exp, inventory):
        self.name = name
        self.level = level
        self.exp = exp
        self.inventory = inventory
        self.gold = 0
        self.hp = 10 + (level * (level // 2))
        self.ac = 5 + (level * (level // 3))
        self.damage = 5 + level
        self.maxhp = self.hp
        self.mitigation = int(self.ac * 0.25)

        for item in inventory:
            try:
                self.ac += item.ac
                self.mitigation = int(self.ac * 0.25)
            except AttributeError:
                pass

            try:
                self.damage += item.damage
            except AttributeError:
                pass
            


    def is_alive(self):
        return self.hp > 0

    