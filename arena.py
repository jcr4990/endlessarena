import pickle
import random
import asyncio
from discord.ext import commands
from bot_token import TOKEN
from player import Player
from enemies import Enemy
from items import Weapon, Armor


bot = commands.Bot(command_prefix='/')
# bot.remove_command("help")

# def check(m):
#     return m.author.name == name


def cb(content):
    return f"```{content}```"


def save(filename, var):
    with open(f"data/{filename}.dat", "wb") as f:
        pickle.dump(var, f)


def load(filename):
    with open(f"data/{filename}.dat", "rb") as f:
        return pickle.load(f)

# On Message


@bot.event
async def on_message(message):
    """Discord 'on_message' function"""
    if message.author == bot.user:
        return

    # On message logic here

    await bot.process_commands(message)


@bot.event
async def on_ready():
    """Discord 'on_ready' function"""
    print('Activating Bot')
    print('Name: ' + bot.user.name)
    print('ID: ' + str(bot.user.id))
    print('----------------')


@bot.command()
async def create(ctx):
    if ctx.author.nick is None:
        name = ctx.author.name
    else:
        name = ctx.author.nick

    bronze_dagger = Weapon(name="Bronze Dagger", damage=10, dexterity=15, value=4)
    print(f"Name:{bronze_dagger.name} Dmg:{bronze_dagger.damage} Str:{bronze_dagger.strength} Dex:{bronze_dagger.dexterity} Val:{bronze_dagger.value}")

    rusty_sword = Weapon("Rusty Sword", 3, 0)
    rusty_armor = Armor("Rusty Armor", "Chest", 3, 0)
    player = Player(name, 1, 1, [rusty_sword, rusty_armor])
    # player.hp = 100
    save(name, player)

    msg = cb(f"Welcome to Endless Arena!\nCharacter Name: {player.name}\nLevel: {player.level}\nHP: {player.hp}\nAC: {player.ac}\nMax Damage: {player.damage}")
    await ctx.send(msg)


@bot.command(aliases=['inv'])
async def inventory(ctx):
    if ctx.author.nick is None:
        name = ctx.author.name
    else:
        name = ctx.author.nick

    player = load(name)

    item_names = []
    for item in player.inventory:
        item_names.append(item.name)

    newline = "\n"
    msg = cb(f"{player.name}'s Inventory:\n{player.gold} Gold\n{newline.join(item_names)}")
    await ctx.send(msg)


@bot.command()
async def battle(ctx):
    if ctx.author.nick is None:
        name = ctx.author.name
    else:
        name = ctx.author.nick

    player = load(name)
    if not player.is_alive():
        await ctx.send(cb("You are dead. Use /create to create a new character."))
        return
    combat_round = 0

    enemy = Enemy.random(player.level)
    await ctx.send(cb(f"Entering combat with {enemy.name}..."))
    await asyncio.sleep(2)

    while True:
        combat_round += 1

        # Outgoing Damage Calcs
        player_dmg_preac = random.randint(0, player.damage)
        dmg_dealt = player_dmg_preac - enemy.mitigation
        if dmg_dealt <= 0:
            dmg_dealt = 0
        enemy.hp = enemy.hp - dmg_dealt

        # Incoming Damage Calcs
        enemy_dmg_preac = random.randint(0, enemy.damage)
        dmg_received = enemy_dmg_preac - player.mitigation
        if dmg_received <= 0:
            dmg_received = 0
        player.hp = player.hp - dmg_received

        msg = cb(f"ROUND:{combat_round}\n{player.name} hit for {dmg_dealt} damage!\n{enemy.name} hit for {dmg_received} damage!\n\n{player.name}: {player.hp}/{player.maxhp}hp\n{enemy.name}: {enemy.hp}/{enemy.maxhp}hp\n\n1: Continue\n2: Attempt to flee")
        await ctx.send(msg)

        if not player.is_alive():
            await ctx.send(cb(f"You have been slain by {enemy.name}."))
            break

        if not enemy.is_alive():
            if enemy.gold == 0:
                enemy.gold = 1
            player.gold += enemy.gold

            await ctx.send(cb(f"You have slain {enemy.name}!\nYou loot {enemy.gold} gold from their corpse!"))
            break

        try:
            msg = await bot.wait_for('message', timeout=60.0, check=lambda message: message.author == ctx.author)
        except asyncio.TimeoutError:
            await ctx.send("Timed out waiting for response - Game Over")
            break
        else:
            if msg.content == "1":
                continue
            elif msg.content == "2":
                await ctx.send("You ran away!")
                break

    # Save player object at completion of each battle
    save(name, player)


if __name__ == "__main__":
    bot.run(TOKEN)
