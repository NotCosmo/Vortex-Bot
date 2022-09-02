## Main Imports

import nextcord as discord
import asyncio
import time
import math

# Other

from nextcord.ext import commands
from nextcord.ext.commands import BucketType
from nextcord.utils import find, get
from datetime import datetime
from pymongo import MongoClient
from random import choice, randint
from .utils.replies import workReplies, crimeReplies, slutReplies
from .utils.weapons import WeaponInstance
from pymongo.errors import DuplicateKeyError

# ------------------------------- #
''' Cluster '''
# ------------------------------- #

cluster = MongoClient("mongodb+srv://Cosmo:1H1uqPGjo5CjtHQe@eco.5afje.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
database = cluster["Discord"]
users = database["Users"]
collectdb = database["Collect"]
inventory = database["Inventories"]
settings = database["EcoSettings"]
titles = database["EcoTitles"]

def numformat(number):
    s = number
    if number < 1000:
        return number
    elif number < 1000000:
        s = "{:.2f}K".format(number / 1000)
    elif number < 1000000000:
        s = "{:.2f}M".format(number / 1000000)
    elif number < 1000000000000:
        s = "{:.2f}B".format(number / 1000000000)
    elif number < 1000000000000000:
        s = "{:.2f}T".format(number / 1000000000000)
    elif number < 1000000000000000000:
        s = "{:.2f}Qa".format(number / 1000000000000000)
    elif number < 1000000000000000000000:
        s = "{:.2f}Qi".format(number / 1000000000000000000)

    if ".00" in s:
        s = s.replace(".00", "")
    return s

# convert numbers like 10B into their actual number
def numconvert(number):

    # get last character
    if number[-1].lower() == "k":
        try:
            return int(number[:-1]) * 1000
        except:
            return int(float(number[:-1]) * 1000)
    if number[-1].lower() == "m":
        try:
            return int(number[:-1]) * 1000000
        except:
            return int(float(number[:-1]) * 1000000)
    if number[-1].lower() == "b":
        try:
            return int(number[:-1]) * 1000000000
        except:
            return int(float(number[:-1]) * 1000000000)
    if number[-1].lower() == "t":
        try:
            return int(number[:-1]) * 1000000000000
        except:
            return int(float(number[:-1]) * 1000000000000)

    if number[-1].lower() == "a":
        try:
            return int(number[:-1]) * 1000000000000000
        except:
            return int(float(number[:-1]) * 1000000000000000)
    if number[-1].lower() == "i":
        try:
            return int(number[:-1]) * 1000000000000000000
        except:
            return int(float(number[:-1]) * 1000000000000000000)

class EcoDrop(discord.ui.View):

    def __init__(self, host: int):
        super().__init__()
        self.winners = []
        self.host_id = host

    @discord.ui.button(
        label="Collect!", style=discord.ButtonStyle.green, custom_id="ecodrop:collect"
    )
    async def ecodrop(self, button: discord.ui.Button, i: discord.Interaction):

        if i.user.id != self.host_id:
            if i.user.id not in self.winners and len(self.winners) < 3:
                self.winners.append(i.user.id)
                await i.response.send_message("You have collected the drop!", ephemeral=True)

class Economy(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.users = users
        self.collect = collectdb
        self.settings = settings
        self.inv = inventory
        self.logs_id = 814787632776609812

    # get users
    async def get_users(self) -> None:

        '''
        Used in the leaderboard command, gets you a list of all user profiles
        :return:
        '''

        users_ = self.users.find()
        return users_

    # Get and return user object
    async def get_user(self, user: discord.Member) -> None:

        """
        Gets a user object (user profile) from the database
        :param user: discord.Member
        :return:
        """

        user = self.users.find_one({"_id": user.id})
        return user

    # Update user object
    async def update_user(self, user: discord.Member, data: str, new_data) -> None:

        """
        Updates a user object (user profile) in the database
        :param user: discord.Member
        :param data: str
        :param new_data: Any
        :return:
        """

        user_dict = await self.get_user(user)
        user_dict[data] = new_data
        return self.users.replace_one({"_id": user.id}, user_dict)

    # Update user bal
    async def update_bal(self, user_: discord.Member, amount: int) -> None:

        """
        Updates a users balance in the database
        :param user_: discord.Member
        :param amount: int
        :return:
        """

        user = await self.get_user(user_)
        user['balance'] += amount
        return self.users.replace_one({"_id": user_.id}, user)

    # Get and return settings object
    async def get_settings(self) -> None:

        """
        Gets a settings object from the database
        :return:
        """

        settings_ = self.settings.find_one({"_id": "settings"})
        return settings_

    async def set_setting(self, setting: str, value) -> None:

        """
        Updates a setting in the database
        :param setting: str
        :param value: Any
        :return:
        """

        settings_ = await self.get_settings()
        settings_[setting] = value
        return self.settings.replace_one({"_id": "settings"}, settings_)

    async def get_collect_amount(self, ctx):

        """
        Gets amount of money user has collected from ranks
        :param ctx: commands.Context
        :return: int
        """

        amount = 0
        collect_str = ""
        if get(ctx.guild.roles, name="[I] Apprentice") in ctx.author.roles:
            amount += 50000  # 50K
            collect_str += f"{get(ctx.guild.roles, name='[I] Apprentice').mention} - :gem: 50K\n"

        if get(ctx.guild.roles, name="[II] Warrior") in ctx.author.roles:
            amount += 100000  # 100K
            collect_str += f"{get(ctx.guild.roles, name='[II] Warrior').mention} - :gem: 100K\n"

        if get(ctx.guild.roles, name="[III] Paladin") in ctx.author.roles:
            amount += 250000  # 250K
            collect_str += f"{get(ctx.guild.roles, name='[III] Paladin').mention} - :gem: 250K\n"

        if get(ctx.guild.roles, name="[IV] Lord") in ctx.author.roles:
            amount += 500000  # 500K
            collect_str += f"{get(ctx.guild.roles, name='[IV] Lord').mention} - :gem: 500K\n"

        if get(ctx.guild.roles, name="[V] Sentinel") in ctx.author.roles:
            amount += 1000000  # 1M
            collect_str += f"{get(ctx.guild.roles, name='[V] Sentinel').mention} - :gem: 1M\n"

        if get(ctx.guild.roles, name="[VI] Conjurer") in ctx.author.roles:
            amount += 2000000  # 2M
            collect_str += f"{get(ctx.guild.roles, name='[VI] Conjurer').mention} - :gem: 2M\n"

        if get(ctx.guild.roles, name="[VII] Warlock") in ctx.author.roles:
            amount += 2500000  # 2.5M
            collect_str += f"{get(ctx.guild.roles, name='[VII] Warlock').mention} - :gem: 2.5M\n"

        if get(ctx.guild.roles, name="[VIII] Elder") in ctx.author.roles:
            amount += 3750000  # 3.75M
            collect_str += f"{get(ctx.guild.roles, name='[VIII] Elder').mention} - :gem: 3.75M\n"

        if get(ctx.guild.roles, name="[IX] Saint") in ctx.author.roles:
            amount += 4250000  # 4.25M
            collect_str += f"{get(ctx.guild.roles, name='[IX] Saint').mention} - :gem: 4.25M\n"

        if get(ctx.guild.roles, name="[X] Duck God") in ctx.author.roles:
            amount += 5000000  # 5M
            collect_str += f"{get(ctx.guild.roles, name='[X] Duck God').mention} - :gem: 5M\n"

        return (amount, collect_str)
        
    # Get and return rank multi
    async def get_rank_multi(self, ctx) -> int:

        """
        Gets users rank multi based on their ranks
        :param ctx: commands.Context
        :return: int
        """

        user_accessories = self.inv.find_one({"_id":ctx.author.id})["accessories"]
        
        rank_multi = 1
        if get(ctx.guild.roles, name="[I] Apprentice") in ctx.author.roles:
            rank_multi = 2.5
        if (get(ctx.guild.roles, name="[II] Warrior") in ctx.author.roles):
            rank_multi = 3
        if (get(ctx.guild.roles, name="[III] Paladin") in ctx.author.roles):
            rank_multi = 3.5
        if (get(ctx.guild.roles, name="[IV] Lord") in ctx.author.roles):
            rank_multi = 4
        if (get(ctx.guild.roles, name="[V] Sentinel") in ctx.author.roles):
            rank_multi = 5
        if (get(ctx.guild.roles, name="[VI] Conjurer") in ctx.author.roles):
            rank_multi = 6
        if (get(ctx.guild.roles, name="[VII] Warlock") in ctx.author.roles):
            rank_multi = 8
        if (get(ctx.guild.roles, name="[VIII] Elder") in ctx.author.roles):
            rank_multi = 10
        if (get(ctx.guild.roles, name="[IX] Saint") in ctx.author.roles):
            rank_multi = 12
        if (get(ctx.guild.roles, name="[X] Duck God") in ctx.author.roles):
            rank_multi = 15

        if "<:uncommon:992507268715262002> Wolf Charm" in user_accessories:
            rank_multi *= 2 # 2
        
        if "<:uncommon:992507268715262002> Lunar Guard" in user_accessories:
            rank_multi *= 2 # 3

        if "<:epic:992507250595877005> Nature's Blessing" in user_accessories:
            rank_multi *= 3 # 3
        
        return math.floor(rank_multi)

    # Amount to give user (based on multis)
    async def get_amount(self, user_: discord.Member, amount: int) -> int:

        """
        Calculates the amount to give a user (global multi & rank multi)
        :param user_: discord.Member
        :param amount: int
        :return: int
        """

        user = await self.get_user(user_)
        settings_ = await self.get_settings()
        user_accessories = self.inv.find_one({"_id":user_.id})["accessories"]

        m = int(amount * settings_["global_multiplier"])

        return m

    async def payout_multi(self, amount: int) -> int:

        """
        Payout multi
        :param amount: int
        :return:
        """

        settings_ = await self.get_settings()
        return int(amount * settings_["global_multiplier"])

    # convert numbers like 1e10 to ints
    async def convert_amount(self, donator, amount: str) -> int:

        """
        Converts amounts (1e10, 1k, 1M) into integers
        :param donator: user object (database)
        :param amount: str
        :return: int
        """

        if amount == "0":
            return 0

        if "e" in amount:
            _s = amount.split("e")
            amount = int(_s[0]) * (10 ** int(_s[1]))

        elif amount == "all":
            amount = donator["balance"]

        elif amount == "half":
            amount = int(donator["balance"] / 2)

        elif "," in amount:
            _s = amount.split(",")
            amt = ''
            for x in _s:
                amt += x
                amount = int(amt)

        else:
            try:
                amount = int(amount)
                if amount < 0:
                    return -1
            except:
                return numconvert(amount)

        return abs(amount)

    # Get and return user position
    async def get_position(self, user_: int) -> int:

        i = 1
        for data in self.users.find().sort("balance", -1):
            if data["_id"] == user_:
                return i
            i += 1

    # send eco logs to log channel
    async def send_log(self, user: discord.Member, title: str, desc: str) -> None:

        """
        Sends a log to the log channel
        :param user: discord.Member
        :param title: str
        :param desc: str
        :return:
        """

        log_channel = self.client.get_channel(975008852720353280)
        embed = discord.Embed(title=title, description=desc, colour=discord.Colour.from_rgb(0, 208, 255))
        embed.set_thumbnail(url=user.display_avatar)
        embed.timestamp = datetime.utcnow()
        return await log_channel.send(embed=embed)

    # player stats (health)
    async def get_health(self, ctx, user: discord.Member) -> int:

        """
        Gets a users health
        :param ctx: commands.Context
        :param user: discord.Member
        :return: int
        """

        base_health = 1250
        health = base_health
        user_accessories = self.inv.find_one({"_id": user.id})["accessories"]

        if "<:uncommon:992507268715262002> Wolf Charm" in user_accessories:
            health += 500

        if "<:uncommon:992507268715262002> Lunar Guard" in user_accessories:
            health += 500

        return health

    async def give_item(self, inv, item, amount=1) -> None:

        """
        Add an item to the users inventory.
        :param inv: User Profile
        :param item: Item to add
        :param amount: Amount of items to add
        :return: None
        """

        try:
            user_inventory = inv["inventory"]
            user_inventory[item] += amount
            inventory.update_one({'_id': inv['_id']}, {"$set": {"inventory": user_inventory}})
        except:
            user_inventory = inv["inventory"]
            user_inventory[item] = amount  # sets to 1 by default
            inventory.update_one({'_id': inv['_id']}, {"$set": {"inventory": user_inventory}})

    async def give_weapon(self, inv, weapon) -> None:

        """
        Add a weapon to the users inventory.
        :param inv: User Profile
        :param weapon: Weapon to award
        :return: None
        """

        try:
            if weapon not in inv["weapons"]:
                weapons_inv = inv["weapons"]
                weapons_inv.append(weapon)
                return inventory.update_one({'_id': inv['_id']}, {"$set": {"weapons": weapons_inv}})
        except:
            raise
    
    @commands.command(
        name="loadout",
        help="Shows your current loadout and main stats, or another user's if specified."
    )
    async def loadout(self, ctx, *, user: discord.Member = None):

        if not user:
            user = ctx.author

        profile = self.inv.find_one({"_id": user.id})
        profile_ = await self.get_user(user)
        if not profile:
            return await ctx.send("User not found.")

        weapon = WeaponInstance(profile["equipped"])
        embed = discord.Embed(title=f"{profile_['name']}'s Loadout", colour=discord.Colour.from_rgb(0, 208, 255))
        embed.description = f"Leaderboard Position: `{await self.get_position(profile['_id'])}/{self.users.count_documents({})}`\nRank Multiplier: `{await self.get_rank_multi(ctx, )}x`\nBoss Kills: `{profile_['boss_kills']}`\n\n"
        embed.add_field(name=f"Weapon Stats",
                        value=f"- {profile['equipped']}\n> Damage :crossed_swords: {weapon.min_dmg} - {weapon.max_dmg}\n> Crit Chance :star: {weapon.crit_chance}%\nHealth: :heart: {await self.get_health(ctx, ctx.author)}")
        embed.set_thumbnail(url=user.display_avatar)
        embed.timestamp = datetime.utcnow()
        await ctx.send(embed=embed)

    @commands.command(
        name="bal", aliases=["balance"],
        help="Check your balance or someone else's balance.",
    )
    async def bal(self, ctx, user: discord.Member = None):

        if user is None:
            user = ctx.author

        data = await self.get_user(user)
        settings_ = await self.get_settings()
        if data is None:
            return await ctx.send(f"{user.mention} has no account.")

        bal = data["balance"]
        embed = discord.Embed(colour=discord.Colour.from_rgb(0, 208, 255))
        embed.add_field(name=f"Balance", value=f"{settings_['currency']} {numformat(bal)}")
        embed.set_author(name=user.display_name, icon_url=user.display_avatar)
        embed.set_footer(text=f'Leaderboard Position #{await self.get_position(ctx.author.id)}')
        embed.timestamp = datetime.utcnow()
        return await ctx.send(embed=embed)

    @commands.command(
        name="newbal",
    )
    async def nbal(self, ctx):

        profile = await self.get_user(ctx.author)
        title_data = titles.find_one({"_id": ctx.author.id})
        data = await self.get_user(ctx.author)

        """
        if title_data is not None:
            title_text = f"{title_data['title_equipped']} {data['name']}"
        else:
            title_text = f"{data['name']}"
        """
        
        settings_ = await self.get_settings()
        if data is None:
            return await ctx.send(f"{ctx.author.mention} has no account.")

        embed = discord.Embed(colour=discord.Colour.from_rgb(0, 208, 255))
        embed.add_field(name=f"Balance", value=f"{settings_['currency']} {numformat(data['balance'])}")
        embed.add_field(name="Titles", value=f"{' ,'.join([title for title in title_data['titles']])}")
        embed.set_thumbnail(url=ctx.author.display_avatar)
        embed.set_footer(text='Leaderboard Position : #1')
        embed.timestamp = datetime.utcnow()
        return await ctx.send(embed=embed)

    @commands.command(
        name="profilerename",
        help="Rename your profile!",
        aliases=["rename"]
    )
    async def rename(self, ctx, *, profile_name: str = None):

        if not profile_name:
            embed = discord.Embed(description=":warning: You need to specify a profile name.", colour=discord.Colour.from_rgb(255, 75, 75))
            embed.timestamp = datetime.utcnow()
            return await ctx.send(embed=embed)

        if len(profile_name) > 24:
            embed = discord.Embed(description=":warning: Profile name is too long, please pick a name between 3 and 24 characters.", colour=discord.Colour.from_rgb(255, 75, 75))
            embed.timestamp = datetime.utcnow()
            return await ctx.send(embed=embed)

        if len(profile_name) < 3:
            embed = discord.Embed(description=":warning: Profile name is too short, please pick a name between 3 and 24 characters.", colour=discord.Colour.from_rgb(255, 75, 75))
            embed.timestamp = datetime.utcnow()
            return await ctx.send(embed=embed)

        if self.users.find_one({"name": profile_name}):
            embed = discord.Embed(description=":warning: Profile already exists.", colour=discord.Colour.from_rgb(255, 75, 75))
            embed.timestamp = datetime.utcnow()
            return await ctx.send(embed=embed)

        else:

            try:
                self.users.update_one({'_id': ctx.author.id}, {"$set": {"name": profile_name}})
                embed = discord.Embed(description=f":white_check_mark: Your profile has been renamed to {profile_name}", colour=discord.Colour.from_rgb(75, 255, 75))
                embed.timestamp = datetime.utcnow()
                return await ctx.send(embed=embed)
                
            except:
                embed = discord.Embed(description=":warning: You do not have a profile to rename.", colour=discord.Colour.from_rgb(255, 75, 75))
                embed.timestamp = datetime.utcnow()
                return await ctx.send(embed=embed)

    @commands.command(
        name="start",
        help="Create a profile to play Economy on!"
    )
    async def start(self, ctx, *, profile_name: str = None):

        if not profile_name:
            # create an embed saying they need to specify a profile name
            embed = discord.Embed(description=":warning: You need to specify a profile name.", colour=discord.Colour.from_rgb(255, 75, 75))
            embed.timestamp = datetime.utcnow()
            return await ctx.send(embed=embed)

        # check if the profile name is valid (check if profile name is longer than 16 characters)
        if len(profile_name) > 24:
            embed = discord.Embed(description=":warning: Profile name is too long, please pick a name between 3 and 24 characters.", colour=discord.Colour.from_rgb(255, 75, 75))
            embed.timestamp = datetime.utcnow()
            return await ctx.send(embed=embed)

        if len(profile_name) < 3:
            embed = discord.Embed(description=":warning: Profile name is too short, please pick a name between 3 and 24 characters.", colour=discord.Colour.from_rgb(255, 75, 75))
            embed.timestamp = datetime.utcnow()
            return await ctx.send(embed=embed)

        if self.users.count_documents({"_id": ctx.author.id}) == 0:

            # if profile name already exists
            if self.users.find_one({"name": profile_name}):
                embed = discord.Embed(description=":warning: Profile already exists.", colour=discord.Colour.from_rgb(255, 75, 75))
                embed.timestamp = datetime.utcnow()
                return await ctx.send(embed=embed)

            profile_no = self.users.count_documents({}) + 1

            try:
                self.users.insert_one({"_id": ctx.author.id, "name": profile_name, "balance": 0, "boss_kills": 0, "can_collect_in": 0, "cf_winstreak": 0, "profile_number": profile_no, "banned": False})
                self.inv.insert_one({"_id": ctx.author.id, "inventory": {}, "weapons": ["Fists"], "accessories": [], "equipped": "Fists"})
            # User already has an account
            except DuplicateKeyError:
                embed = discord.Embed(description=":warning: You already have an account.", colour=discord.Colour.from_rgb(255, 75, 75))
                embed.timestamp = datetime.utcnow()
                return await ctx.send(embed=embed)

            em = discord.Embed(description=f"Welcome to Economy V2 **{profile_name}**! (Profile #{profile_no})", colour=discord.Colour.from_rgb(0, 208, 255))
            em.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar)
            em.timestamp = datetime.utcnow()

            # Send account creation log
            await self.send_log(ctx.author, "New Profile", f"{ctx.author.mention} has created a profile with the name **{profile_name}**. (Profile #{profile_no})")
            return await ctx.send(embed=em)

        # user already has a profile
        else:
            embed = discord.Embed(description=":warning: You already have an account.", colour=discord.Colour.from_rgb(255, 75, 75))
            embed.timestamp = datetime.utcnow()
            return await ctx.send(embed=embed)

    @commands.command(
        name="work", aliases=["job"],
        help="Work a random job and make money, who doesn't love that!",
    )
    @commands.cooldown(1, 10, BucketType.user)
    async def work(self, ctx):
        try:
            user = await self.get_user(ctx.author)

            settings_ = await self.get_settings()
            if user["banned"] is False and settings_["work_disabled"] is False:

                multi = await self.get_rank_multi(ctx)
                amount = int(await self.get_amount(ctx.author, randint(settings_["work_min"], settings_["work_max"])) * multi)
                reply = choice(workReplies).replace("{}", f"{settings_['currency']} {numformat(amount)}")

                embed = discord.Embed(description=reply, colour=discord.Colour.from_rgb(0, 208, 255))
                embed.timestamp = datetime.utcnow()
                embed.set_author(name="Work", icon_url=ctx.author.display_avatar)
                embed.set_footer(text=f"Multiplier: x{multi}")

                await self.update_bal(ctx.author, amount)
                await ctx.send(embed=embed)
            else:
                if user["banned"]:
                    em = discord.Embed(description=":warning: You are banned from playing economy.", colour=discord.Colour.from_rgb(255, 75, 75))
                    em.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar)
                    em.timestamp = datetime.utcnow()
                    return await ctx.send(embed=em)

                em = discord.Embed(description=":warning: This command is currently disabled.",
                                   colour=discord.Colour.from_rgb(255, 75, 75))
                em.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar)
                em.timestamp = datetime.utcnow()
                return await ctx.send(embed=em)

        except TypeError:
            em = discord.Embed(
                description=":exclamation: You need an account to play eco. Type `!start` to create one.",
                colour=discord.Colour.from_rgb(0, 208, 255))
            em.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar)
            em.timestamp = datetime.utcnow()
            return await ctx.send(embed=em)

    @commands.command(
        name="crime", aliases=["rob"],
        help="Commit a dangerous crime for money!"
    )
    @commands.cooldown(1, 10, BucketType.user)
    async def crime(self, ctx):
        try:
            user = await self.get_user(ctx.author)

            settings_ = await self.get_settings()
            if user["banned"] is False and settings_["crime_disabled"] is False:

                multi = await self.get_rank_multi(ctx)
                amount = int(await self.get_amount(ctx.author, randint(settings_["work_min"], settings_["work_max"])) * multi)
                reply = choice(crimeReplies).replace("{}", f"{settings_['currency']} {numformat(amount)}")

                embed = discord.Embed(description=reply, colour=discord.Colour.from_rgb(0, 208, 255))
                embed.timestamp = datetime.utcnow()
                embed.set_author(name="Crime", icon_url=ctx.author.display_avatar)
                embed.set_footer(text=f"Multiplier: x{multi}")

                await self.update_bal(ctx.author, amount)
                await ctx.send(embed=embed)
            else:
                if user["banned"]:
                    em = discord.Embed(description=":warning: You are banned from playing economy.", colour=discord.Colour.from_rgb(255, 75, 75))
                    em.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar)
                    em.timestamp = datetime.utcnow()
                    return await ctx.send(embed=em)

                em = discord.Embed(description=":warning: This command is currently disabled.",
                                   colour=discord.Colour.from_rgb(255, 75, 75))
                em.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar)
                em.timestamp = datetime.utcnow()
                return await ctx.send(embed=em)

        except TypeError:
            em = discord.Embed(
                description=":exclamation: You need an account to play eco. Type `!start` to create one.",
                colour=discord.Colour.from_rgb(0, 208, 255))
            em.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar)
            em.timestamp = datetime.utcnow()
            return await ctx.send(embed=em)

    @commands.command(
        name="slut",
        help="Become a slut for money!"
    )
    @commands.cooldown(1, 10, BucketType.user)
    async def slut(self, ctx):
        try:
            user = await self.get_user(ctx.author)

            settings_ = await self.get_settings()
            if user["banned"] is False and settings_["slut_disabled"] is False:

                multi = await self.get_rank_multi(ctx)
                amount = int(await self.get_amount(ctx.author, randint(settings_["work_min"], settings_["work_max"])) * multi)
                reply = choice(slutReplies).replace("{}", f"{settings_['currency']} {numformat(amount)}")

                embed = discord.Embed(description=reply, colour=discord.Colour.from_rgb(0, 208, 255))
                embed.timestamp = datetime.utcnow()
                embed.set_author(name="Slut", icon_url=ctx.author.display_avatar)
                embed.set_footer(text=f"Multiplier: x{multi}")

                await self.update_bal(ctx.author, amount)
                await ctx.send(embed=embed)
            else:
                if user["banned"]:
                    em = discord.Embed(description=":warning: You are banned from playing economy.",
                                       colour=discord.Colour.from_rgb(255, 75, 75))
                    em.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar)
                    em.timestamp = datetime.utcnow()
                    return await ctx.send(embed=em)

                em = discord.Embed(description=":warning: This command is currently disabled.",
                                   colour=discord.Colour.from_rgb(255, 75, 75))
                em.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar)
                em.timestamp = datetime.utcnow()
                return await ctx.send(embed=em)

        except TypeError:
            em = discord.Embed(
                description=":exclamation: You need an account to play eco. Type `!start` to create one.",
                colour=discord.Colour.from_rgb(0, 208, 255))
            em.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar)
            em.timestamp = datetime.utcnow()
            return await ctx.send(embed=em)

    @commands.command(
        name="givemoney", aliases=["give", "givemoneyto", "transfer", "pay"],
        help="Give money to another user.",
    )
    async def givemoney(self, ctx, user: discord.Member, amount: str):

        if user.id == ctx.author.id:
            em = discord.Embed(description=":warning: You can't give money to yourself.",
                               colour=discord.Colour.from_rgb(255, 75, 75))
            em.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar)
            em.timestamp = datetime.utcnow()
            return await ctx.send(embed=em)

        try:
            donator = await self.get_user(ctx.author)
            receiver = await self.get_user(user)
            settings_ = await self.get_settings()

            amount = await self.convert_amount(donator, amount)

            if donator["banned"] is False and receiver["banned"] is False:

                if amount == -1:
                    em = discord.Embed(description=":warning: You can't give negative money.",
                                       colour=discord.Colour.from_rgb(255, 75, 75))
                    em.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar)
                    em.timestamp = datetime.utcnow()
                    return await ctx.send(embed=em)

                elif amount <= donator["balance"]:
                    await self.update_bal(ctx.author, -amount)
                    await self.update_bal(user, amount)
                    embed = discord.Embed(
                        description=f"Gave {user.mention} {settings_['currency']} {numformat(amount)}",
                        colour=discord.Colour.from_rgb(0, 208, 255))
                    embed.timestamp = datetime.utcnow()
                    embed.set_author(name="Give Money", icon_url=ctx.author.display_avatar)
                    await ctx.send(embed=embed)

                else:
                    em = discord.Embed(description=":warning: You don't have enough money.",
                                       colour=discord.Colour.from_rgb(255, 75, 75))
                    em.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar)
                    em.timestamp = datetime.utcnow()
                    return await ctx.send(embed=em)

            else:
                if donator["banned"] or receiver["banned"]:
                    em = discord.Embed(
                        description=":warning: Either you or the person you are giving money to is banned from playing economy.",
                        colour=discord.Colour.from_rgb(255, 75, 75))
                    em.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar)
                    em.timestamp = datetime.utcnow()
                    return await ctx.send(embed=em)

        except:
            em = discord.Embed(
                description=":warning: Error occurred, please check if both users have an account and try again.",
                colour=discord.Colour.from_rgb(255, 75, 75))
            em.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar)
            em.timestamp = datetime.utcnow()
            return await ctx.send(embed=em)

    # make a leaderboard command that sorts by balance and displays the top 10
    @commands.command(
        name="leaderboard", aliases=["lb"],
        help="Shows the top 10 richest users in the economy."
    )
    async def leaderboard(self, ctx):

        embed = discord.Embed(title=f"{ctx.guild.name} Leaderboard", colour=discord.Colour.from_rgb(0, 208, 255))
        st = await self.get_settings()
        i = 1

        for data in self.users.find().sort("balance", -1):
            if data["banned"] is False:
                # fetch user object
                user = await self.client.fetch_user(data["_id"])
                if i == 10:
                    embed.add_field(name=f"**{i}**. {data['name']} ({str(user)})", value=f"> {st['currency']} {data['balance']:,} ({st['currency']} {numformat(data['balance'])})", inline=False)
                elif i == 1:
                    embed.add_field(name=f"**{i}**. :star: {data['name']} ({str(user)})", value=f"> {st['currency']} {data['balance']:,} ({st['currency']} {numformat(data['balance'])})\n<:transparent:911319446918955089>", inline=True)

                else:
                    embed.add_field(name=f"**{i}**. {data['name']} ({str(user)})", value=f"> {st['currency']} {data['balance']:,} ({st['currency']} {numformat(data['balance'])})\n<:transparent:911319446918955089>", inline=False)
                i += 1
                if i == 11:
                    break

        embed.description = f"Gems can be used to buy new ranks in the shop, as well as upgrade your items."
        embed.set_footer(text=f"Position: {await self.get_position(ctx.author.id)}/{self.users.count_documents({})}")
        embed.set_thumbnail(url=ctx.guild.icon.url)
        await ctx.send(embed=embed)

    @commands.command(
        name="collect",
        help="Collect your rank income."
    )
    async def collect(self, ctx):

        user = await self.get_user(ctx.author)
        banned = user["banned"]
        st = await self.get_settings()

        if banned is False:

            can_collect_in = user["can_collect_in"]

            # First time collecting
            if can_collect_in == 0:

                data = await self.get_collect_amount(ctx)
                amount = data[0]
                string = data[1]
                if amount == 0:
                    embed = discord.Embed(title="Income Error", description="You don't have anything to collect yet!", colour=discord.Colour.from_rgb(255, 75, 75))
                    embed.timestamp = datetime.utcnow()
                    return await ctx.send(embed=embed)

                await self.update_bal(ctx.author, amount)
                self.users.update_one({"_id": ctx.author.id}, {"$set": {"can_collect_in": int(datetime.now().timestamp() + 21600)}})
                embed = discord.Embed(title="Income Collected", description=f"{string}\n**Total** {st['currency']} {numformat(amount)}", colour=discord.Colour.from_rgb(0, 208, 255))
                embed.timestamp = datetime.utcnow()
                return await ctx.send(embed=embed)

            # User can collect
            if can_collect_in <= int(datetime.now().timestamp()):

                data = await self.get_collect_amount(ctx)
                amount = data[0]
                string = data[1]
                if amount == 0:
                    embed = discord.Embed(title="Income Error", description="You don't have anything to collect yet!", colour=discord.Colour.from_rgb(255, 75, 75))
                    embed.timestamp = datetime.utcnow()
                    return await ctx.send(embed=embed)

                await self.update_bal(ctx.author, amount)
                self.users.update_one({"_id": ctx.author.id}, {"$set": {"can_collect_in": int(datetime.now().timestamp() + 21600)}})
                embed = discord.Embed(title="Income Collected", description=f"{string}\n**Total** {st['currency']} {numformat(amount)}", colour=discord.Colour.from_rgb(0, 208, 255))
                embed.timestamp = datetime.utcnow()
                return await ctx.send(embed=embed)

            # User cannot collect
            else:
                embed = discord.Embed(title="Cooldown", description=f"You can only collect in <t:{int(can_collect_in)}:R>", colour=discord.Colour.from_rgb(0, 208, 255))
                embed.timestamp = datetime.utcnow()
                return await ctx.send(embed=embed)

        else:
            em = discord.Embed(
                description=":warning: You are banned from playing economy.",
                colour=discord.Colour.from_rgb(255, 75, 75))
            em.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar)
            em.timestamp = datetime.utcnow()
            return await ctx.send(embed=em)
    
    @commands.command(
        name="stats", aliases=["playerstats"],
        help="Shows your command payouts, or someone else's command payouts if you specify someone else.",
    )
    async def stats(self, ctx, *, user: discord.Member = None):
        if not user:
            user = ctx.author

        st = await self.get_settings()
        currency = st['currency']
        profile = await self.get_user(user)

        # work out payouts
        work_min = st["work_min"] * st["global_multiplier"] * await self.get_rank_multi(ctx)
        work_max = st["work_max"] * st["global_multiplier"] * await self.get_rank_multi(ctx)
        slut_min = st["slut_min"] * st["global_multiplier"] * await self.get_rank_multi(ctx)
        slut_max = st["slut_max"] * st["global_multiplier"] * await self.get_rank_multi(ctx)
        crime_min = st["crime_min"] * st["global_multiplier"] * await self.get_rank_multi(ctx)
        crime_max = st["crime_max"] * st["global_multiplier"] * await self.get_rank_multi(ctx)

        embed = discord.Embed(title=f"{profile['name']}'s Payouts", description=f"Global Multiplier: **{st['global_multiplier']}x**\nRank Multiplier: **{await self.get_rank_multi(ctx)}x**", colour=discord.Colour.from_rgb(0, 208, 255))
        embed.add_field(name="Work", value=f"Ranging from {currency} {numformat(work_min)} to {currency} {numformat(work_max)}", inline=False)
        embed.add_field(name="Crime", value=f"Ranging from {currency} {numformat(crime_min)} to {currency} {numformat(crime_max)}", inline=False)
        embed.add_field(name="Slut", value=f"Ranging from {currency} {numformat(slut_min)} to {currency} {numformat(slut_max)}", inline=False)
        embed.set_thumbnail(url=ctx.author.display_avatar)
        embed.timestamp = datetime.utcnow()
        await ctx.send(embed=embed)
        
    @commands.command(
        name="roulette",
        help="Roulette command"
    )
    async def roulette(self, ctx, _bet: str, space: str):

        user = await self.get_user(ctx.author)
        bet = await self.convert_amount(user, _bet)
        st = await self.get_settings()

        if bet < 0:
            await ctx.send("You can't bet a negative amount!")
            return

        # remove bet from user (makes it easier for later)
        await self.update_bal(ctx.author, -bet)

        if bet > user["balance"]:
            embed = discord.Embed(description=f":warning: You do not have enough {st['currency']} to bet that much!", colour=discord.Colour.from_rgb(255, 75, 75))
            embed.timestamp = datetime.utcnow()
            return await ctx.send(embed=embed)

        space_picked = randint(1, 36)
        space_colour = ""
        spaces = []

        # if space_picked % 2 == 0:
        if space_picked in [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]:
            space_colour = "red"
        #if space_picked % 2 != 0:
        elif space_picked in [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35]:
            space_colour = "black"

        win_embed = discord.Embed(
            title="Win!",
            description=f"The ball has landed on {space_colour} {space_picked} \n\nYou won {st['currency']} {numformat(bet)}!",
            colour=discord.Colour.from_rgb(75, 255, 75)
        )
        win_embed.timestamp = datetime.utcnow()
        lose_embed = discord.Embed(
            title="Lose",
            description=f"The ball has landed on {space_colour} {space_picked} \n\nYou lost {st['currency']} {numformat(bet)}!",
            colour=discord.Colour.from_rgb(255, 75, 75)
        )
        lose_embed.timestamp = datetime.utcnow()

        if "," in space:
            spaces = [int(x) for x in space.split(",")]

        if "-" in space:
            _s = space.split("-")
            spaces = [int(x) for x in range(int(_s[0]), int(_s[1]) + 1)]

        if len(spaces) > 18:
            return await ctx.send("Too many numbers!")

        # await ctx.send(f"Space picked: {space_colour} {space_picked}\nUser Pick: {space}\nSpaces: {spaces}")

        if space == "even":
            spaces = [x for x in range(1, 37) if x % 2 == 0]
        if space == "odd":
            spaces = [x for x in range(1, 37) if x % 2 != 0]

        if space == "red":
            spaces = [x for x in range(1, 37) if x % 2 != 0]

        if space == "black":
            spaces = [x for x in range(1, 37) if x % 2 == 0]

        if space == "red":
            if space_colour == "red":
                # add bet to user bal
                bet *= 2
                await self.update_bal(ctx.author, bet)
                return await ctx.send(embed=win_embed)
            else:
                return await ctx.send(embed=lose_embed)

        if space == "black":
            if space_colour == "black":
                # add bet to user bal
                bet *= 2
                await self.update_bal(ctx.author, bet)
                return await ctx.send(embed=win_embed)
            else:
                return await ctx.send(embed=lose_embed)

        if space == "even":
            if space_picked % 2 == 0:
                # add bet to user bal
                bet *= 2
                await self.update_bal(ctx.author, bet)
                return await ctx.send(embed=win_embed)
            else:
                return await ctx.send(embed=lose_embed)

        if space == "odd":
            if space_picked % 2 != 0:
                # add bet to user bal
                bet *= 2
                await self.update_bal(ctx.author, bet)
                return await ctx.send(embed=win_embed)
            else:
                return await ctx.send(embed=lose_embed)

        if space_picked in spaces:
            # add bet to user bal
            bet *= 2
            await self.update_bal(ctx.author, bet)
            return await ctx.send(embed=win_embed)

        # dozens
        if space == "1-12" or space == "13-24" or space == "25-36":
            if space_picked in spaces:
                # add bet to user bal
                bet *= 3
                await self.update_bal(ctx.author, bet)
                return await ctx.send(embed=win_embed)
            else:
                return await ctx.send(embed=lose_embed)

        # halves
        if space in ["1-18", "19-36"]:
            if space_picked in spaces:
                # add bet to user bal
                bet *= 2
                await self.update_bal(ctx.author, bet)
                return await ctx.send(embed=win_embed)
            else:
                return await ctx.send(embed=lose_embed)

        try:
            # if space is invalid (greater than 36 or less than 1)
            if (int(space) > 36) or (int(space) < 1):
                await ctx.send(f"Invalid space, please pick a number between 1 and 36.")
                return
        except ValueError:
            if len(spaces) > 18:
                return await ctx.send("Too many spaces!")

        # if space is a single number
        try:
            if len(space) <= 2 and space_picked == int(space):
                # add bet to user bal
                bet *= 36
                await self.update_bal(ctx.author, bet)
                return await ctx.send(embed=win_embed)
            else:
                return await ctx.send(embed=lose_embed)
        except ValueError:
            return await ctx.send(embed=lose_embed)

    @commands.command(
        name="cockfight", aliases=['cf'],
        description="Play a game of cockfighting with the bot.",
    )
    async def cockfight(self, ctx, _bet: str):

        cf_win_replies = [
            "Your chicken won you {} {}! :chicken:",
            "Your chicken :chicken: beat the other chickens ass so hard, good job! You won {} {}!",
            "The other chicken was weak as fuck, your chicken :chicken: easily won you {} {}",
            "Your chicken turned the other chicken into fucking KFC :poultry_leg: God damn! You won {} {}!",
        ]
        cf_lose_replies = [
            "Your chicken :chicken: lost to the other chicken, better luck next time! You lost {} {}",
            "Your chickens :chicken: ass got beat so hard he doesn't want to fight again. You lost {} {}",
            "Your chicken :chicken: was weak as fuck, the other chicken beat you so hard you lost {} {}",
            "Your chicken was turned into KFC :poultry_leg: Pathetic ass chicken. You lost {} {} :chicken:",
        ]

        user = await self.get_user(ctx.author)
        bet = await self.convert_amount(user, _bet)
        bet_amount_to_display = bet
        st = await self.get_settings()
        winstreak = user["cf_winstreak"]
        winchance = 50 + winstreak # adds winstreak to winchance

        # makes sure winchance doesnt go over max of 70%
        if winchance < 70:
            pass
        else: winchance = 70

        if bet < 0 or bet == 0:
            return await ctx.send("You can't bet that!")

        if bet > user["balance"]:
            embed = discord.Embed(description=f":warning: You do not have enough {st['currency']} to bet that much!", colour=discord.Colour.from_rgb(255, 75, 75))
            embed.timestamp = datetime.utcnow()
            return await ctx.send(embed=embed)

        # remove bet from user (makes it easier for later)
        await self.update_bal(ctx.author, -bet)
            
        # get random number
        n = randint(1, 100)
        # user's chicken won
        if n in range(1, winchance):
            # add bet to user bal
            bet *= 2
            winstreak += 1
            await self.update_bal(ctx.author, bet)
            await self.update_user(ctx.author, "cf_winstreak", winstreak)
            embed = discord.Embed(
                description=choice(cf_win_replies).format(st['currency'], numformat(bet_amount_to_display)),
                colour=discord.Colour.from_rgb(75, 255, 75)
            )
            embed.timestamp = datetime.utcnow()
            embed.set_author(name="🐔 Cockfight", icon_url=ctx.author.display_avatar)
            embed.set_footer(text=f"Winstreak of {winstreak}")
            return await ctx.send(embed=embed)

        # user's chicken lost
        else:
            embed = discord.Embed(
                description=choice(cf_lose_replies).format(st['currency'], numformat(bet_amount_to_display)),
                colour=discord.Colour.from_rgb(255, 75, 75)
            )
            embed.timestamp = datetime.utcnow()
            embed.set_author(name="🐔 Cockfight", icon_url=ctx.author.display_avatar)
            embed.set_footer(text=f"Lost winstreak of {winstreak}")
            winstreak = 0
            await self.update_user(ctx.author, "cf_winstreak", winstreak)
            return await ctx.send(embed=embed)

    @commands.command(
        name="economystats", aliases=["ecostats"],
        description="Shows the global economy stats.",
    )
    async def economystats(self, ctx):

        author = await self.get_user(ctx.author)
        st = await self.get_settings()
        total_bal = 0
        total_kills = 0
        total_users = 0

        for data in self.users.find():
            total_bal += data["balance"]
            total_kills += data["boss_kills"]
            total_users += 1

        embed = discord.Embed(colour=discord.Colour.from_rgb(75, 255, 75))
        embed.description = f"Showing total stats for {total_users} users.\n\n**Net Worth** {st['currency']} {total_bal:,} ({numformat(total_bal)})\n**Total Kills** {total_kills:,}"
        try:
            embed.description += f"\n\n*You are contributing to {(author['balance'] / total_bal) * 100:.2f}% of the total net worth* "
        except ZeroDivisionError:
            embed.description += f"\n\n*You are contributing to 0.00% of the total net worth* "
        try:
            embed.description += f"*and {(author['boss_kills'] / total_kills) * 100:.2f}% of the total boss kills.*"
        except ZeroDivisionError:
            embed.description += f"*and 0.00% of the total boss kills.*"

        embed.timestamp = datetime.utcnow()
        embed.set_author(name="💰 Economy Stats", icon_url=ctx.author.display_avatar)
        return await ctx.send(embed=embed)

    @commands.command(
        name="titlelist", aliases=["tl"],
        description="Shows a list of all titles.",
    )
    async def titlelist(self, ctx):

        embed = discord.Embed(title="Title List", colour=discord.Colour.from_rgb(75, 255, 75))
        embed.add_field(name="👑 Season Champion", value="Awarded to the person who came on top of the leaderboard in that season.", inline=False)
        embed.add_field(name="🏆 Season Elites", value="Awarded to those who reached top 5 in the leaderboard of that season. This title was no longer awarded after Season 12.", inline=False)
        embed.add_field(name="🍀 Lucky Bastard", value="Awarded to players who gambled, a lot, and won, a lot.", inline=False)
        embed.add_field(name="🔨 Gamebreaker", value="Awarded to players who found and reported a gamebreaking bug in the game.", inline=False)
        embed.timestamp = datetime.utcnow()
        embed.set_thumbnail(url=ctx.guild.icon.url)
        return await ctx.send(embed=embed)

    @commands.command(
        name="award", aliases=["awardtitle"],
        description="Awards a title to a user.",
    )
    @commands.has_permissions(administrator=True)
    async def award(self, ctx, user: discord.Member, *, title: str=None):

        if not title:
            return await ctx.send("What are you trying to award them with?")

        # check if user is in database
        if titles.find_one({"_id": user.id}) is None:
            titles.insert_one({
                "_id": user.id,
                "titles": [title],
                "title_equipped": title,
            })
            return await ctx.send("Done")

        # if user not in database
        else:
            title_list = titles.find_one({"_id": user.id})["titles"]
            if title in title_list:  # check if they have title
                return await ctx.send("They already have that title.")
            else:  # add title
                title_list.append(title)
                titles.update_one({"_id": user.id}, {"$set": {"titles": title_list}})
                return await ctx.send("Done")
    
    @commands.command(
        name="drop",
        hidden=True
    )
    @commands.is_owner()
    async def drop(self, ctx, _amount: str):
        amount = await self.convert_amount(ctx.author, _amount)
        st = await self.get_settings()

        await ctx.send(f":exclamation: {ctx.author.name} is dropping {st['currency']} {numformat(amount)} in 5 minutes! <@&774847513298862120>")
        #await asyncio.sleep(300)
        embed = discord.Embed(
            title="💰 Drop",
            description=f"{ctx.author.name} has dropped {st['currency']} {numformat(amount)}! Click the button to collect!",
            colour=discord.Colour.from_rgb(75, 255, 75)
        )
        v = EcoDrop(host=ctx.author.id)
        await ctx.send(embed=embed, view=v)
        await asyncio.sleep(10)
        await ctx.send(v.winners)

    # ------------------------------------------- #
    #              ADMIN COMMANDS                 #
    # ------------------------------------------- #

    @commands.group(name="set", hidden=True)
    @commands.has_permissions(administrator=True)
    async def set(self, ctx):
        pass

    @set.command(name="item")
    @commands.has_permissions(administrator=True)
    async def set_item(self, ctx, user: discord.Member, amount: str, *, item: str):

        user_profile = self.inv.find_one({"_id":ctx.author.id})
        _amt = await self.convert_amount(ctx.author, amount)
        try:
            await self.give_item(user_profile, item, _amt)
            embed = discord.Embed(
                description=f"Added {numformat(_amt)} {item} to {user.mention}'s inventory.",
                colour=discord.Colour.from_rgb(0, 208, 255))
            embed.timestamp = datetime.utcnow()
            embed.set_author(name="Give Item", icon_url=ctx.author.display_avatar)
            await ctx.reply(embed=embed, mention_author=False)
        except:
            raise
            embed = discord.Embed(description=f":warning: Error occurred, please try again.", colour=discord.Colour.from_rgb(255, 75, 75))
            embed.timestamp = datetime.utcnow()
            await ctx.reply(embed=embed, mention_author=False)

    @set.command(name="weapon", hidden=True)
    @commands.has_permissions(administrator=True)
    async def set_weapon(self, ctx, user: discord.Member, *, _weapon: str):

        user_profile = self.inv.find_one({"_id":ctx.author.id})
        try:
            await self.give_weapon(user_profile, _weapon)
            embed = discord.Embed(
                description=f"Gave the weapon {_weapon} to {user.mention}.",
                colour=discord.Colour.from_rgb(0, 208, 255))
            embed.timestamp = datetime.utcnow()
            embed.set_author(name="Give Item", icon_url=ctx.author.display_avatar)
            await ctx.reply(embed=embed, mention_author=False)
        except:
            embed = discord.Embed(description=f":warning: Error occurred, please try again.", colour=discord.Colour.from_rgb(255, 75, 75))
            embed.timestamp = datetime.utcnow()
            await ctx.reply(embed=embed, mention_author=False)

    @set.command(name="balance", aliases=["bal"], hidden=True)
    @commands.has_permissions(administrator=True)
    async def set_balance(self, ctx, user: discord.Member, amount_: str):

        amount = await self.convert_amount(ctx.author, amount_)
        st = await self.get_settings()

        try:
            await self.update_bal(user, amount)
            embed = discord.Embed(
                description=f"Added {st['currency']} {numformat(amount)} to {user.mention}",
                colour=discord.Colour.from_rgb(0, 208, 255))
            embed.timestamp = datetime.utcnow()
            embed.set_author(name="Add Money", icon_url=ctx.author.display_avatar)
            await ctx.reply(embed=embed, mention_author=False)
        except:
            embed = discord.Embed(description=f":warning: Error occurred, please try again.", colour=discord.Colour.from_rgb(255, 75, 75))
            embed.timestamp = datetime.utcnow()
            await ctx.reply(embed=embed, mention_author=False)

    # create an admin command that shows the current economy settings
    @commands.command(name="settings", hidden=True)
    @commands.has_permissions(administrator=True)
    async def settings(self, ctx):

        settings_ = await self.get_settings()
        embed = discord.Embed(description='', colour=discord.Colour.from_rgb(0, 208, 255))
        embed.description += f"**Work**: {settings_['currency']} {await self.payout_multi(settings_['work_min'])} - {settings_['currency']} {await self.payout_multi(settings_['work_max'])}\n"
        embed.description += f"**Crime**: {settings_['currency']} {await self.payout_multi(settings_['crime_min'])} - {settings_['currency']} {await self.payout_multi(settings_['crime_max'])}\n"
        embed.description += f"**Slut**: {settings_['currency']} {await self.payout_multi(settings_['slut_min'])} - {settings_['currency']} {await self.payout_multi(settings_['slut_max'])}\n\n"
        embed.description += f"**Currency**: {settings_['currency']}\n"
        embed.description += f"**Multiplier**: x{settings_['global_multiplier']}"
        embed.set_author(name="Settings", icon_url=ctx.author.display_avatar)
        embed.timestamp = datetime.utcnow()
        await ctx.send(embed=embed)

    @commands.command(name="eco-ban", aliases=["ecoban", "eban"], hidden=True)
    @commands.has_permissions(administrator=True)
    async def eco_ban(self, ctx, user: discord.Member):

        await self.update_user(user, "banned", True)
        embed = discord.Embed(description=f"{user.mention} has been banned from playing economy.",
                              colour=discord.Colour.from_rgb(255, 75, 75))
        embed.set_author(name="Economy Ban", icon_url=ctx.author.display_avatar)
        embed.timestamp = datetime.utcnow()
        await ctx.send(embed=embed)

    @commands.command(name="eco-unban", aliases=["ecounban", "eunban"], hidden=True)
    @commands.has_permissions(administrator=True)
    async def eco_unban(self, ctx, user: discord.Member):

        await self.update_user(user, "banned", False)
        embed = discord.Embed(description=f"{user.mention} has been unbanned from playing economy.",
                              colour=discord.Colour.from_rgb(255, 75, 75))
        embed.set_author(name="Economy Unban", icon_url=ctx.author.display_avatar)
        embed.timestamp = datetime.utcnow()
        await ctx.send(embed=embed)

    @commands.command(name="set_currency", aliases=["setcurrency"], hidden=True)
    @commands.has_permissions(administrator=True)
    async def set_currency(self, ctx, currency: str):
        try:
            await self.set_setting("currency", currency)
            em = discord.Embed(description=f":white_check_mark: Currency set to `{currency}`.", colour=discord.Colour.from_rgb(0, 208, 255))
            em.set_author(name="Set Currency", icon_url=ctx.author.display_avatar)
            em.timestamp = datetime.utcnow()
            return await ctx.send(embed=em)
        except Exception:
            em = discord.Embed(description=":exclamation: Could not set currency, please try again.", colour=discord.Colour.from_rgb(255, 75, 75))
            em.set_author(name="Set Currency", icon_url=ctx.author.display_avatar)
            em.timestamp = datetime.utcnow()
            return await ctx.send(embed=em)

    @commands.command(name="toggle-boss", aliases=["toggleboss", "tboss"], hidden=True)
    @commands.has_permissions(administrator=True)
    async def toggle_boss(self, ctx, toggle: str = "enable"):

        if toggle.lower() == "enable":
            await self.set_setting("bosses_disabled", False)
            em = discord.Embed(description=":white_check_mark: Bosses have been `enabled`.", colour=discord.Colour.from_rgb(0, 208, 255))
            em.set_author(name="Toggle Bosses", icon_url=ctx.author.display_avatar)
            em.timestamp = datetime.utcnow()
            return await ctx.send(embed=em)

        elif toggle.lower() == "disable":
            await self.set_setting("bosses_disabled", True)
            em = discord.Embed(description=":white_check_mark: Bosses have been `disabled`.", colour=discord.Colour.from_rgb(0, 208, 255))
            em.set_author(name="Toggle Bosses", icon_url=ctx.author.display_avatar)
            em.timestamp = datetime.utcnow()
            return await ctx.send(embed=em)

    @commands.command(name="setpayouts", aliases=["setpayout", "setpay"], hidden=True)
    @commands.has_permissions(administrator=True)
    async def set_payouts(self, ctx, command: str, range: str, amount: int):

        st = await self.get_settings()
        currency = st["currency"]
        # Set payouts for work command
        if command.lower() == "work":
            if range.lower() == "min":
                await self.set_setting("work_min", amount)
                em = discord.Embed(description=f":white_check_mark: Minimum work payout set to {currency} {numformat(amount)}.", colour=discord.Colour.from_rgb(0, 208, 255))
                em.set_author(name="Set Payouts", icon_url=ctx.author.display_avatar)
                em.timestamp = datetime.utcnow()
                return await ctx.send(embed=em)
            if range.lower() == "max":
                await self.set_setting("work_max", amount)
                em = discord.Embed(description=f":white_check_mark: Maximum work payout set to {currency} {numformat(amount)}.", colour=discord.Colour.from_rgb(0, 208, 255))
                em.set_author(name="Set Payouts", icon_url=ctx.author.display_avatar)
                return await ctx.send(embed=em)

        if command.lower() == "crime":
            if range.lower() == "min":
                await self.set_setting("crime_min", amount)
                em = discord.Embed(description=f":white_check_mark: Minimum crime payout set to {currency} {numformat(amount)}.", colour=discord.Colour.from_rgb(0, 208, 255))
                em.set_author(name="Set Payouts", icon_url=ctx.author.display_avatar)
                em.timestamp = datetime.utcnow()
                return await ctx.send(embed=em)

            if range.lower() == "max":
                await self.set_setting("crime_max", amount)
                em = discord.Embed(description=f":white_check_mark: Maximum work payout set to {currency} {numformat(amount)}.", colour=discord.Colour.from_rgb(0, 208, 255))
                em.set_author(name="Set Payouts", icon_url=ctx.author.display_avatar)
                return await ctx.send(embed=em)

        if command.lower() == "slut":
            if range.lower() == "min":
                await self.set_setting("slut_min", amount)
                em = discord.Embed(description=f":white_check_mark: Minimum slut payout set to {currency} {numformat(amount)}.", colour=discord.Colour.from_rgb(0, 208, 255))
                em.set_author(name="Set Payouts", icon_url=ctx.author.display_avatar)
                em.timestamp = datetime.utcnow()
                return await ctx.send(embed=em)

            if range.lower() == "max":
                await self.set_setting("slut_max", amount)
                em = discord.Embed(description=f":white_check_mark: Maximum slut payout set to {currency} {numformat(amount)}.", colour=discord.Colour.from_rgb(0, 208, 255))
                em.set_author(name="Set Payouts", icon_url=ctx.author.display_avatar)
                return await ctx.send(embed=em)

    @commands.command(name="enable", aliases=["enable_command"], hidden=True)
    @commands.has_permissions(administrator=True)
    async def enable_command(self, ctx, command: str):

        try:
            await self.set_setting(f"{command.lower()}_disabled", False)
            em = discord.Embed(description=f":white_check_mark: {command.title()} enabled.", colour=discord.Colour.from_rgb(0, 208, 255))
            em.set_author(name="Enable Command", icon_url=ctx.author.display_avatar)
            em.timestamp = datetime.utcnow()
            return await ctx.send(embed=em)
        except:
            raise
            em = discord.Embed(description=f":x: {command.title()} is not a valid command.", colour=discord.Colour.from_rgb(255, 0, 0))
            em.set_author(name="Enable Command", icon_url=ctx.author.display_avatar)
            em.timestamp = datetime.utcnow()
            return await ctx.send(embed=em)

    @commands.command(name="disable", aliases=["disable_command"], hidden=True)
    @commands.has_permissions(administrator=True)
    async def disable_command(self, ctx, command: str):

        try:
            await self.set_setting(f"{command.lower()}_disabled", True)
            em = discord.Embed(description=f":white_check_mark: {command.title()} disabled.", colour=discord.Colour.from_rgb(0, 208, 255))
            em.set_author(name="Disable Command", icon_url=ctx.author.display_avatar)
            em.timestamp = datetime.utcnow()
            return await ctx.send(embed=em)
        except:
            raise
            em = discord.Embed(description=f":x: {command.title()} is not a valid command.", colour=discord.Colour.from_rgb(255, 0, 0))
            em.set_author(name="Disable Command", icon_url=ctx.author.display_avatar)
            em.timestamp = datetime.utcnow()
            return await ctx.send(embed=em)

    @commands.command(name="setmulti", aliases=["set_multi"], hidden=True)
    @commands.has_permissions(administrator=True)
    async def set_multi(self, ctx, multi: int):

        await self.set_setting("global_multiplier", multi)
        em = discord.Embed(description=f":white_check_mark: Multiplier set to {multi}x.", colour=discord.Colour.from_rgb(0, 208, 255))
        em.set_author(name="Set Multiplier", icon_url=ctx.author.display_avatar)
        em.timestamp = datetime.utcnow()
        return await ctx.send(embed=em)

    @commands.command(name="ecoinfo", hidden=True)
    @commands.has_permissions(administrator=True)
    async def ecoinfo(self, ctx):

        st = await self.get_settings()
        currency = st['currency']

        introduction_embed = discord.Embed(title="Welcome to Economy!", colour=discord.Colour.from_rgb(0, 208, 255))
        introduction_embed.description = "Welcome to the server's economy! If you are an old member, you would know the previous economy was on <@292953664492929025>, though that is now retired, and economy is running completely custom now! You can expect things such as ranks, bosses, item crafting, weapon upgrading and more!\n\nThis has been a huge project, and it would not have been able to be completed without the help of these individuals:\n\n**The Economy Team**\n<@455971566199767040> - Developer\n<@452779528167751681> - Ideas, Feedback, Testing\n<@843131902290427974> - Ideas, Feedback, Testing\n<@778827797677998130> - Ideas, Feedback, Testing\n<@510698980636622848> - Ideas, Feedback, Testing\n<@983184004041814016> - Ideas, Feedback\n<@518764077032669187> - Ideas, Feedback\n<@364752513334771713> -  Feedback"
        introduction_embed.set_author(name=f"{ctx.guild.name}", icon_url=ctx.guild.icon.url)

        income_ranks = discord.Embed(title="Income & Ranks", colour=discord.Colour.from_rgb(0, 208, 255))
        income_ranks.description = f"You can earn {currency} using the following commands: `!work`, `!slut`, `!crime`. The amount of currency you get can be boosted by different items and ranks, which you will learn about down the line. You can also give money to other users using the `!givemoney` command.\n\nIn addition, you can use your {currency} to buy different rank upgrades at the shop. (`!shop`) These rank upgrades will give you a multiplier on your normal command income, as well as a sum of {currency} that you can collect every 6 hours, using the `!collect` command!\n\nIf you ever want to check your current command income, or someone elses, you can use the `!payouts` command."
        income_ranks.set_author(name=f"{ctx.guild.name}", icon_url=ctx.guild.icon.url)

        games = discord.Embed(title="Gambling", colour=discord.Colour.from_rgb(0, 208, 255))
        games.description = f"You can gamble your {currency} to your hearts content with the gambling commands! There are currently only two games you can gamble on, being cockfight and roulette.\n\nCockfight is a 50/50 chance of winning or loosing. If you win, you will get back twice your bet, though if you lose, you'll loose it all. Cockfight chances increase by 1% each win, resets back to 50% when you lose, and caps at 70%.\n\nRoulette works as you would expect. You can bet on a specific number, or on a specific colour. If you win, you'll get back either twice your bet, or 3 times your bet, depending on what you bet."
        games.set_author(name=f"{ctx.guild.name}", icon_url=ctx.guild.icon.url)

        bosses = discord.Embed(title="Bosses", colour=discord.Colour.from_rgb(0, 208, 255))
        bosses.description = "You can fight bosses using the /boss command. A word of advice, you should always check what your current stats are before going into a boss, you can use the `!loadout` command to check your weapon, stats, and other things about your profile.\n\nEach boss has a different set of materials, and will have a weapon drop as well. These drops can be categorised into different rarities:\n\n<:common:992507237413167145> Common items\n<:uncommon:992507268715262002> Uncommon items\n<:epic:992507250595877005> Epic items\n<:legendary:992505206308884611> Legendary items\n<:mythic:992527133744304250> Mythic items.\n\nThese rarities can be for weapons, materials and accessories. The final rarity, being <:special:992527447327252532> Special, cannot be obtained from bosses, at the moment there are no obtainable items with this rarity."
        bosses.set_author(name=f"{ctx.guild.name}", icon_url=ctx.guild.icon.url)

        crafting = discord.Embed(title="Crafting & Enhancing", colour=discord.Colour.from_rgb(0, 208, 255))
        crafting.description = f"Boss materials can be combined together to either craft new items, or enhance items you already own.\n\nIf you have the required materials to craft something, you can use the craft command. In case you are missing materials, you will be told what materials you are missing and how many of them.\n\nEnhancing is slightly different. It requires {currency} as well. There are 4 main tiers of enhancements, which can be applied to weapons ranging from <:common:992507237413167145> Common to <:legendary:992505206308884611> Legendary. However, <:mythic:992527133744304250> Mythic weapons __can not__ be enhanced. Enhancements are split into tiers, each tier giving a stat boost to the weapons original stats.\n\n(+1) 💫 ➞ +5% Stats\n(+2) ✨ ➞ +15% Stats\n(+3) ⭐ ➞ +30% Stats\n(+4) 🌟 ➞ +50% Stats"
        crafting.set_author(name=f"{ctx.guild.name}", icon_url=ctx.guild.icon.url)

        await ctx.send(embeds=[introduction_embed, income_ranks, games, bosses, crafting])

def setup(client):
    client.add_cog(Economy(client))