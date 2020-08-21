from discord.ext import commands 
from bot_token import TOKEN
from player import Player
from enemies import Enemy
import pickle
import random
import asyncio

bot = commands.Bot(command_prefix='/')
# bot.remove_command("help")

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
    if message.content == "hi":
        await message.channel.send("Hello")

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

    player = Player(name, 1, 1, [])
    # player.hp = 100
    save(name, player)

    msg = cb(f"Welcome to Endless Arena!\nCharacter Name: {player.name}\nLevel: {player.level}\nHP: {player.hp}\nAC: {player.ac}")
    await ctx.send(msg)


@bot.command()
async def battle(ctx):
    if ctx.author.nick is None:
        name = ctx.author.name
    else:
        name = ctx.author.nick

    player = load(name)
    combat_round = 0
    
    enemy = Enemy.random(player.level)
    await ctx.send(cb(f"Entering combat with {enemy.name}..."))
    await asyncio.sleep(3)

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

        
        msg = cb(f"ROUND:{combat_round}\n{player.name} hit for {dmg_dealt} damage!\n{enemy.name} hit for {dmg_received} damage!\n\n{player.name}: {player.hp}/{player.maxhp}hp\n{enemy.name}: {enemy.hp}/{enemy.maxhp}hp")
        await ctx.send(msg)

        if player.hp <= 0:
            await ctx.send(cb(f"You have been slain by {enemy.name}."))
            break

        if enemy.hp <= 0:
            await ctx.send(cb(f"You have slain {enemy.name}!!!"))
            break



        await asyncio.sleep(3)

        
    save(name, player)


        












if __name__ == "__main__":
    bot.run(TOKEN)
