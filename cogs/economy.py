# Main Imports

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
from .utils.utils_dict import ranks

# ------------------------------- #
''' Cluster '''
# ------------------------------- #

cluster = MongoClient("mongodb+srv://Cosmo:1H1uqPGjo5CjtHQe@eco.5afje.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
database = cluster["Discord"]
users = database["Users"]
collectdb = database["Collect"]
settings = database["EcoSettings"]

def numformat(num):
    num = float('{:.3g}'.format(num))
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['', 'K', 'M', 'B', 'T'][magnitude])

class Economy(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.userdb = users
        self.collectdb = collectdb
        self.settingsdb = settings
        self.logs_id = 814787632776609812
    
    async def get_rank_multi(self, ctx, user) -> None:

        rankmulti = 1
        
        if (find(lambda r: r.name == '[I] Rank', ctx.message.guild.roles) in user.roles):
            rankmulti = 5

        return rankmulti

    async def get_stat(self, stat: str, user_id: int) -> None:

        # Get user object
        user = self.userdb.find_one({"_id":user_id})
        return user[stat]

    async def get_setting(self, setting: str) -> None:

        # Get settings db object
        st = self.settingsdb.find_one({"tag":"Settings"})
        return st[setting]

    async def lb_position(self, ctx, stat: str, user_id: int) -> None:

        rankings = self.userdb.find().sort(stat,-1)
        i = 1

        # Cycle through database entries
        for entry in rankings:

            try:
                # Get user object and user bal
                user = ctx.guild.get_member(entry["_id"])

                # Check if we found user we are looking for
                if user.id == user_id:
                    return i

                i += 1

            except:
                # Could not get user
                pass

    @commands.command()
    @commands.is_owner()
    async def setup(self, ctx):

        self.settingsdb.insert_one(
            {
            "tag":"Settings",
            "currency":":gem:",
            "work_min_value":100,
            "work_max_value":800,
            "slut_min_value":150,
            "slut_max_value":850,
            "crime_min_value":250,
            "crime_max_value":1000,
            "global_multiplier":1,
            "default_cf_winchance":50,
            "economy_disabled":False,
            "bosses_disabled":False,
            })

    @commands.command(hidden=True)
    @commands.has_permissions(administrator=True)
    async def set(self, ctx, user: discord.Member, stat: str, new_value):

        if stat in ['bal']:
            new_value = int(new_value)
        else:
            new_value = str(new_value)

        self.userdb.update_one({"_id":user.id},{"$set":{stat:new_value}})
        await ctx.message.add_reaction("✅")

    @commands.command(hidden=True)
    @commands.has_permissions(administrator=True)
    async def settings(self, ctx):

        settings = self.settingsdb.find_one({"tag":"Settings"})

        em = discord.Embed(description='',colour=discord.Colour.from_rgb(0,208,255))
        currency = settings["currency"]
        cf = settings["default_cf_winchance"]
        eco = settings["economy_disabled"]
        bosses = settings["bosses_disabled"]
        em.description += f"**Currency**: {currency}\n"
        em.description += f"**Cf Winchance**: {cf}%\n"
        em.description += f"**Economy Disabled**: {eco}\n"
        em.description += f"**Bosses Disabled**: {bosses}\n"
        em.set_footer(text="To view payouts, use the payouts command.")
        await ctx.send(embed=em)

    @commands.command(aliases = ['set-currency'])
    @commands.has_permissions(administrator=True)
    async def setcurrency(self, ctx, new_currency: str=None):

        if new_currency is None:
            settings = self.settingsdb.find_one({"tag":"Settings"})
            currency = settings["currency"]
            await ctx.send(currency)
        else:
            self.settingsdb.update_one({"tag":"Settings"},{"$set":{"currency":new_currency}})
            await ctx.message.add_reaction("✅")

    @commands.command()
    async def work(self, ctx):

        if self.userdb.count_documents({"_id":ctx.author.id}) == 0:
            return
        else:

            # Getting values and multis
            min_val = await self.get_setting('work_min_value')
            max_val = await self.get_setting('work_max_value')
            bal = await self.get_stat('bal', ctx.author.id)
            multi = await self.get_rank_multi(ctx, ctx.author)
            amount = randint(min_val*multi, max_val*multi)
            replyMsg = choice(workReplies).format(f"{amount:,}")

            # Updating User Bal
            self.userdb.update_one({"_id":ctx.author.id},{"$set":{"bal":bal+amount}})

            embed = discord.Embed(
                description = replyMsg,
                colour = discord.Colour.from_rgb(0, 208, 255)
            )

            embed.set_author(name=ctx.author, icon_url=ctx.author.display_avatar)
            embed.set_footer(text=f"Rank Boost: {multi}x")
            embed.timestamp = datetime.utcnow()
            await ctx.reply(embed=embed, mention_author=False)
    
    @commands.command(aliases = ['ball', 'profile'])
    @commands.has_permissions(administrator=True)
    async def balance(self, ctx, user: discord.Member=None):

        if user is None:
            id = ctx.author.id
            av = ctx.author.display_avatar
            name = ctx.author
        else:
            id = user.id
            av = user.display_avatar
            name = user

        try:
        
            bal = await self.get_stat("bal", id)
            boss_kills = await self.get_stat("boss_kills", id)
            currency = await self.get_setting("currency")
            position = await self.lb_position(ctx, "bal", id)

            embed = discord.Embed(
                colour = discord.Colour.from_rgb(0, 208, 255),
            )
            embed.add_field(name="Balance", value=f"{currency} {bal:,}", inline=True)
            embed.add_field(name="<:transparent:911319446918955089>", value="<:transparent:911319446918955089>", inline=True)
            embed.add_field(name="Position", value=f"{position}/{ctx.guild.member_count}", inline=True)
            embed.add_field(name="Boss Kills", value=boss_kills, inline=False)
            embed.set_author(name=name, icon_url=av)
            embed.timestamp = datetime.utcnow()
            return await ctx.reply(embed=embed, mention_author=False)

        except:
            
            # User does not have an actual profile
            if self.userdb.count_documents({"_id":id}) == 0:
                self.userdb.insert_one({
                    "_id":id,
                    "bal":0,
                    "can_collect_in":0,
                    "boss_kills":0,
                    "cf_winstreak":0,
                    "eco_locked":False,
                })

                bal = await self.get_stat("bal", id)
                boss_kills = await self.get_stat("boss_kills", id)
                currency = await self.get_setting("currency")
                position = await self.lb_position(ctx, "bal", id)


                embed = discord.Embed(
                    colour = discord.Colour.from_rgb(0, 208, 255),
                )
                embed.add_field(name="Balance", value=f"{currency} {bal:,}", inline=True)
                embed.add_field(name="<:transparent:911319446918955089>", value="<:transparent:911319446918955089>", inline=True)
                embed.add_field(name="Position", value=f"{position}", inline=False)
                embed.add_field(name="Boss Kills", value=boss_kills, inline=True)
                embed.set_author(name=name, icon_url=av)
                embed.timestamp = datetime.utcnow()
                return await ctx.reply(embed=embed, mention_author=False)
            
            # Command failed in general
            else:
                await ctx.reply(":exclamation: Command failed.", mention_author=False)

    @commands.command()
    async def lb(self, ctx, _type=None):

        i = 1

        if _type is None or _type == "gem":

            embed = discord.Embed(
                description = "Gems can be used in exchange to purchase different ranks and items over at `>shop`.\n",
                colour = discord.Colour.from_rgb(0, 208, 255)
            )

            rankings = self.userdb.find().sort("bal",-1)
            currency = await self.get_setting("currency")

            for entry in rankings:
                try:
                    user = ctx.guild.get_member(entry["_id"])
                    bal = entry["bal"]
                    #embed.add_field(name=f"`[#{i}]` {temp.name}", value=f":gem: {bal:,}", inline=False)

                    if user.id == ctx.author.id:
                        embed.set_footer(text=f"Your Rank: {i}/{ctx.guild.member_count}")

                    if i in [1, 2, 3]:
                        embed.description += f"\n**#{i}.** {user.mention} - {currency} {bal:,} \n\n"
                        #embed.add_field(name=f"**#{i}.** {user.name}",value=f"{currency} {bal}\n<:transparent:911319446918955089>")
                    elif i == 10:       
                        embed.description += f"\n#{i}. {user.mention} - {user.mention} - {currency} {bal:,}"
                        #embed.add_field(name=f"**#{i}.** {user.mention}",value=f"{currency} {bal}\n<:transparent:911319446918955089>")
                    else:
                        embed.description += f"\n#{i}. {user.mention} - {user.mention} - {currency} {bal:,} \n<:transparent:911319446918955089>"
                        #embed.add_field(name=f"**#{i}.** {user.mention}",value=f"{currency} {bal}\n<:transparent:911319446918955089>")
                    i += 1
                except:
                    pass
                if i == 11:
                    break

            embed.timestamp = datetime.utcnow()
            embed.set_author(name="Gem Leaderboard", icon_url=ctx.guild.icon.url) 
            await ctx.send(embed=embed)

        if _type == "kills":

            embed = discord.Embed(
                description = "Boss kills are counted whenever you kill a boss, tutorial bosses (Minion) not included.\n",
                colour = discord.Colour.from_rgb(0, 208, 255)
            )

            rankings = self.userdb.find().sort("boss_kills",-1)
            for entry in rankings:
                try:
                    user = ctx.guild.get_member(entry["_id"])
                    kills = entry["boss_kills"]
                    #embed.add_field(name=f"`[#{i}]` {temp.name}", value=f":gem: {bal:,}", inline=False)

                    if user.id == ctx.author.id:
                        embed.set_footer(text=f"Your Rank: {i}/{ctx.guild.member_count}")

                    if i in [1, 2, 3]:
                        embed.description += f"\n**#{i}.** {user.mention} - :crossed_swords: {kills} \n\n"
                        #embed.add_field(name=f"**#{i}.** {user.mention}",value=f":crossed_swords: {bal}\n<:transparent:911319446918955089>")
                    elif i == 10:       
                        embed.description += f"\n#{i}. {user.mention} - :crossed_swords: {kills}"
                        #embed.add_field(name=f"**#{i}.** {user.mention}",value=f":crossed_swords: {bal}\n<:transparent:911319446918955089>")
                    else:
                        embed.description += f"\n#{i}. {user.mention} - :crossed_swords: {kills} \n<:transparent:911319446918955089>"
                        #embed.add_field(name=f"**#{i}.** {user.mention}",value=f":crossed_swords: {bal}\n<:transparent:911319446918955089>")
                    i += 1
                except:
                    pass
                if i == 11:
                    break

            embed.timestamp = datetime.utcnow()
            embed.set_author(name="Kills Leaderboard", icon_url=ctx.guild.icon.url) 
            await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Economy(client))