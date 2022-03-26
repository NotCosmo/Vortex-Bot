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
from .utils.loot import *
from .utils.weapons import WeaponInstance

quest_instance = False

# ------------------------------- #
''' Cluster '''
# ------------------------------- #

cluster = MongoClient("mongodb+srv://Cosmo:1H1uqPGjo5CjtHQe@eco.5afje.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
database = cluster["Discord"]
eco = database["Economy"]
inventory = database["Inventories"]

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
# ------------------------------- #!

class Boss(commands.Cog):

    def __init__(self, client):
        self.client = client

    MinionLoot = []


    @commands.command()
    @commands.has_permissions(administrator=True)
    async def dbt(self, ctx):
        
        inventory.update_one({"_id":ctx.author.id}, {"$set": {"selected_weapon":"None"}})
        await ctx.send("Done!")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def weapon(self, ctx, *, display_name: str):

        weapon = WeaponInstance(display_name)
        await ctx.send(f"{weapon.name}\n\n__**Min Dmg**__: {weapon.min_dmg}\n__**Max Dmg**__: {weapon.max_dmg}")
    
    @commands.command()
    async def boss_test(self, ctx):

        player = Player(name=ctx.author.name,health=500,originalhealth=500,mindamage=100,maxdamage=300,agility=15)
        boss = NewBoss(name="Starter Boss",desc=None,health=1000,mindamage=50,maxdamage=80,loot=[])

        em = discord.Embed(
            title=boss.name,
            colour=discord.Colour.from_rgb(0, 208, 255)
        )
        em.add_field(name="Boss Health", value = f":heart: {boss.health:,}", inline=True)
        em.add_field(name="Player Health", value = f":heart: {player.health:,}", inline=True)
        em.add_field(name="Last Action", value="`Boss initiated.`", inline=False)
        em.add_field(name="Difficulty", value=":star:", inline=False)
        em.timestamp = datetime.utcnow()

        actions = Button(player_health=player.health,player_agility=player.agility,player_min=player.mindamage,player_max=player.maxdamage,boss_min=boss.mindamage,boss_max=boss.maxdamage,boss_health=boss.health)
        msg = await ctx.send(embed=em, view=actions)

        while (boss.health > 0) and (player.health) > 0:

            await actions.wait()

            if actions.player_dead == False:
                pass
            else:
                return

    @commands.command(aliases=['inv'])
    async def inventory(self, ctx):

        try:
            data = inventory.find_one({"_id":ctx.author.id})
            em = discord.Embed(description='',colour=discord.Colour.from_rgb(0, 208, 255))

            for result in data:

                if str(result) == "_id":
                    continue
                    
                item = result.title().replace("_", "")
                em.description += f"{item} - `{data[result]}`x"

                em.description += "\n"
                em.description += "__**Weapons**__"
                em.description += " \n".join(data['weapons_inventory'])
            return await ctx.send(embed=em)
            
        except:
            return inventory.insert_one({
                "_id":ctx.author.id,
                "selected_weapon":"None",
                "weapons_inventory":[],
                
            })

    @commands.command()
    async def bossinfo(self, ctx, *, boss=None):

        if boss in ["serpent", "Serpent"]:
            em = discord.Embed(title=":fire: Blazing Serpent", description="> An ancient beast found within the volcanic region.", colour=discord.Colour.from_rgb(0, 208, 255))
            em.add_field(name="Loot",value="> [Common] Blazing Scales - 50%\n> [Rare] Flaming Fang - 35%\n> [Epic] Unrefined Venom - 10%\n> :star: [Legendary] Scorching Heart - 5%")
            em.timestamp = datetime.utcnow()
            await ctx.send(embed=em)

    @commands.group(invoke_without_command=True)
    @commands.cooldown(1, 1, BucketType.user)
    async def boss(self, ctx, *, bossName=None):

        em = discord.Embed(colour=discord.Colour.from_rgb(0, 208, 255))

        em.add_field(name="Minion",value="> Tutorial boss in order to get the first starter weapon.",inline=False)
        em.add_field(name="Raven's Follower",value="> Second boss, unlocks amulets and a new weapon.\n> `>bossinfo Follower` for more info.",inline=False)
        em.add_field(name="The Gryphon",value="> Higher level boss, drops are used in crafting a new powerful weapon.\n> `>bossinfo Gryphon` for more info.",inline=False)
        em.add_field(name="Ancient Wizard",value="> An ancient wizard with the power to travel between dimensions, used to craft the dimensional amulet.\n> `>bossinfo Wizard` for more info.",inline=False)
        em.add_field(name="Blazing Serpent",value="> An ancient beast found within the volcanic region.\n> `>bossinfo Serpent` for more info.",inline=False)
        em.timestamp = datetime.utcnow()
        em.set_author(name=ctx.author,icon_url=ctx.author.display_avatar)
        await ctx.send(embed=em)

    @boss.command(aliases = ["Serpent"])
    @commands.cooldown(1, 1, BucketType.user)
    async def serpent(self, ctx):

        # Weapon drop needs to be made
        azure_splitter = find(lambda r: r.name == "⚜️ Azure Splitter", ctx.message.guild.roles)
        legendary_count = 0
        mythic_count = 0

        atkspeed = 1.5
        boss = NewBoss(
            name=":fire: Blazing Serpent",
            desc="Temp Desc",
            health=18750,
            mindamage=650,
            maxdamage=775,
            loot=blazing_serpent_loot,
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

        # Reforged Splitter boost
        if find(lambda r: r.name == "⭐ Azure Splitter", ctx.message.guild.roles) in ctx.author.roles:
            player.health += 3000
            player.originalhealth += 3000
            player.mindamage += (player.mindamage + (player.mindamage * (10/100))) + 1250
            player.maxdamage += (player.maxdamage + (player.maxdamage * (10/100))) + 1250

            player.mindamage = int(player.mindamage + (player.mindamage * 15/100))
            player.maxdamage = int(player.maxdamage + (player.maxdamage * 15/100))
            player.health = int(player.health + (player.health * 15/100))

        elif azure_splitter in ctx.author.roles:
            player.health += 3000
            player.originalhealth += 3000
            player.mindamage += (player.mindamage + (player.mindamage * (10/100))) + 1250
            player.maxdamage += (player.maxdamage + (player.maxdamage * (10/100))) + 1250

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
            if boss.health <= 0 or boss.health == 0:

                boss.health = 0
                # Check if player is also dead
                if player.health <= 0:
                    #if boss.health <= 0:
                    #    boss.health = 0
                    player.health = 0
                    em = discord.Embed(title="Boss has defeated you.",description="You were weakened and had to flee the boss fight.",colour=discord.Colour.from_rgb(255, 95, 95))
                    em.timestamp = datetime.utcnow()
                    return await ctx.reply(embed=em)
                    # await ctx.author.remove_roles(keyreq)

                # Boss defeated
                else:
                    try:
                        inv = inventory.find_one({"memberid":ctx.author.id})

                    except:
                        inventory.insert_one({
                            "memberid":ctx.author.id,
                            "blazing_scales":0,
                            "flaming_fangs":0,
                            "unrefined_venom":0,
                            "scorching_hearts":0,
                            "ancient_fangs":0,
                            "dragons_breath":0,
                            "horn_of_hermes":0,
                            "archion_hearts":0,
                            "fractured_wings":0,
                            "serpent_essence":0,      
                        })

                    Economy = eco.find_one({"memberid":ctx.author.id})
                    #inv = inventory.find_one({"memberid":ctx.author.id})
                    blazing_scales = inv["blazing_scales"]
                    flaming_fangs = inv["flaming_fangs"]
                    venom = inv["unrefined_venom"]
                    scorching_hearts = inv["scorching_hearts"]
                    essence = inv["serpent_essence"]
                    kills = Economy["totalBossKills"]

                    eco.update_one({"memberid":ctx.author.id},{"$set":{"totalBossKills":kills+1}})

                    # LOOT
                    em = discord.Embed(title="Boss has fled.",description="You forced the boss to flee.",colour=discord.Colour.from_rgb(95, 255, 95))
                    
                    loot = []
                    for item, weight in boss.loot:
                        loot.extend([item]*weight)

                    l1 = random.choice(loot)
                    l2 = random.choice(loot)
                    l3 = random.choice(loot)

                    amt1 = 1
                    amt2 = 1
                    amt3 = 1

                    if l1.startswith("**COMMON**"):
                        amt1 = random.randint(1, 4)
                        blazing_scales += 1*amt1
                        inventory.update_one({"memberid":ctx.author.id},{"$set":{"blazing_scales":blazing_scales}})

                    elif l1.startswith("**RARE**"):
                        flaming_fangs += 1
                        inventory.update_one({"memberid":ctx.author.id},{"$set":{"flaming_fangs":flaming_fangs}})

                    elif l1.startswith("**EPIC**"):
                        venom += 1
                        inventory.update_one({"memberid":ctx.author.id},{"$set":{"flaming_fangs":venom}})

                    elif l1.startswith(":star:"):
                        scorching_hearts += 1
                        #inventory.update_one({"memberid":ctx.author.id},{"$set":{"scorching_hearts":scorching_hearts}})
                        legendary_count += 1

                    elif l1.startswith(":star2:"):
                        essence += 1
                        #inventory.update_one({"memberid":ctx.author.id},{"$set":{"scorching_hearts":scorching_hearts}})
                        mythic_count += 1

                    if l2.startswith("**COMMON**"):
                        amt2 = random.randint(1, 4)
                        blazing_scales += 1*amt2
                        inventory.update_one({"memberid":ctx.author.id},{"$set":{"blazing_scales":blazing_scales}})

                    elif l2.startswith("**RARE**"):
                        flaming_fangs += 1
                        inventory.update_one({"memberid":ctx.author.id},{"$set":{"flaming_fangs":flaming_fangs}})

                    elif l2.startswith("**EPIC**"):
                        venom += 1
                        inventory.update_one({"memberid":ctx.author.id},{"$set":{"unrefined_venom":venom}})

                    elif l2.startswith(":star:"):
                        scorching_hearts += 1
                        #inventory.update_one({"memberid":ctx.author.id},{"$set":{"scorching_hearts":scorching_hearts}})
                        legendary_count += 1

                    elif l2.startswith("***:star2:"):
                        essence += 1
                        #inventory.update_one({"memberid":ctx.author.id},{"$set":{"scorching_hearts":scorching_hearts}})
                        mythic_count += 1

                    if l3.startswith("**COMMON**"):
                        amt3 = random.randint(1, 4)
                        blazing_scales += 1*amt3
                        inventory.update_one({"memberid":ctx.author.id},{"$set":{"blazing_scales":blazing_scales}})

                    elif l3.startswith("**RARE**"):
                        flaming_fangs += 1
                        inventory.update_one({"memberid":ctx.author.id},{"$set":{"flaming_fangs":flaming_fangs}})

                    elif l3.startswith("**EPIC**"):
                        venom += 1
                        inventory.update_one({"memberid":ctx.author.id},{"$set":{"unrefined_venom":venom}})

                    elif l3.startswith(":star:"):
                        scorching_hearts += 1
                        #inventory.update_one({"memberid":ctx.author.id},{"$set":{"scorching_hearts":scorching_hearts}})
                        legendary_count += 1

                    elif l3.startswith("***:star2:"):
                        essence += 1
                        #inventory.update_one({"memberid":ctx.author.id},{"$set":{"scorching_hearts":scorching_hearts}})
                        mythic_count += 1

                    if legendary_count != 0:
                        embed = discord.Embed(title="Boss Drops",description=f"{ctx.author.mention} has dropped **{legendary_count}x** :star: **LEGENDARY Scorching Heart!**",colour=discord.Colour.from_rgb(255,215,0))
                        await self.client.get_channel(774847444617396234).send(embed=embed)
                        inventory.update_one({"memberid":ctx.author.id},{"$set":{"scorching_hearts":scorching_hearts}})

                    if mythic_count != 0:
                        embed = discord.Embed(title="Boss Drops",description=f"{ctx.author.mention} has dropped **{mythic_count}x** :star2: ***MYTHIC! Burning Essence***",colour=discord.Colour.from_rgb(0,0,0))
                        await ctx.send(embed=embed) #self.client.get_channel(774847444617396234).send(embed=embed)
                        inventory.update_one({"memberid":ctx.author.id},{"$set":{"serpent_essence":essence}})

                    em.add_field(name="Loot", value=f"> `{amt1}x` {l1}\n> `{amt2}x` {l2}\n> `{amt3}x` {l3}")
                    em.timestamp = datetime.utcnow()
                    await ctx.reply(embed=em)

            elif player.health <= 0:
                player.health = 0
                em = discord.Embed(title="You fled.",description="> You were overpowered and forced to flee, the boss escaped.", colour=discord.Colour.from_rgb(255, 95, 95))
                em.timestamp = datetime.utcnow()
                return await ctx.reply(embed=em)
                # await ctx.author.remove_roles(keyreq)

    @commands.command()
    async def trade(self, ctx, *, item, amt: int, member: discord.Member):

        scales = ["scorching scales", "Scorching Scales", "Scorching", "scorching", "scales"]

        if item in scales:

            author_inv = inventory.find_one({"memberid":ctx.author.id})
            member_inv = inventory.find_one({"memberid":member.id})

            author_scales = author_inv["blazing_scales"]
            m_inv = member_inv["blazing_scales"]

            if amt < author_scales:

                # make embed,
                # give item
                # update db values
                pass

def setup(client):
    client.add_cog(Boss(client))