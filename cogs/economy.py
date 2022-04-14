## Main Imports

import nextcord as discord
import asyncio
import time

# Other

from nextcord.ext import commands
from nextcord.ext.commands import BucketType
from nextcord.utils import find
from datetime import datetime
from pymongo import MongoClient
from random import choice, randint
from .utils.replies import workReplies, crimeReplies, slutReplies

# ------------------------------- #
''' Cluster '''
# ------------------------------- #

cluster = MongoClient("mongodb+srv://Cosmo:1H1uqPGjo5CjtHQe@eco.5afje.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
database = cluster["Discord"]
users = database["Users"]
collectdb = database["Collect"]
settings = database["EcoSettings"]

def numformat(number):
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
        
    if ".00" in s:
        s = s.replace(".00", "")
    return s

class Economy(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.users = users
        self.collect = collectdb
        self.settings = settings
        self.logs_id = 814787632776609812

    # setup command, owner only
    @commands.command(name="setup", aliases=["setup_eco"])
    @commands.is_owner()
    async def setup(self, ctx):

        self.settings.insert_one({
            "_id": "settings",
            "currency": ":gem:",
            "work_min": 100,
            "work_max": 1000,
            "work_disabled": False,
            "crime_min": 100,
            "crime_max": 1000,
            "crime_disabled": False,
            "slut_min": 100,
            "slut_max": 1000,
            "slut_disabled": False,
            "global_multiplier": 1,
            "cf_winchance": 50,
            "bosses_disabled": True
        })
        await ctx.send("Done")

    # get users
    async def get_users(self) -> None:

        users_ = self.users.find()
        return users_

    # Get and return user object
    async def get_user(self, user: discord.Member) -> None:

        user = self.users.find_one({"_id": user.id})
        return user

    # Update user object
    async def update_user(self, user: discord.Member, data: str, new_data) -> None:
        user_dict = await self.get_user(user)
        user_dict[data] = new_data
        return self.users.replace_one({"_id": user.id}, user_dict)

    # Update user bal
    async def update_bal(self, user_: discord.Member, amount: int) -> None:
        
        user = await self.get_user(user_)
        user['balance'] += amount
        return self.users.replace_one({"_id": user_.id}, user)

    # Get and return settings object
    async def get_settings(self) -> None:

        settings_ = self.settings.find_one({"_id": "settings"})
        return settings_

    async def set_setting(self, setting: str, value) -> None:

        settings_ = await self.get_settings()
        settings_[setting] = value
        return self.settings.replace_one({"_id": "settings"}, settings_)

    # Amount to give user (based on multis)
    async def get_amount(self, user_: discord.Member, amount: int) -> int:

        user_ = await self.get_user(user_)
        settings_ = await self.get_settings()
        # rank_multi = await self.get_rank_multi(user_)

        return int(amount * settings_["global_multiplier"])

    async def payout_multi(self, amount: int) -> int:

        settings_ = await self.get_settings()
        return int(amount * settings_["global_multiplier"])

    # convert numbers like 1e10 to ints
    async def convert_amount(self, donator, amount: str) -> int:

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
            amount = int(amount)
            if amount < 0:
                return -1

        return abs(amount)

    @commands.command(name="bal", aliases=["balance"])
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
        embed.set_footer(text='Leaderboard Position : #1')
        embed.timestamp = datetime.utcnow()
        return await ctx.send(embed=embed)

    @commands.command(name="start")
    async def start(self, ctx):

        if self.users.count_documents({"_id": ctx.author.id}) == 0:
            self.users.insert_one(
                {"_id": ctx.author.id, "balance": 0, "boss_kills": 0, "can_collect_in": 0, "cf_winstreak": 0,
                 "banned": False})

            em = discord.Embed(description="Created your account.", colour=discord.Colour.from_rgb(0, 208, 255))
            em.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar)
            em.timestamp = datetime.utcnow()
            return await ctx.send(embed=em)

        else:
            return

    @commands.command(name="work", aliases=["job"])
    async def work(self, ctx):
        try:
            user = await self.get_user(ctx.author)

            settings_ = await self.get_settings()
            if user["banned"] is False and settings_["work_disabled"] is False:

                amount = await self.get_amount(ctx.author, randint(settings_["work_min"], settings_["work_max"]))
                reply = choice(workReplies).replace("{}", f"{settings_['currency']} {numformat(amount)}")

                embed = discord.Embed(description=reply, colour=discord.Colour.from_rgb(0, 208, 255))
                embed.timestamp = datetime.utcnow()
                embed.set_author(name="Work", icon_url=ctx.author.display_avatar)
                embed.set_footer(text="Multiplier: x{}".format(settings_["global_multiplier"]))

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

        except Exception:
            em = discord.Embed(
                description=":exclamation: You need an account to play eco. Type `!start` to create one.",
                colour=discord.Colour.from_rgb(0, 208, 255))
            em.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar)
            em.timestamp = datetime.utcnow()
            return await ctx.send(embed=em)

    @commands.command(name="crime", aliases=["rob"])
    async def crime(self, ctx):
        try:
            user = await self.get_user(ctx.author)

            settings_ = await self.get_settings()
            if user["banned"] is False and settings_["crime_disabled"] is False:

                amount = await self.get_amount(ctx.author, randint(settings_["crime_min"], settings_["crime_max"]))
                reply = choice(crimeReplies).replace("{}", f"{settings_['currency']} {numformat(amount)}")

                embed = discord.Embed(description=reply, colour=discord.Colour.from_rgb(0, 208, 255))
                embed.timestamp = datetime.utcnow()
                embed.set_author(name="Crime", icon_url=ctx.author.display_avatar)
                embed.set_footer(text="Multiplier: x{}".format(settings_["global_multiplier"]))

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

        except Exception:
            em = discord.Embed(
                description=":exclamation: You need an account to play eco. Type `!start` to create one.",
                colour=discord.Colour.from_rgb(0, 208, 255))
            em.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar)
            em.timestamp = datetime.utcnow()
            return await ctx.send(embed=em)

    @commands.command(name="slut")
    async def slut(self, ctx):
        try:
            user = await self.get_user(ctx.author)

            settings_ = await self.get_settings()
            if user["banned"] is False and settings_["slut_disabled"] is False:

                amount = await self.get_amount(ctx.author, randint(settings_["slut_min"], settings_["slut_max"]))
                reply = choice(slutReplies).replace("{}", f"{settings_['currency']} {numformat(amount)}")

                embed = discord.Embed(description=reply, colour=discord.Colour.from_rgb(0, 208, 255))
                embed.timestamp = datetime.utcnow()
                embed.set_author(name="Slut", icon_url=ctx.author.display_avatar)
                embed.set_footer(text="Multiplier: x{}".format(settings_["global_multiplier"]))

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

        except Exception:
            em = discord.Embed(
                description=":exclamation: You need an account to play eco. Type `!start` to create one.",
                colour=discord.Colour.from_rgb(0, 208, 255))
            em.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar)
            em.timestamp = datetime.utcnow()
            return await ctx.send(embed=em)

    @commands.command(name="givemoney", aliases=["give", "givemoneyto", "transfer", "pay"])
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
    @commands.command(name="leaderboard", aliases=["lb"])
    async def leaderboard(self, ctx):
        try:
            users = await self.get_users()
            users = sorted(users, key=lambda x: x["balance"], reverse=True)
            embed = discord.Embed(
                description="Top 10 Users",
                colour=discord.Colour.from_rgb(0, 208, 255))
            embed.timestamp = datetime.utcnow()
            embed.set_author(name="Leaderboard", icon_url=ctx.author.display_avatar)
            for i in range(10):
                user = await self.get_user(users[i]["_id"])
                embed.add_field(name=f"{i + 1}. {user['name']}", value=f"{settings['currency']} {numformat(user['balance'])}")
            await ctx.send(embed=embed)
        except:
            await ctx.send("Error occurred, please try again.")

    @commands.command()
    async def updatetest(self, ctx):

        await self.update_bal(ctx.author, -100)
            
    # ------------------------------------------- #
    #              ADMIN COMMANDS                 #
    # ------------------------------------------- #

    @commands.command(name="addmoney")
    @commands.has_permissions(administrator=True)
    async def add_money(self, ctx, user: discord.Member, amt: int):
        
        amount = await self.convert_amount(ctx.author, amt)
        st = await self.get_settings()
        
        try:
            await self.update_bal(user, amount)
            embed = discord.Embed(
                description=f"Added {st['currency']} {numformat(amount)} to {user.mention}",
                colour=discord.Colour.from_rgb(0, 208, 255))
            embed.timestamp = datetime.utcnow()
            await ctx.reply(embed=embed, mention_author=False)
        except:
            embed = discord.Embed(description=f"Error occured, please try again.", colour=discord.Colour.from_rgb(255, 75, 75))
            embed.timestamp = datetime.utcnow()
            await ctx.reply(embed=embed, mention_author=False)
        
    # create an admin command that shows the current economy settings
    @commands.command(name="settings")
    @commands.has_permissions(administrator=True)
    async def settings(self, ctx):

        settings_ = await self.get_settings()
        embed = discord.Embed(description = '', colour=discord.Colour.from_rgb(0, 208, 255))
        embed.description += f"**Work**: {settings_['currency']} {await self.payout_multi(settings_['work_min'])} - {settings_['currency']} {await self.payout_multi(settings_['work_max'])}\n"
        embed.description += f"**Crime**: {settings_['currency']} {await self.payout_multi(settings_['crime_min'])} - {settings_['currency']} {await self.payout_multi(settings_['crime_max'])}\n"
        embed.description += f"**Slut**: {settings_['currency']} {await self.payout_multi(settings_['slut_min'])} - {settings_['currency']} {await self.payout_multi(settings_['slut_max'])}\n\n"
        embed.description += f"**Currency**: {settings_['currency']}\n"
        embed.description += f"**Multiplier**: x{settings_['global_multiplier']}"
        embed.set_author(name="Settings", icon_url=ctx.author.display_avatar)
        embed.timestamp = datetime.utcnow()
        await ctx.send(embed=embed)

    @commands.command(name="eco-ban", aliases=["ecoban", "eban"])
    @commands.has_permissions(administrator=True)
    async def eco_ban(self, ctx, user: discord.Member):

        await self.update_user(user, "banned", True)
        embed = discord.Embed(description=f"{user.mention} has been banned from playing economy.",
                              colour=discord.Colour.from_rgb(255, 75, 75))
        embed.set_author(name="Economy Ban", icon_url=ctx.author.display_avatar)
        embed.timestamp = datetime.utcnow()
        await ctx.send(embed=embed)

    @commands.command(name="eco-unban", aliases=["ecounban", "eunban"])
    @commands.has_permissions(administrator=True)
    async def eco_unban(self, ctx, user: discord.Member):

        await self.update_user(user, "banned", False)
        embed = discord.Embed(description=f"{user.mention} has been unbanned from playing economy.",
                              colour=discord.Colour.from_rgb(255, 75, 75))
        embed.set_author(name="Economy Unban", icon_url=ctx.author.display_avatar)
        embed.timestamp = datetime.utcnow()
        await ctx.send(embed=embed)

    @commands.command(name="set_currency", aliases=["setcurrency"])
    @commands.has_permissions(administrator=True)
    async def set_currency(self, ctx, currency: str):
        try:
            await self.set_setting("currency", currency)
            em = discord.Embed(description=f":white_check_mark: Currency set to `{currency}`.",
                               colour=discord.Colour.from_rgb(0, 208, 255))
            em.set_author(name="Set Currency", icon_url=ctx.author.display_avatar)
            em.timestamp = datetime.utcnow()
            return await ctx.send(embed=em)
        except Exception:
            em = discord.Embed(description=":exclamation: Could not set currency, please try again.",
                               colour=discord.Colour.from_rgb(255, 75, 75))
            em.set_author(name="Set Currency", icon_url=ctx.author.display_avatar)
            em.timestamp = datetime.utcnow()
            return await ctx.send(embed=em)

    @commands.command(name="toggle-boss", aliases=["toggleboss", "tboss"])
    @commands.has_permissions(administrator=True)
    async def toggle_boss(self, ctx, toggle: str="enable"):

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

    @commands.command(name="edit_payouts", aliases=["editpayouts", "setpayouts", "set"])
    @commands.has_permissions(administrator=True)
    async def set(self, ctx, command: str, type_: str, amount: int = None):

        if command.lower() in ['multi', 'multiplier', 'm']:
            await self.set_setting(f"global_multiplier", int(type_))
            em = discord.Embed(description=f":white_check_mark: Global multiplier set to `{int(type_)}`x.", colour=discord.Colour.from_rgb(0, 208, 255))
            em.set_author(name="Payouts", icon_url=ctx.author.display_avatar)
            em.timestamp = datetime.utcnow()
            return await ctx.send(embed=em)

        if type_.lower() == "min":
            await self.set_setting(f"{command.lower()}_min", amount)
            em = discord.Embed(description=f":white_check_mark: {command.title()} minimum payout set to `{amount}`.", colour=discord.Colour.from_rgb(0, 208, 255))
            em.set_author(name="Payouts", icon_url=ctx.author.display_avatar)
            em.timestamp = datetime.utcnow()
            return await ctx.send(embed=em)

        if type_.lower() == "max":
            await self.set_setting(f"{command.lower()}_max", amount)
            em = discord.Embed(description=f":white_check_mark: {command.title()} maximum payout set to `{amount}`.", colour=discord.Colour.from_rgb(0, 208, 255))
            em.set_author(name="Payouts", icon_url=ctx.author.display_avatar)
            em.timestamp = datetime.utcnow()
            return await ctx.send(embed=em)

        if type_.lower() == "disable":
            await self.set_setting(f"{command.lower()}_disabled", True)
            em = discord.Embed(description=f":white_check_mark: {command.title()} has been `disabled`.", colour=discord.Colour.from_rgb(0, 208, 255))
            em.set_author(name="Payouts", icon_url=ctx.author.display_avatar)
            em.timestamp = datetime.utcnow()
            return await ctx.send(embed=em)

        if type_.lower() == "enable":
            await self.set_setting(f"{command.lower()}_disabled", False)
            em = discord.Embed(description=f":white_check_mark: {command.title()} has been `enabled`.", colour=discord.Colour.from_rgb(0, 208, 255))
            em.set_author(name="Payouts", icon_url=ctx.author.display_avatar)
            em.timestamp = datetime.utcnow()
            return await ctx.send(embed=em)

        if type_.lower() in ['work', 'slut', 'crime']:

            if command.lower() == 'enable':
                await self.set_setting(f"{type_.lower()}_disabled", False)
                em = discord.Embed(description=f":white_check_mark: {type_.title()} has been `enabled`.", colour=discord.Colour.from_rgb(0, 208, 255))
                em.set_author(name="Payouts", icon_url=ctx.author.display_avatar)
                em.timestamp = datetime.utcnow()
                return await ctx.send(embed=em)

            if command.lower() == 'disable':
                await self.set_setting(f"{type_.lower()}_disabled", True)
                em = discord.Embed(description=f":white_check_mark: {type_.title()} has been `disabled`.", colour=discord.Colour.from_rgb(0, 208, 255))
                em.set_author(name="Payouts", icon_url=ctx.author.display_avatar)
                em.timestamp = datetime.utcnow()
                return await ctx.send(embed=em)

def setup(client):
    client.add_cog(Economy(client))