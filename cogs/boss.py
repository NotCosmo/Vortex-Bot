# Main Imports

import nextcord as discord
import random
import asyncio
import time

# Other

from datetime import datetime
from nextcord.ext import commands
from nextcord.ext.commands import BucketType
from nextcord.utils import find
from pymongo import MongoClient
from loot import *

quest_instance = False

# ------------------------------- #
''' Cluster '''
# ------------------------------- #

cluster = MongoClient("mongodb+srv://Cosmo:1H1uqPGjo5CjtHQe@eco.5afje.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
database = cluster["Discord"]
eco = database["Economy"]

#
''' Boss Class '''
#

class NewBoss():
    
    def __init__(self, name, desc, health, mindamage, maxdamage, loot):
        self.name = name
        self.desc = desc
        self.health = health
        self.mindamage = mindamage
        self.maxdamage = maxdamage
        self.loot = loot

class Player():
    
    def __init__(self, name, health, originalhealth, mindamage, maxdamage, agility):
        self.name = name
        self.health = health
        self.originalhealth = originalhealth
        self.mindamage = mindamage
        self.maxdamage = maxdamage
        self.agility = agility
        self.potionActive = False

# ------------------------------- #
''' Setup '''
# ------------------------------- #

class Boss(commands.Cog):

    def __init__(self, client):
        self.client = client

    MinionLoot = []

    @commands.group(invoke_without_command=True)
    @commands.cooldown(1, 1, BucketType.user)
    async def boss(self, ctx, *, bossName=None):

        await ctx.send("What boss are you trying to fight?")

    @boss.command(aliases = ["Minion"])
    @commands.cooldown(1, 1, BucketType.user)
    async def minion(self, ctx):

        # Weapon drop needs to be made
        weaponDrop = find(lambda r: r.name == "Minion Drop Here", ctx.message.guild.roles)
        logs = self.client.get_channel(873941431570546770)

        atkspeed = 1.5
        boss = NewBoss(
            name="Raven's Minion",
            desc="Temp Desc",
            health=5000,
            mindamage=80,
            maxdamage=120,
            loot=[],
        )
        # name, health, originalhealth, mindamage, maxdamage, agility
        player = Player(
            name=ctx.author.name,
            health=2500,
            originalhealth=2500,
            mindamage=150,
            maxdamage=300,
            agility=0,
        )

        em = discord.Embed(
            title=boss.name,
            colour=discord.Colour.from_rgb(0, 208, 255)
        )
        em.add_field(name="Boss Health", value = f":heart: {boss.health:,}", inline=True)
        em.add_field(name="Player Health", value = f":heart: {player.health:,}", inline=True)
        em.add_field(name="Last Action", value="`Boss initiated.`", inline=False)
        em.add_field(name="Difficulty", value=":star:", inline=False)
        em.timestamp = datetime.utcnow()

        msg = await ctx.send(embed=em)

        '''
        Potion Work 
        '''

        # Boss loop
        while (boss.health > 0) and (player.health) > 0:

            await asyncio.sleep(atkspeed)

            player_dps = random.randint(player.mindamage, player.maxdamage)
            boss.health -= player_dps
            em2 = discord.Embed(
                title=boss.name,
                colour=discord.Colour.from_rgb(0, 208, 255)
            )
            em2.add_field(name="Boss HP",value=f":heart: {boss.health:,}",inline=True)
            em2.add_field(name="Player HP",value=f":heart: {player.health:,}",inline=True)
            em2.add_field(name="Last Action",value=f"> {ctx.author.name} dealt :crossed_swords: {player_dps:,}", inline=False)
            em2.timestamp = datetime.utcnow()
            await msg.edit(embed=em2)

            await asyncio.sleep(atkspeed)

            boss_dps = random.randint(boss.mindamage, boss.maxdamage)
            player.health -= boss_dps
            em3 = discord.Embed(
                title=boss.name,
                colour=discord.Colour.from_rgb(0, 208, 255)
            )
            em3.add_field(name="Boss HP",value=f":heart: {boss.health:,}",inline=True)
            em3.add_field(name="Player HP",value=f":heart: {player.health:,}",inline=True)
            em3.add_field(name="Last Action",value=f"> {boss.name} dealt :crossed_swords: {boss_dps:,}", inline=False)
            em3.timestamp = datetime.utcnow()
            await msg.edit(embed=em3)

            # Boss has died
            if boss.health <= 0:

                boss.health = 0
                # Check if player is also dead
                if player.health <= 0:
                    #if boss.health <= 0:
                    #    boss.health = 0
                    player.health = 0
                    em = discord.Embed(title="Boss has defeated you.",description="You were weakened and had to flee the boss fight.",colour=discord.Colour.from_rgb(255, 95, 95))
                    em.timestamp = datetime.utcnow()
                    return await ctx.send(ctx.author.mention, embed=em)
                    # await ctx.author.remove_roles(keyreq)

                # Boss defeated
                else:

                    Economy = eco.find_one({"memberid":ctx.author.id})
                    quest = Economy["currentQuest"]

                    if quest == "Merlin1":
                        eco.update_one({"memberid":ctx.author.id},{"$set":{"currentQuest":"Merlin2"}})

                        em = discord.Embed(title="Quest Completed!",description="Successfully completed Merlin's quest. Head back to >quest Merlin to get your next quest.",colour=discord.Colour.from_rgb(95, 255, 95))
                        em.set_author(name=ctx.author, icon_url=ctx.author.display_avatar)
                        em.timestamp = datetime.utcnow()
                        await ctx.send(embed=em)

                    # LOOT
                    em = discord.Embed(title="Boss has fled.",description="You forced the boss to flee.",colour=discord.Colour.from_rgb(95, 255, 95))
                    em.add_field(name="Loot", value="> Minion's Drop (100%)", inline=False)
                    em.timestamp = datetime.utcnow()
                    return await ctx.send(ctx.author.mention, embed=em)
                    # await ctx.author.remove_roles(keyreq)

            elif player.health <= 0:
                player.health = 0
                em = discord.Embed(title="You fled.",description="> You were overpowered and forced to flee, the boss escaped.", colour=discord.Colour.from_rgb(255, 95, 95))
                em.timestamp = datetime.utcnow()
                return await ctx.send(embed=em)
                # await ctx.author.remove_roles(keyreq)

    @boss.command(aliases = ["Follower"])
    @commands.cooldown(1, 1, BucketType.user)
    async def follower(self, ctx):

        # Weapon drop needs to be made
        cursed_staff = find(lambda r: r.name == "✧ Cursed Staff", ctx.message.guild.roles)

        weapon_drop = find(lambda r: r.name == "✪ Raven's Dagger", ctx.message.guild.roles)
        amulet_drop = find(lambda r: r.name == "✪ Darkness Amulet", ctx.message.guild.roles)
        logs = self.client.get_channel(873941431570546770)

        atkspeed = 1.5
        boss = NewBoss(
            name="Raven's Follower",
            desc="Temp Desc",
            health=7500,
            mindamage=200,
            maxdamage=250,
            loot=follower_loot,
        )
        # name, health, originalhealth, mindamage, maxdamage, agility
        player = Player(
            name=ctx.author.name,
            health=2500,
            originalhealth=2500,
            mindamage=150,
            maxdamage=300,
            agility=0,
        )

        if cursed_staff in ctx.author.roles:
            player.health += 500
            player.originalhealth += 500
            player.mindamage += 350
            player.maxdamage += 350

        em = discord.Embed(
            title=boss.name,
            colour=discord.Colour.from_rgb(0, 208, 255)
        )
        em.add_field(name="Boss Health", value = f":heart: {boss.health:,}", inline=True)
        em.add_field(name="Player Health", value = f":heart: {player.health:,}", inline=True)
        em.add_field(name="Last Action", value="`Boss initiated.`", inline=False)
        em.add_field(name="Difficulty", value=":star:", inline=False)
        em.timestamp = datetime.utcnow()

        msg = await ctx.send(embed=em)

        '''
        Potion Work 
        '''

        # Boss loop
        while (boss.health > 0) and (player.health) > 0:

            await asyncio.sleep(atkspeed)

            player_dps = random.randint(player.mindamage, player.maxdamage)
            if player.health <= 0:
                player.health = 0
                player_dps = 0
            boss.health -= player_dps
            em2 = discord.Embed(
                title=boss.name,
                colour=discord.Colour.from_rgb(0, 208, 255)
            )
            em2.add_field(name="Boss HP",value=f":heart: {boss.health:,}",inline=True)
            em2.add_field(name="Player HP",value=f":heart: {player.health:,}",inline=True)
            em2.add_field(name="Last Action",value=f"> {ctx.author.name} dealt :crossed_swords: {player_dps:,}", inline=False)
            em2.timestamp = datetime.utcnow()
            await msg.edit(embed=em2)

            await asyncio.sleep(atkspeed)

            boss_dps = random.randint(boss.mindamage, boss.maxdamage)
            if boss.health <= 0:
                boss.health = 0
                boss_dps = 0
            player.health -= boss_dps
            em3 = discord.Embed(
                title=boss.name,
                colour=discord.Colour.from_rgb(0, 208, 255)
            )
            em3.add_field(name="Boss HP",value=f":heart: {boss.health:,}",inline=True)
            em3.add_field(name="Player HP",value=f":heart: {player.health:,}",inline=True)
            em3.add_field(name="Last Action",value=f"> {boss.name} dealt :crossed_swords: {boss_dps:,}", inline=False)
            em3.timestamp = datetime.utcnow()
            await msg.edit(embed=em3)

            # Boss has died
            if boss.health <= 0:

                boss.health = 0
                # Check if player is also dead
                if player.health <= 0:
                    #if boss.health <= 0:
                    #    boss.health = 0
                    player.health = 0
                    em = discord.Embed(title="Boss has defeated you.",description="You were weakened and had to flee the boss fight.",colour=discord.Colour.from_rgb(255, 95, 95))
                    em.timestamp = datetime.utcnow()
                    return await ctx.send(ctx.author.mention, embed=em)
                    # await ctx.author.remove_roles(keyreq)

                # Boss defeated
                else:

                    Economy = eco.find_one({"memberid":ctx.author.id})
                    quest = Economy["currentQuest"]

                    # Defeat Boss 10 times
                    if quest == "Merlin3":
                        
                        Economy = eco.find_one({"memberid":ctx.author.id})
                        boss_kills = Economy["totalBossKills"]
                        quest_objective = Economy["questObjectiveCounter"]

                        eco.update_one({"memberid":ctx.author.id},{"$set":{"totalBossKills":boss_kills+1}})
                        eco.update_one({"memberid":ctx.author.id},{"$set":{"questObjectiveCounter":quest_objective+1}})
                        quest_instance = True

                        quest_objective_updated = Economy["questObjectiveCounter"]
                        if quest_objective_updated >= 10:


                        #eco.update_one({"memberid":ctx.author.id},{"$set":{"currentQuest":"Merlin2"}})

                            em = discord.Embed(title="Quest Completed!",description="Successfully completed Merlin's quest. Head back to >quest Merlin to get your next quest.",colour=discord.Colour.from_rgb(95, 255, 95))
                            em.set_author(name=ctx.author, icon_url=ctx.author.display_avatar)
                            em.timestamp = datetime.utcnow()
                            await ctx.send(embed=em)
                            eco.update_one({"memberid":ctx.author.id},{"$set":{"questObjectiveCounter":0}})
                            eco.update_one({"memberid":ctx.author.id},{"$set":{"currentQuest":"Merlin4"}})

                    # LOOT
                    em = discord.Embed(title="Boss has fled.",description="You forced the boss to flee.",colour=discord.Colour.from_rgb(95, 255, 95))
                    
                    l1 = random.choice(boss.loot)
                    l2 = random.choice(boss.loot)
                    l3 = random.choice(boss.loot)

                    if l1 == "Darkness Amulet" or l2 == "Darkness Amulet" or l3 == "Darkness Amulet":
                        await ctx.author.add_roles(amulet_drop)

                    if l1 == "Raven's Dagger" or l2 == "Raven's Dagger" or l3 == "Raven's Dagger":
                        await ctx.author.add_roles(weapon_drop)
                    
                    em.add_field(name="Loot", value=f"> {l1}\n> {l2}\n> {l3}", inline=False)
                    em.timestamp = datetime.utcnow()

                    if quest_instance == False:
                        Economy = eco.find_one({"memberid":ctx.author.id})
                        boss_kills = Economy["totalBossKills"]
                        eco.update_one({"memberid":ctx.author.id},{"$set":{"totalBossKills":boss_kills+1}})

                    return await ctx.send(ctx.author.mention, embed=em)
                    # await ctx.author.remove_roles(keyreq)

            elif player.health <= 0:
                player.health = 0
                em = discord.Embed(title="You fled.",description="> You were overpowered and forced to flee, the boss escaped.", colour=discord.Colour.from_rgb(255, 95, 95))
                em.timestamp = datetime.utcnow()
                return await ctx.send(embed=em)
                # await ctx.author.remove_roles(keyreq)

    @boss.command(aliases = ["Gryphon"])
    @commands.cooldown(1, 1, BucketType.user)
    async def gryphon(self, ctx):

        # Weapon drop needs to be made
        raven_dagger = find(lambda r: r.name == "✪ Raven's Dagger", ctx.message.guild.roles)

        feather = find(lambda r: r.name == "🕊️ Gryphon's Feather", ctx.message.guild.roles)
        claw = find(lambda r: r.name == "🐉 Gryphon's Claw", ctx.message.guild.roles)
        heart = find(lambda r: r.name == "❤️ Gryphon's Heart", ctx.message.guild.roles)
        azure_splitter = find(lambda r: r.name == "⚜️ Azure Splitter", ctx.message.guild.roles)
        logs = self.client.get_channel(873941431570546770)

        atkspeed = 1.5
        boss = NewBoss(
            name="Gryphon",
            desc="Temp Desc",
            health=10000,
            mindamage=300,
            maxdamage=475,
            loot=gryphon_loot,
        )
        # name, health, originalhealth, mindamage, maxdamage, agility
        player = Player(
            name=ctx.author.name,
            health=2500,
            originalhealth=2500,
            mindamage=150,
            maxdamage=300,
            agility=0,
        )

        if raven_dagger in ctx.author.roles:
            player.health += 2000
            player.originalhealth += 2000
            player.mindamage += 625
            player.maxdamage += 625

        elif azure_splitter in ctx.author.roles:
            player.health += 2500
            player.originalhealth += 2500
            player.mindamage += (player.mindamage + (player.mindamage * (10/100))) + 750
            player.maxdamage += (player.maxdamage + (player.maxdamage * (10/100))) + 750

        em = discord.Embed(
            title=boss.name,
            colour=discord.Colour.from_rgb(0, 208, 255)
        )
        em.add_field(name="Boss Health", value = f":heart: {boss.health:,}", inline=True)
        em.add_field(name="Player Health", value = f":heart: {player.health:,}", inline=True)
        em.add_field(name="Last Action", value="`Boss initiated.`", inline=False)
        em.add_field(name="Difficulty", value=":star:", inline=False)
        em.timestamp = datetime.utcnow()

        msg = await ctx.send(embed=em)

        '''
        Potion Work 
        '''

        # Boss loop
        while (boss.health > 0) and (player.health) > 0:

            await asyncio.sleep(atkspeed)

            player_dps = random.randint(player.mindamage, player.maxdamage)
            if player.health <= 0:
                player.health = 0
                player_dps = 0

            boss.health -= player_dps
            em2 = discord.Embed(
                title=boss.name,
                colour=discord.Colour.from_rgb(0, 208, 255)
            )
            em2.add_field(name="Boss HP",value=f":heart: {boss.health:,}",inline=True)
            em2.add_field(name="Player HP",value=f":heart: {player.health:,}",inline=True)
            em2.add_field(name="Last Action",value=f"> {ctx.author.name} dealt :crossed_swords: {player_dps:,}", inline=False)
            em2.timestamp = datetime.utcnow()
            await msg.edit(embed=em2)

            await asyncio.sleep(atkspeed)

            boss_dps = random.randint(boss.mindamage, boss.maxdamage)
            if boss.health <= 0:
                boss.health = 0
                boss_dps = 0

            player.health -= boss_dps
            em3 = discord.Embed(
                title=boss.name,
                colour=discord.Colour.from_rgb(0, 208, 255)
            )
            em3.add_field(name="Boss HP",value=f":heart: {boss.health:,}",inline=True)
            em3.add_field(name="Player HP",value=f":heart: {player.health:,}",inline=True)
            em3.add_field(name="Last Action",value=f"> {boss.name} dealt :crossed_swords: {boss_dps:,}", inline=False)
            em3.timestamp = datetime.utcnow()
            await msg.edit(embed=em3)

            # Boss has died
            if boss.health <= 0:

                boss.health = 0
                # Check if player is also dead
                if player.health <= 0:
                    #if boss.health <= 0:
                    #    boss.health = 0
                    player.health = 0
                    em = discord.Embed(title="Boss has defeated you.",description="You were weakened and had to flee the boss fight.",colour=discord.Colour.from_rgb(255, 95, 95))
                    em.timestamp = datetime.utcnow()
                    return await ctx.send(ctx.author.mention, embed=em)
                    # await ctx.author.remove_roles(keyreq)

                # Boss defeated
                else:

                    Economy = eco.find_one({"memberid":ctx.author.id})
                    kills = Economy["totalBossKills"]

                    eco.update_one({"memberid":ctx.author.id},{"$set":{"totalBossKills":kills+1}})

                    # LOOT
                    em = discord.Embed(title="Boss has fled.",description="You forced the boss to flee.",colour=discord.Colour.from_rgb(95, 255, 95))
                    
                    l1 = random.choice(boss.loot)
                    l2 = random.choice(boss.loot)
                    l3 = random.choice(boss.loot)

                    if l1 == ":feather: **Gryphon's Feather**" or l2 == ":feather: **Gryphon's Feather**" or l3 == ":feather: **Gryphon's Feather**":
                        await ctx.author.add_roles(feather)

                    if l1 == ":eagle: **Gryphon's Claw**" or l2 == ":eagle: **Gryphon's Claw**" or l3 == ":eagle: **Gryphon's Claw**":
                        await ctx.author.add_roles(claw)

                    if l1 == ":heart: **Gryphon's Heart**" or l2 == ":heart: **Gryphon's Heart**" or l3 == ":heart: **Gryphon's Heart**":
                        await ctx.author.add_roles(heart)
                    
                    em.add_field(name="Loot", value=f"> {l1}\n> {l2}\n> {l3}", inline=False)
                    em.timestamp = datetime.utcnow()

                    if quest_instance == False:
                        Economy = eco.find_one({"memberid":ctx.author.id})
                        boss_kills = Economy["totalBossKills"]
                        eco.update_one({"memberid":ctx.author.id},{"$set":{"totalBossKills":boss_kills+1}})

                    return await ctx.send(ctx.author.mention, embed=em)
                    # await ctx.author.remove_roles(keyreq)

            elif player.health <= 0:
                player.health = 0
                em = discord.Embed(title="You fled.",description="> You were overpowered and forced to flee, the boss escaped.", colour=discord.Colour.from_rgb(255, 95, 95))
                em.timestamp = datetime.utcnow()
                return await ctx.send(embed=em)
                # await ctx.author.remove_roles(keyreq)

def setup(client):
    client.add_cog(Boss(client))