import random
from items import Item, Weapon, Armor

class Enemy:
    """Represents an enemy in the game."""
    def __init__(self, name, level, inventory):
        self.name = name
        self.hp = 10 + (level * (level // 2))
        self.ac = 5 + (level * (level // 3))
        self.damage = damage = 5 + level
        self.inventory = inventory
        self.maxhp = self.hp
        self.mitigation = int(self.ac * 0.25)
        self.gold = random.randint(int((level * 0.8)), int((level * 1.2)))

    def is_alive(self):
        return self.hp > 0

    @staticmethod
    def random(level):
        name = random.choice(enemy_names)
        gold = random.randint(int((level * 0.8)), int((level * 1.2)))
        enemy = Enemy(name, level, [])
        return enemy


enemy_names = ["a mountain lion", "a grizzly bear", "a rattlesnake", "a bandit", "a wolf",
"an oozing slime", "a fire elemental", "a water elemental", "an air elemental", "an earth elemental",
"a fire giant", "an ice giant", "a kobold", "a gnoll", "a goblin", "an orc"]
