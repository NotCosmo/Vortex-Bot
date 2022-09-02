# Main Imports

import nextcord as discord
import random
import asyncio
import time

# Other

from datetime import datetime
from nextcord import Interaction, SlashOption
from nextcord.ext import commands
from discord.ext.commands import BucketType
from discord.utils import find
from pymongo import MongoClient
from .utils.loot import dire_wolf_loot, selene_loot, paragon_loot
from .utils.weapons import *

# ------------------------------- #
''' Cluster '''
# ------------------------------- #

cluster = MongoClient(
    "mongodb+srv://Cosmo:1H1uqPGjo5CjtHQe@eco.5afje.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
database = cluster["Discord"]
users = database["Users"]
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

    def __init__(self, author_id, player, boss):
        self.player = player
        self.boss = boss
        self.author = author_id
        super().__init__()

    '''
    try:
        weapons = _inv["weapons"]
        if "Alpha Blade" not in weapons:
            weapons.append("Alpha Blade")
            inventory.update_one({"_id": i.user.id}, {"$set": {"weapons": weapons}})
    except:
        raise
    '''
    async def award_items(self, inv, loot, item, amount=1) -> None:

        if loot[0] == item:
            try:
                user_inventory = inv["inventory"]
                user_inventory[item] += amount
                inventory.update_one({'_id': self.author}, {"$set": {"inventory": user_inventory}})
            except:
                user_inventory = inv["inventory"]
                user_inventory[item] = amount # sets to 1 by default
                inventory.update_one({'_id': self.author}, {"$set": {"inventory": user_inventory}})

        if loot[1] == item:
            try:
                user_inventory = inv["inventory"]
                user_inventory[item] += amount
                inventory.update_one({'_id': self.author}, {"$set": {"inventory": user_inventory}})
            except:
                user_inventory = inv["inventory"]
                user_inventory[item] = amount # sets to 1 by default
                inventory.update_one({'_id': self.author}, {"$set": {"inventory": user_inventory}})

        if loot[2] == item:
            try:
                user_inventory = inv["inventory"]
                user_inventory[item] += amount
                inventory.update_one({'_id': self.author}, {"$set": {"inventory": user_inventory}})
            except:
                user_inventory = inv["inventory"]
                user_inventory[item] = amount # sets to 1 by default
                inventory.update_one({'_id': self.author}, {"$set": {"inventory": user_inventory}})

    async def award_weapon(self, inv, loot, weapon) -> None:

        if loot[0] == weapon:
            try:
                if weapon not in inv["weapons"]:
                    weapons_inv = inv["weapons"]
                    weapons_inv.append(weapon)
                    return inventory.update_one({'_id': self.author}, {"$set": {"weapons": weapons_inv}})
            except:
                raise

        elif loot[1] == weapon:
            try:
                if weapon not in inv["weapons"]:
                    weapons_inv = inv["weapons"]
                    weapons_inv.append(weapon)
                    return inventory.update_one({'_id': self.author}, {"$set": {"weapons": weapons_inv}})
            except:
                raise

        elif loot[2] == weapon:
            try:
                if weapon not in inv["weapons"]:
                    weapons_inv = inv["weapons"]
                    weapons_inv.append(weapon)
                    return inventory.update_one({'_id': self.author}, {"$set": {"weapons": weapons_inv}})
            except:
                raise

    @discord.ui.button(label="Attack️", style=discord.ButtonStyle.green)
    async def attack(self, button: discord.Button, i: discord.Interaction):
        await i.response.defer()
        if i.user.id != self.author:
            return

        if (self.boss.health > 0) and (self.player.health > 0):

            crit = False
            # crit chance
            if random.randint(0, 100) <= self.player.crit_chance:
                damage = int(self.player.damage * 1.75)
                crit = True
            else:
                damage = self.player.damage
            self.boss.health -= damage
            em = discord.Embed(title=self.boss.name, colour=discord.Colour.from_rgb(0, 208, 255))
            em.add_field(name="Boss HP", value=f":heart: {self.boss.health:,}", inline=True)
            em.add_field(name="<:transparent:911319446918955089>", value=":crossed_swords:", inline=True)
            em.add_field(name="Player HP", value=f":heart: {self.player.health:,}", inline=True)
            if crit:
                em.add_field(name="Last Action",value=f"> :exclamation: **CRIT** {i.user.name} dealt :crossed_swords: {damage:,}",inline=False)
            else:
                em.add_field(name="Last Action", value=f"> {i.user.name} dealt :crossed_swords: {damage:,}",inline=False)
            em.timestamp = datetime.utcnow()

            # Disable button
            button.disabled = True
            self.children[1].disabled = True
            button.style = discord.ButtonStyle.red
            await i.edit_original_message(embed=em, view=self)
            await asyncio.sleep(1.5)

            if self.player.health <= 0:
                self.player.health = 0
                button.disabled = False
                button.style = discord.ButtonStyle.green

                em = discord.Embed(title=f"{i.user.name} died.",description=f"You have been defeated by {self.boss.name}",colour=discord.Colour.from_rgb(0, 208, 255))
                em.timestamp = datetime.utcnow()
                return await i.send(embed=em, view=None)

            # check if boss is dead
            if not self.boss.health <= 0:

                damage = self.boss.damage
                self.player.health -= damage
                em = discord.Embed(title=self.boss.name, colour=discord.Colour.from_rgb(0, 208, 255))
                em.add_field(name="Boss HP", value=f":heart: {self.boss.health:,}", inline=True)
                em.add_field(name="<:transparent:911319446918955089>", value=":crossed_swords:", inline=True)
                em.add_field(name="Player HP", value=f":heart: {self.player.health:,}", inline=True)
                em.add_field(name="Last Action", value=f"> {self.boss.name} dealt :crossed_swords: {damage:,}", inline=False)
                em.timestamp = datetime.utcnow()

                # Enable button
                button.disabled = False
                self.children[1].disabled = False
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
                    embed = discord.Embed(title=f"{self.boss.name} defeated.", description=f"You have successfully defeated {self.boss.name}",colour=discord.Colour.from_rgb(0, 208, 255))
                    embed.add_field(name="Reward Bag", value=f"- {loot[0]}\n- {loot[1]}\n- {loot[2]}", inline=False)
                    embed.timestamp = datetime.utcnow()

                    _inv = inventory.find_one({"_id": i.user.id})
                    if self.boss.name == "🐺 Dire Wolf":
                        await self.award_weapon(inv=_inv, loot=loot, weapon="<:uncommon:992507268715262002> Eclipse")
                        await self.award_items(inv=_inv, loot=loot, item="<:common:992507237413167145> Wolf Mandible")
                        await self.award_items(inv=_inv, loot=loot, item="<:uncommon:992507268715262002> Dire Heart")
                    if self.boss.name == "🌙 Selene":
                        await self.award_weapon(inv=_inv, loot=loot, weapon="<:uncommon:992507268715262002> Crescent Scythe")
                        await self.award_items(inv=_inv, loot=loot, item="<:uncommon:992507268715262002> Pristine Gem")
                        await self.award_items(inv=_inv, loot=loot, item="<:common:992507237413167145> Moonstone")
                    if self.boss.name == "⛰️ Paragon":
                        await self.award_weapon(inv=_inv, loot=loot, weapon="<:epic:992507250595877005> Terra Scepter")
                        await self.award_items(inv=_inv, loot=loot, item="<:uncommon:992507268715262002> Earth Crystal")
                        await self.award_items(inv=_inv, loot=loot, item="<:common:992507237413167145> Ancient Fossil")

                    # Update boss kills then send embed
                    boss_kills = users.find_one({"_id": i.user.id})["boss_kills"]
                    users.update_one({"_id": i.user.id}, {"$set": {"boss_kills": boss_kills+1}})
                    await i.channel.send(f"{i.user.mention}", embed=embed)

            # Player died
            elif self.player.health <= 0:
                self.player.health = 0
                em = discord.Embed(title="You were forced to flee.",description=f"{self.boss.name} overpowered you and you were forced to flee.",colour=discord.Colour.from_rgb(0, 208, 255))
                em.timestamp = datetime.utcnow()
                return await i.send(embed=em, view=None)

    @discord.ui.button(label="Block", style=discord.ButtonStyle.blurple)
    async def block(self, button: discord.Button, i: discord.Interaction):

        await i.response.defer()
        if i.user.id != self.author:
            return

        chance = random.randint(0, 100)

        # check if boss and/or player is dead
        if (self.boss.health > 0) and (self.player.health > 0):

            # 25% Chance -> Full Block
            if chance <= 25:
                #self.player.health -= self.boss.damage
                em = discord.Embed(title=self.boss.name, colour=discord.Colour.from_rgb(0, 208, 255))
                em.add_field(name="Boss HP", value=f":heart: {self.boss.health:,}", inline=True)
                em.add_field(name="<:transparent:911319446918955089>", value=":crossed_swords:", inline=True)
                em.add_field(name="Player HP", value=f":heart: {self.player.health:,}", inline=True)
                em.add_field(name="Last Action", value=f"> :shield: **BLOCK** {i.user.name} blocked the attack!", inline=False)
                em.timestamp = datetime.utcnow()

                # Disable button
                button.disabled = True
                self.children[0].disabled = True
                button.style = discord.ButtonStyle.red
                await i.edit_original_message(embed=em, view=self)
                await asyncio.sleep(1.5)

                # Player attacks
                damage = self.player.damage
                self.boss.health -= damage
                em = discord.Embed(title=self.boss.name, colour=discord.Colour.from_rgb(0, 208, 255))
                em.add_field(name="Boss HP", value=f":heart: {self.boss.health:,}", inline=True)
                em.add_field(name="<:transparent:911319446918955089>", value=":crossed_swords:", inline=True)
                em.add_field(name="Player HP", value=f":heart: {self.player.health:,}", inline=True)
                em.add_field(name="Last Action", value=f"> {i.user.name} dealt :crossed_swords: {damage:,}", inline=False)
                em.timestamp = datetime.utcnow()

                # Check if boss died
                if self.boss.health <= 0:

                    # Player died
                    self.boss.health = 0
                    if self.player.health <= 0:
                        self.player.health = 0
                        em = discord.Embed(title="You were forced to flee.", description=f"{self.boss.name} overpowered you and you were forced to flee.", colour=discord.Colour.from_rgb(0, 208, 255))
                        em.timestamp = datetime.utcnow()
                        return await i.send(embed=em, view=None)

                    # Boss died
                    else:
                        loot = self.boss.loot
                        embed = discord.Embed(title=f"{self.boss.name} defeated.", description=f"You have successfully defeated {self.boss.name}", colour=discord.Colour.from_rgb(0, 208, 255))
                        embed.add_field(name="Reward Bag", value=f"- {loot[0]}\n- {loot[1]}\n- {loot[2]}", inline=False)
                        embed.timestamp = datetime.utcnow()

                        _inv = inventory.find_one({"_id": i.user.id})
                        if self.boss.name == "🐺 Dire Wolf":
                            await self.award_weapon(inv=_inv, loot=loot, weapon="<:uncommon:992507268715262002> Eclipse")
                            await self.award_items(inv=_inv, loot=loot, item="<:common:992507237413167145> Wolf Mandible")
                            await self.award_items(inv=_inv, loot=loot, item="<:uncommon:992507268715262002> Dire Heart")
                        if self.boss.name == "🌙 Selene":
                            await self.award_weapon(inv=_inv, loot=loot, weapon="<:uncommon:992507268715262002> Crescent Scythe")
                            await self.award_items(inv=_inv, loot=loot, item="<:uncommon:992507268715262002> Pristine Gem")
                            await self.award_items(inv=_inv, loot=loot, item="<:common:992507237413167145> Moonstone")
                        if self.boss.name == "⛰️ Paragon":
                            await self.award_weapon(inv=_inv, loot=loot, weapon="<:epic:992507250595877005> Terra Scepter")
                            await self.award_items(inv=_inv, loot=loot, item="<:uncommon:992507268715262002> Earth Crystal")
                            await self.award_items(inv=_inv, loot=loot, item="<:common:992507237413167145> Ancient Fossil")

                        boss_kills = users.find_one({"_id": i.user.id})["boss_kills"]
                        users.update_one({"_id": i.user.id}, {"$set": {"boss_kills": boss_kills + 1}})
                        await i.channel.send(f"{i.user.mention}", embed=embed)

                # Player died
                elif self.player.health <= 0:
                    self.player.health = 0
                    em = discord.Embed(title="You were forced to flee.", description=f"{self.boss.name} overpowered you and you were forced to flee.", colour=discord.Colour.from_rgb(0, 208, 255))
                    em.timestamp = datetime.utcnow()
                    return await i.send(embed=em, view=None)

                # Enable button
                button.disabled = False
                self.children[0].disabled = False
                button.style = discord.ButtonStyle.blurple
                await i.edit_original_message(embed=em, view=self)

            # 25% Chance -> Partial Block
            elif chance >= 25:
                block = [0.5, 0.51, 0.52, 0.53, 0.54, 0.55, 0.56, 0.57, 0.58, 0.59, 0.6, 0.61, 0.62, 0.63, 0.64, 0.65, 0.66, 0.67, 0.68, 0.69, 0.70]
                x = random.choice(block)
                damage = int(self.boss.damage * x)
                self.player.health -= damage
                em = discord.Embed(title=self.boss.name, colour=discord.Colour.from_rgb(0, 208, 255))
                em.add_field(name="Boss HP", value=f":heart: {self.boss.health:,}", inline=True)
                em.add_field(name="<:transparent:911319446918955089>", value=":crossed_swords:", inline=True)
                em.add_field(name="Player HP", value=f":heart: {self.player.health:,}", inline=True)
                em.add_field(name="Last Action", value=f"> :shield: **PARTIAL** {self.boss.name} dealt :crossed_swords: {damage:,} ({round(x*100,0)}%)", inline=False)
                em.timestamp = datetime.utcnow()

                # Disable button
                button.disabled = True
                self.children[0].disabled = True
                button.style = discord.ButtonStyle.red
                await i.edit_original_message(embed=em, view=self)
                await asyncio.sleep(1.5)

                if self.player.health <= 0:
                    self.player.health = 0
                    button.disabled = False
                    button.style = discord.ButtonStyle.green

                    em = discord.Embed(title=f"{i.user.name} died.", description=f"You have been defeated by {self.boss.name}", colour=discord.Colour.from_rgb(0, 208, 255))
                    em.timestamp = datetime.utcnow()
                    return await i.edit_original_message(embed=em, view=None)

                # Enable button
                button.disabled = False
                self.children[0].disabled = False
                button.style = discord.ButtonStyle.blurple
                await i.edit_original_message(embed=em, view=self)


    @discord.ui.button(label="🚪", style=discord.ButtonStyle.red)
    async def flee(self, button: discord.Button, i: discord.Interaction):

        await i.response.defer()
        if i.user.id != self.author:
            return

        em = discord.Embed(title="You fled.", description=f"{self.boss.name}'s power overwhelmed you.", colour=discord.Colour.from_rgb(0, 208, 255))
        em.timestamp = datetime.utcnow()
        await i.edit_original_message(embed=em, view=None)

# ------------------------------- #
''' Setup '''
# ------------------------------- #

class Boss(commands.Cog):

    def __init__(self, client):
        self.client = client

    # player stats (health)
    async def get_health(self, user: discord.Member) -> int:

        """
        Gets a users health
        :param user: discord.Member
        :return: int
        """

        base_health = 1250
        health = base_health
        user_accessories = inventory.find_one({"_id": user.id})["accessories"]

        if "<:uncommon:992507268715262002> Wolf Charm" in user_accessories:
            health += 500

        if "<:uncommon:992507268715262002> Lunar Guard" in user_accessories:
            health += 500

        return health

    @discord.slash_command(name="boss", description="Fight a boss", guild_ids=[581139467381768192])
    async def _boss(
            self,
            i: Interaction,
            boss: str = SlashOption(
                name="fight",
                description="Boss to fight",
                choices={
                    "🐺 The Dire Wolf, King of the Mountains.": "🐺 Dire Wolf",
                    "🌙 Selene, Priestess of the Moon.": "🌙 Selene",
                    "⛰️ Paragon, the Ancient Golem.": "⛰️ Paragon",
                }
            )
    ):

        if boss == "🐺 Dire Wolf":
            player_inv = inventory.find_one({"_id": i.user.id})
            weapon = WeaponInstance(player_inv["equipped"])
            player = PlayerInstance(
                name=i.user.name,
                health=await self.get_health(i.user),
                min=weapon.min_dmg,
                max=weapon.max_dmg,
                crit=weapon.crit_chance,
                agility=30
            )
            boss = BossInstance(
                name="🐺 Dire Wolf",
                health=1250,
                min=40,
                max=60,
                lt=dire_wolf_loot
            )

            # Create view
            view = Actions(i.user.id, player, boss)
            em = discord.Embed(title=boss.name, colour=discord.Colour.from_rgb(0, 208, 255))
            em.add_field(name="Boss HP", value=f":heart: {boss.health:,}", inline=True)
            em.add_field(name="Player HP", value=f":heart: {player.health:,}", inline=True)
            em.timestamp = datetime.utcnow()
            await i.response.send_message(embed=em, view=view)

        if boss == "🌙 Selene":

            # if user has the required role (975665560912273408)
            if True:

                player_inv = inventory.find_one({"_id": i.user.id})
                weapon = WeaponInstance(player_inv["equipped"])
                player = PlayerInstance(
                    name=i.user.name,
                    health=await self.get_health(i.user),
                    min=weapon.min_dmg,
                    max=weapon.max_dmg,
                    crit=weapon.crit_chance,
                    agility=30
                )
                boss = BossInstance(
                    name="🌙 Selene",
                    health=1750,
                    min=70,
                    max=90,
                    lt=selene_loot,
                )

                # Create view
                view = Actions(i.user.id, player, boss)
                em = discord.Embed(title=boss.name, colour=discord.Colour.from_rgb(0, 208, 255))
                em.add_field(name="Boss HP", value=f":heart: {boss.health:,}", inline=True)
                em.add_field(name="Player HP", value=f":heart: {player.health:,}", inline=True)
                em.timestamp = datetime.utcnow()
                await i.response.send_message(embed=em, view=view)
            else:
                await i.response.send_message("You require the **[V] Sentinel** to fight this boss.")

        if boss == "⛰️ Paragon":
            player_inv = inventory.find_one({"_id": i.user.id})
            weapon = WeaponInstance(player_inv["equipped"])
            player = PlayerInstance(
                name=i.user.name,
                health=await self.get_health(i.user),
                min=weapon.min_dmg,
                max=weapon.max_dmg,
                crit=weapon.crit_chance,
                agility=30
            )
            boss = BossInstance(
                name="⛰️ Paragon",
                health=2250,
                min=110,
                max=135,
                lt=paragon_loot,
            )

            # Create view
            view = Actions(i.user.id, player, boss)
            em = discord.Embed(title=boss.name, colour=discord.Colour.from_rgb(0, 208, 255))
            em.add_field(name="Boss HP", value=f":heart: {boss.health:,}", inline=True)
            em.add_field(name="Player HP", value=f":heart: {player.health:,}", inline=True)
            em.timestamp = datetime.utcnow()
            await i.response.send_message(embed=em, view=view)
    
    @commands.command(
        name="inventory",
        description="View your inventory",
        aliases=['inv']
    )
    async def inventory(self, ctx):

        # get user inventory
        _inv = inventory.find_one({"_id": ctx.author.id})
        user_inventory = _inv["inventory"]
        accessories = _inv["accessories"]

        # if user does not have an inventory
        if user_inventory is None:
            embed = discord.Embed(title=f"You do not have an inventory.", colour=discord.Colour.from_rgb(255, 75, 75))
            embed.timestamp = datetime.utcnow()
            return await ctx.send(embed=embed)
        else:
            embed = discord.Embed(description="", colour=discord.Colour.from_rgb(0, 208, 255))
            embed.description += "**Inventory**\n"
            for _item in user_inventory:
                # Ignore _id, weapons, selected weapon
                if _item in ["_id", "weapons", "selected_weapon"]: continue

                item = _item.replace("_", " ")
                # add item to embed
                embed.description += f"{user_inventory[_item]}x - {item}\n"

            embed.description += "\n**Accessories**\n"
            embed.description += "".join([f"{accessory}, " for accessory in accessories])
            await ctx.send(embed=embed)

    @commands.command(
        name="weapons",
        description="View your weapon inventory.",
    )
    async def weapons(self, ctx):

        # Get user inventory
        try:
            profile_name = users.find_one({"_id": ctx.author.id})['name']
            user = inventory.find_one({"_id": ctx.author.id})
            embed = discord.Embed(title=f"{profile_name}'s Weapons", colour=discord.Colour.from_rgb(0, 208, 255))
            embed.add_field(name="Equipped", value=f"{user['equipped']}\n<:transparent:911319446918955089>", inline=False)
            embed.add_field(name="All Weapons", value=" \n".join([weapon for weapon in user["weapons"]]), inline=False)
            embed.set_thumbnail(url=ctx.author.display_avatar)
            embed.timestamp = datetime.utcnow()
            await ctx.send(embed=embed)
        except:

            embed = discord.Embed(title="Inventory Error", description="You do not have a weapon inventory/", colour=discord.Colour.from_rgb(255, 75, 75))
            return await ctx.reply(embed=embed, mention_author=False)

    @commands.command(
        name="equip",
        description="Equip a weapon",
    )
    async def equip(self, ctx, *, weapon):

        # Get user inventory
        try:
            user = inventory.find_one({"_id": ctx.author.id})

            for _w in user["weapons"]:
                if weapon in _w:
                    inventory.update_one({"_id": ctx.author.id}, {"$set": {"equipped": _w}})
                    embed = discord.Embed(title=f"You have equipped {_w}.", colour=discord.Colour.from_rgb(0, 208, 255))
                    embed.timestamp = datetime.utcnow()
                    return await ctx.send(embed=embed)

            embed = discord.Embed(title=f"There is no weapon {weapon} in your inventory.", colour=discord.Colour.from_rgb(255, 75, 75))
            embed.timestamp = datetime.utcnow()
            return await ctx.send(embed=embed)
        except:
            embed = discord.Embed(title=f"You do not have an inventory.", colour=discord.Colour.from_rgb(255, 75, 75))
            embed.timestamp = datetime.utcnow()
            return await ctx.send(embed=embed)

    @commands.command(
        name="craft",
        description="Craft an item or accessory.",
    )
    async def craft(self, ctx, *, item: str = None):

        req = {
            "<:uncommon:992507268715262002> Wolf Charm": (35, "<:common:992507237413167145> Wolf Mandible", 5, "<:uncommon:992507268715262002> Dire Heart", "- Extra :heart: 500\n- :zap: 2x rank multi."),
            "<:uncommon:992507268715262002> Lunar Guard": (50, "<:common:992507237413167145> Moonstone", 10, "<:uncommon:992507268715262002> Pristine Gem", "- Extra :heart: 500\n- :zap: 2x rank multi."),
            "<:epic:992507250595877005> Nature's Blessing": (50, "<:common:992507237413167145> Ancient Fossil", 10, "<:uncommon:992507268715262002> Earth Crystal", ":zap: 3x rank multi."),
        }

        if item is None:
            embed = discord.Embed(title="Crafting Recipes", colour=discord.Colour.from_rgb(0, 208, 255))
            for recipe in req:
                embed.add_field(name=recipe, value=f"{req[recipe][4]}\n", inline=True)
            embed.timestamp = datetime.utcnow()
            return await ctx.send(embed=embed)

        try:
            data = inventory.find_one({"_id": ctx.author.id})
            inv = data["inventory"]
            accessories = data["accessories"]

            if item.title() not in accessories:

                for key in req.keys():
                    if item in key:
                        item_name = key
                        item = req[key]
                        break

                if item_name in accessories:
                    
                    embed = discord.Embed(title="Duplicate Error", description=f"You already own this item!", colour=discord.Colour.from_rgb(255, 75, 75))
                    embed.timestamp = datetime.utcnow()
                    return await ctx.send(embed=embed)

                material = item[1]
                material_amount = item[0]
                material_two = item[3]
                material_two_amount = item[2]

                if material in inv and inv[material] >= material_amount and material_two in inv and inv[material_two] >= material_two_amount:
                    inv[material] -= material_amount
                    inv[material_two] -= material_two_amount
                    inventory.update_one({"_id": ctx.author.id}, {"$set": {"inventory": inv}})
                    accessories.append(item_name)
                    inventory.update_one({"_id": ctx.author.id}, {"$set": {"accessories": accessories}})
                    embed = discord.Embed(title=f"Accessory Crafted", description=f"You have crafted {item_name}!\n\n**Materials:**\n{material_amount}x {material}\n {material_two_amount}x {material_two}", colour=discord.Colour.from_rgb(0, 208, 255))
                    embed.timestamp = datetime.utcnow()
                    await ctx.send(embed=embed)
                else:
                    # get required materials
                    try:
                        material_req = material_amount - inv[material]
                    except:
                        material_req = material_amount

                    try:
                        material_two_req = material_two_amount - inv[material_two]
                    except:
                        material_two_req = material_two_amount

                    desc = f"You do not have enough materials to craft {item_name}!\n\nMissing:\n"
                    if material_req > 0:
                        desc += f"{material_req}x {material}\n"
                    if material_two_req > 0:
                        desc += f"{material_two_req}x {material_two}\n"

                    desc += f"\n**Total Materias:**\n{material_amount}x {material}\n {material_two_amount}x {material_two}"
                    
                    embed = discord.Embed(title="Not enough materials!", description=desc, colour=discord.Colour.from_rgb(255, 75, 75))
                    embed.timestamp = datetime.utcnow()
                    await ctx.send(embed=embed)

            else:
                embed = discord.Embed(title="Duplicate Error", description=f"You already own this item!", colour=discord.Colour.from_rgb(255, 75, 75))
                embed.timestamp = datetime.utcnow()
                await ctx.send(embed=embed)

        except Exception as e:
            raise
            return await ctx.send(e)

    @commands.command(
        name="enhance",
        description="Enhance your weapon.",
        aliases=["en", "e"]
    )
    async def enhance(self, ctx, *, weapon=None):

        # req: {
        #   weapon_name (with tier): (material_amount, cost, material_name)
        # }
        req = {
            # Uncommon to Epic
            "<:uncommon:992507268715262002> Eclipse": (25, 200000, "<:common:992507237413167145> Wolf Mandible"),
            # Epic to Legendary
            "<:epic:992507250595877005> Eclipse": (25, 500000, "<:uncommon:992507268715262002> Dire Heart"),
            # Uncommon to Epic
            "<:uncommon:992507268715262002> Crescent Scythe": (50, 750000, "<:common:992507237413167145> Moonstone"),
            # Epic to Legendary
            "<:epic:992507250595877005> Crescent Scythe": (40, 1000000, "<:uncommon:992507268715262002> Pristine Gem"),
            "<:epic:992507250595877005> Terra Scepter": (50, 50000000, "<:uncommon:992507268715262002> Earth Crystal"),
        }

        if not weapon:
            return await ctx.send("What are you trying to enhance??")

        # Get user data
        try:
            user = users.find_one({"_id": ctx.author.id})
            user_inventory = inventory.find_one({"_id": ctx.author.id})
            weapons_inv = user_inventory["weapons"]
            material_inv = user_inventory["inventory"]

            for _ in weapons_inv:
                if weapon in _:
                    weapon = _
                    weapon_name = _
                    break

            if weapon in weapons_inv and weapon in req:

                weapon_instance = WeaponInstance(weapon)

                # GET UPGRADE REQUIREMENTS
                bal = user["balance"]
                material = req[weapon][2]
                material_amount = req[weapon][0]
                cost = req[weapon][1]

                if bal >= cost and material_inv[material] >= material_amount:

                    try:
                        weapon_instance.upgrade()
                    except Exception:
                        return await ctx.send("You cannot upgrade this weapon anymore!")

                    # Remove materials
                    material_inv[material] -= material_amount
                    inventory.update_one({"_id": ctx.author.id}, {"$set": {"inventory": material_inv}})
                    # Remove money
                    users.update_one({"_id":ctx.author.id}, {"$inc": {"balance": -cost}})
                    
                    weapons_inv.remove(weapon)
                    weapons_inv.append(weapon_instance.name)
                    inventory.update_one({"_id": ctx.author.id}, {"$set": {"weapons": weapons_inv}})
                    inventory.update_one({"_id": ctx.author.id}, {"$set": {"equipped": weapon_instance.name}})

                    embed = discord.Embed(title=f"Weapon Upgraded.", description=f"You have upgraded {weapon_name} to {weapon_instance.name}!\n\n**Materials**:\n{material_amount}x {material}\n:gem: {cost:,}", colour=discord.Colour.from_rgb(0, 208, 255))
                    embed.timestamp = datetime.utcnow()
                    await ctx.send(embed=embed)

                # Not enough materials
                else:
                    desc = f"You do not have enough materials to upgrade {weapon_name}.\n\n**Missing:**\n"

                    try:
                        material_req = material_amount - material_inv[material]
                    except:
                        material_req = material_amount
                    try:
                        bal_req = cost - bal
                    except:
                        bal_req = cost

                    if material_req > 0:
                        desc += f"{material_req}x {material}\n"
                    if bal_req > 0:
                        desc += f":gem: {bal_req:,}\n"

                    desc += f"\n**Total Materials:**\n{material_amount}x {material}\n:gem: {cost:,}"

                    embed = discord.Embed(title="Not enough materials!", description=desc, colour=discord.Colour.from_rgb(255, 75, 75))
                    embed.timestamp = datetime.utcnow()
                    return await ctx.send(embed=embed)

        except:
            raise

def setup(client):
    client.add_cog(Boss(client))