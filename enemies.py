import random

class Enemy:
    """Represents an enemy in the game."""
    def __init__(self, name, hp, ac, damage, inventory):
        self.name = name
        self.hp = hp
        self.ac = ac
        self.damage = damage
        self.inventory = inventory
        self.maxhp = self.hp
        self.mitigation = int(self.ac * 0.25)

    def is_alive(self):
        return self.hp > 0

    @staticmethod
    def random(level):
        name = random.choice(enemy_names)
        hp = 10 + (level * (level // 2))
        ac = 5 + (level * (level // 3))
        damage = 5 + level
        enemy = Enemy(name, hp, ac, damage, [])
        return enemy


enemy_names = ["a mountain lion", "a grizzly bear", "a rattlesnake", "a bandit", "a wolf",
"an oozing slime", "a fire elemental", "a water elemental", "an air elemental", "an earth elemental",
"a fire giant", "an ice giant", "a kobold", "a gnoll", "a goblin", "an orc"]
