# Main Imports

import nextcord as discord
import random
import asyncio
import time

# Other

from datetime import datetime
from nextcord.ext import commands
from discord.ext.commands import BucketType
from discord.utils import find
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

class BossInstance:

    def __init__(self, name, health, min, max, lt):
        self.name = name
        self.health = health
        self.min_damage = min
        self.max_damage = max
        self.loot_table = []

        # Setup loot table with %-items
        for percent, item in lt:
            for i in range(0, percent):
                self.loot_table.append(item)

    @property
    def damage(self) -> int:
        return random.randint(self.min_damage, self.max_damage)

    @property
    def loot(self) -> list:
        l1 = random.choice(self.loot_table)
        l2 = random.choice(self.loot_table)
        l3 = random.choice(self.loot_table)
        return [l1, l2, l3]

class PlayerInstance:

    def __init__(self, name, health, min, max, crit, agility):
        self.name = name
        self.health = health
        self.min_damage = min
        self.max_damage = max
        self.crit_chance = crit
        self.agility = agility

    @property
    def damage(self) -> int:
        return random.randint(self.min_damage, self.max_damage)

# ------------------------------- #
#      MAIN BOSS VIEW             #
# ------------------------------- #

class Actions(discord.ui.View):

    def __init__(self, player, boss):
        self.player = player
        self.boss = boss
        super().__init__()

    @discord.ui.button(label="Attack", style=discord.ButtonStyle.green)
    async def attack(self, button: discord.Button, i: discord.Interaction):
        await i.response.defer()

        if (self.boss.health > 0) and (self.player.health > 0):

            crit = False
            # crit chance
            if random.randint(0, 100) <= self.player.crit_chance:
                damage = int(self.player.damage * 1.75)
                crit = True
            else:
                damage = self.player.damage
            self.boss.health -= damage
            em = discord.Embed(title=":hammer_pick: Bosses V3", colour=discord.Colour.from_rgb(0, 208, 255))
            em.add_field(name="Boss HP", value=f":heart: {self.boss.health:,}", inline=True)
            em.add_field(name="<:transparent:911319446918955089>", value=":crossed_swords:", inline=True)
            em.add_field(name="Player HP", value=f":heart: {self.player.health:,}", inline=True)
            if crit:
                em.add_field(name="Last Action", value=f"> :exclamation: **CRIT** {i.user.name} dealt :crossed_swords: {damage:,}", inline=False)
            else:
                em.add_field(name="Last Action",value=f"> {i.user.name} dealt :crossed_swords: {damage:,}",inline=False)
            em.timestamp = datetime.utcnow()

            # Disable button
            button.disabled = True
            button.style = discord.ButtonStyle.red
            await i.edit_original_message(embed=em, view=self)
            await asyncio.sleep(1.5)

            if self.boss.health <= 0:

                self.boss.health = 0
                if self.player.health <= 0:
                    self.player.health = 0
                    return await i.edit_original_message(content="Player died", view=None)
                else:

                    loot = self.boss.loot
                    em = discord.Embed(title=f"{self.boss.name} defeated.", description=f"You have successfully defeated {self.boss.name}", colour=discord.Colour.from_rgb(0, 208, 255))
                    em.add_field(name="Reward Bag", value=f"- {loot[0]}\n- {loot[1]}\n- {loot[2]}", inline=False)
                    em.timestamp = datetime.utcnow()
                    await i.edit_original_message(embed=em, view=None)

            elif self.player.health <= 0:
                self.player.health = 0
                button.disabled = False
                button.style = discord.ButtonStyle.green

                em = discord.Embed(title=f"{i.user.name} died.", description=f"You have been defeated by {self.boss.name}", colour=discord.Colour.from_rgb(0, 208, 255))
                em.timestamp = datetime.utcnow()
                return await i.edit_original_message(embed=em, view=None)

            damage = self.boss.damage
            self.player.health -= damage
            em = discord.Embed(title=":hammer_pick: Bosses V3", colour=discord.Colour.from_rgb(0, 208, 255))
            em.add_field(name="Boss HP", value=f":heart: {self.boss.health:,}", inline=True)
            em.add_field(name="<:transparent:911319446918955089>", value=":crossed_swords:", inline=True)
            em.add_field(name="Player HP", value=f":heart: {self.player.health:,}", inline=True)
            em.add_field(name="Last Action", value=f"> {self.boss.name} dealt :crossed_swords: {damage:,}", inline=False)
            em.timestamp = datetime.utcnow()

            # Enable button
            button.disabled = False
            button.style = discord.ButtonStyle.green
            await i.edit_original_message(embed=em, view=self)

            if self.boss.health <= 0:

                # Player died
                self.boss.health = 0
                if self.player.health <= 0:
                    self.player.health = 0
                    self.player.health = 0
                    em = discord.Embed(title="You were forced to flee.", description=f"{self.boss.name} overpowered you and you were forced to flee.", colour=discord.Colour.from_rgb(0, 208, 255))
                    em.timestamp = datetime.utcnow()
                    return await i.send(embed=em, view=None)

                # Boss died
                else:
                    loot = self.boss.loot
                    em = discord.Embed(title=f"{self.boss.name} defeated.", description=f"You have successfully defeated {self.boss.name}",colour=discord.Colour.from_rgb(0, 208, 255))
                    em.add_field(name="Reward Bag", value=f"- {loot[0]}\n- {loot[1]}\n- {loot[2]}", inline=False)
                    em.timestamp = datetime.utcnow()

                    inv = inventory.find_one({"_id": i.user.id})
                    if self.boss.name == ":wolf: Dire Wolf":

                        print("pass")
                        if loot[0] == "Alpha Blade" or loot[1] == "Alpha Blade" or loot[2] == "Alpha Blade":
                            weapons = inv["weapons"]
                            weapons.append("Alpha Blade")
                            inventory.update_one({"_id": i.user.id}, {"$set": {"weapons": weapons}})

                        if loot[0] == "Wolf Emblem" or loot[1] == "Wolf Emblem" or loot[2] == "Wolf Emblem":
                            try:
                                wolf_emblems = inv["wolf_emblem"] + 1
                                inventory.update_one({"_id": i.user.id}, {"$set": {"wolf_emblem": wolf_emblems}})
                            except:
                                raise
                                inventory.update({'_id': i.user.id}, {'$set': {'wolf_emblem': 0}})
                    return await i.send(embed=em, view=None)

            # Player died
            elif self.player.health <= 0:
                self.player.health = 0
                em = discord.Embed(title="You were forced to flee.", description=f"{self.boss.name} overpowered you and you were forced to flee.", colour=discord.Colour.from_rgb(0, 208, 255))
                em.timestamp = datetime.utcnow()
                return await i.send(embed=em, view=None)

    @discord.ui.button(label="Dodge", style=discord.ButtonStyle.blurple)
    async def dodge(self, button: discord.Button, i: discord.Interaction):

        await i.response.defer()

        button.disabled = True
        button.style = discord.ButtonStyle.red

        if (self.boss.health > 0) and (self.player.health > 0):
            dodge_chance = random.randint(1, 100)
            if dodge_chance in range(1, self.player.agility):
                em = discord.Embed(title=":hammer_pick: Bosses V3", colour=discord.Colour.from_rgb(0, 208, 255))
                em.add_field(name="Boss HP", value=f":heart: {self.boss.health:,}", inline=True)
                em.add_field(name="<:transparent:91131944691895589>", value=":crossed_swords:", inline=True)
                em.add_field(name="Player HP", value=f":heart: {self.player.health:,}", inline=True)
                em.add_field(name="Last Action", value=f"> :zap: **DODGE** {i.user.name} dodged the attack!\n`Waiting for your move..`", inline=False)
                em.timestamp = datetime.utcnow()
                await i.edit_original_message(embed=em, view=self)
                await asyncio.sleep(0.5)
                button.disabled = False
                button.style = discord.ButtonStyle.blurple
                await i.edit_original_message(embed=em, view=self)

            # player did NOT dodge
            else:
                damage = self.boss.damage
                self.player.health -= damage
                em = discord.Embed(title=":hammer_pick: Bosses V3", colour=discord.Colour.from_rgb(0, 208, 255))
                em.add_field(name="Boss HP", value=f":heart: {self.boss.health:,}", inline=True)
                em.add_field(name="<:transparent:911319446918955089>", value=":crossed_swords:", inline=True)
                em.add_field(name="Player HP", value=f":heart: {self.player.health:,}", inline=True)
                em.add_field(name="Last Action", value=f"> :zap: **MISS** {i.user.name} failed the dodge, {self.boss.name} dealt :crossed_swords: {damage:,}", inline=False)
                em.timestamp = datetime.utcnow()

                # Enable button
                button.disabled = False
                button.style = discord.ButtonStyle.blurple
                await i.edit_original_message(embed=em, view=self)

                if self.boss.health <= 0:

                    self.boss.health = 0
                    if self.player.health <= 0:
                        self.player.health = 0
                        return await i.edit_original_message(content="Player died", view=None)
                    else:
                        return await i.edit_original_message(content="boss died L bozo", view=None)

                elif self.player.health <= 0:
                    self.player.health = 0
                    return await i.edit_original_message(content="Player died", view=None)

# ------------------------------- #
''' Setup '''
# ------------------------------- #

class Boss(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(name="boss")
    async def boss(self, ctx):
        # Get player and boss
        player_inv = inventory.find_one({"_id": ctx.author.id})
        weapon = WeaponInstance(player_inv["selected_weapon"])

        # Get player and boss
        player = PlayerInstance(name=ctx.author.name, health=1200, min=weapon.min_dmg, max=weapon.max_dmg, crit=weapon.crit_chance, agility=30)
        boss = BossInstance(":wolf: Dire Wolf", 2750, 40, 80, [(5, "Alpha Blade"), (10, "Wolf Emblem"), (85, "No loot")])

        # Create view
        view = Actions(player, boss)
        em = discord.Embed(title=":hammer_pick: Bosses V3", colour=discord.Colour.from_rgb(0, 208, 255))
        em.add_field(name="Boss HP", value=f":heart: {boss.health:,}", inline=True)
        em.add_field(name="Player HP", value=f":heart: {player.health:,}", inline=True)
        em.timestamp = datetime.utcnow()
        await ctx.send(embed=em, view=view)

    @commands.command(name="loottest")
    async def loottest(self, ctx):

        # get user inventory
        # add field to user inventory in database
        inv = inventory.find_one({"_id": ctx.author.id})
        wolf_emblems = inv["wolf_emblem"] + 1
        inventory.update_one({"_id": i.user.id}, {"$set": {"wolf_emblem": wolf_emblems}})

    @commands.command(name="inventory")
    async def inventory(self, ctx):

        # get user inventory
        user_inventory = inventory.find_one({"_id":ctx.author.id})
        
        # if user does not have an inventory
        if user_inventory is None:
            embed = discord.Embed(title=f"You do not have an inventory.", colour=discord.Colour.from_rgb(255, 75, 75))
            embed.timestamp = datetime.utcnow()
            return await ctx.send(embed=embed)
        else:
            embed = discord.Embed(description="", colour=discord.Colour.from_rgb(0, 208, 255))
            for _item in user_inventory:
                # Ignore _id, weapons, selected weapon
                if _item in ["_id", "weapons", "selected_weapon"]: continue

                item = _item.replace("_", " ").title()
                # add item to embed
                embed.description += f"{user_inventory[_item]}x - {item}\n"
            
            await ctx.send(embed=embed)

    @commands.command(name="weapons")
    async def weapons(self, ctx):

        # Get user inventory
        try:
            user = inventory.find_one({"_id": ctx.author.id})
            embed = discord.Embed(title="Weapon Inventory", description="", colour=discord.Colour.from_rgb(0, 208, 255))
            for i in user["weapons"]:
                weapon = WeaponInstance(i)
                embed.add_field(name=weapon.name, value=f":crossed_swords: {weapon.min_dmg} - {weapon.max_dmg}\n:star: {weapon.crit_chance}%",inline=False)
            await ctx.send(embed=embed)
        except:
            await ctx.send("Created inventory.")
            return inventory.insert_one({
                "_id": ctx.author.id,
                "weapons": [],
                "selected_weapon": "None",
            })

    @commands.command(name="equip")
    async def equip(self, ctx, *, weapon):

        # Get user inventory
        try:
            user = inventory.find_one({"_id": ctx.author.id})
            if weapon in user["weapons"]:
                inventory.update_one({"_id": ctx.author.id}, {"$set": {"selected_weapon": weapon}})
                embed = discord.Embed(title=f"You have equipped {weapon}.", colour=discord.Colour.from_rgb(0, 208, 255))
                embed.timestamp = datetime.utcnow()
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(title=f"There is no weapon {weapon} in your inventory.", colour=discord.Colour.from_rgb(255, 75, 75))
                embed.timestamp = datetime.utcnow()
                return await ctx.send(embed=embed)
        except:
            embed = discord.Embed(title=f"You do not have an inventory.", colour=discord.Colour.from_rgb(255, 75, 75))
            embed.timestamp = datetime.utcnow()
            return await ctx.send(embed=embed)

    @commands.command(name="weaponstats", aliases=["ws", "loadout"])
    async def weaponstats(self, ctx):
        user = inventory.find_one({"_id": ctx.author.id})
        if user["selected_weapon"] == "None":
            embed = discord.Embed(title=f"You do not have any weapon currently equipped.", colour=discord.Colour.from_rgb(255, 75, 75))
            embed.timestamp = datetime.utcnow()
            return await ctx.send(embed=embed)

        embed = discord.Embed(colour=discord.Colour.from_rgb(0, 208, 255))
        weapon = WeaponInstance(user["selected_weapon"])
        embed.add_field(name=weapon.name, value=f":crossed_swords: {weapon.min_dmg} - {weapon.max_dmg}\n:star: {weapon.crit_chance}%",inline=False)
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Boss(client))