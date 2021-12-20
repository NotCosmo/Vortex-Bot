# Main Imports

import nextcord as discord
import random
import asyncio
import time
import typing

# Other

from nextcord.ext import commands
from nextcord.ext.commands import BucketType
from nextcord.utils import find
import datetime
from pymongo import MongoClient

# ------------------------------- #
''' Cluster '''
# ------------------------------- #

cluster = MongoClient("mongodb+srv://Cosmo:1H1uqPGjo5CjtHQe@eco.5afje.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
database = cluster["Discord"]
eco = database["Economy"]

# ------------------------------- #
''' Setup '''
# ------------------------------- #

class AdminConfig(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def elock(self, ctx, *, update_message):

        eco_channels = [735796560792780891, 814787175576109067, 814787195428405259, 872450532659327016]
        # await channel.set_permissions(ctx.guild.default_role, send_messages=False)

        em = discord.Embed(title="Channel Locked", description=update_message,colour=discord.Colour.from_rgb(0, 208, 255))
        em.set_author(name=ctx.author,icon_url=ctx.author.display_avatar)

        for id in eco_channels:
            channel = self.client.get_channel(id)
            await channel.set_permissions(ctx.guild.default_role, send_messages=False)
            await channel.send(embed=em)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def eunlock(self, ctx, *, update_message="Channels unlocked, thank you for your patience."):

        eco_channels = [735796560792780891, 814787175576109067, 814787195428405259, 872450532659327016]
        # await channel.set_permissions(ctx.guild.default_role, send_messages=False)

        em = discord.Embed(title="Channel Unlocked", description=update_message,colour=discord.Colour.from_rgb(0, 208, 255))
        em.set_author(name=ctx.author,icon_url=ctx.author.display_avatar)

        for id in eco_channels:
            channel = self.client.get_channel(id)
            await channel.set_permissions(ctx.guild.default_role, send_messages=None)
            await channel.send(embed=em)

    @commands.command(aliases = ['ac'])
    @commands.has_permissions(administrator=True)
    async def adminconfig(self, ctx):

        em = discord.Embed(
            title = "Admin Config",
            description = "- All commands have dedicated arguments.\n- Arguments in `[]` are optional, while those in `<>` are required.\n\n ** **\n\n",
            colour = discord.Colour.from_rgb(0, 208, 255)
        )

        em.add_field(name="`>newprofile <id/mention>`", value="- Manually creates a profile/database entry for specified user.", inline=False)
        em.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=em)

    @commands.command()
    @commands.is_owner()
    async def createsettings(self, ctx):

        eco.insert_one(
            {
            "name":"Settings",
            "work_min_value":100,
            "work_max_value":800,
            "slut_min_value":150,
            "slut_max_value":850,
            "crime_min_value":250,
            "crime_max_value":1000,
            "global_multiplier":1,
            })

        em = discord.Embed(
            title = ":hammer_pick: Settings Created",
            description = f"Created Settings for the Economy Database.",
            colour = discord.Colour.from_rgb(0, 208, 255)
        )
        em.set_footer(text=f"Administered By: {ctx.author}", icon_url=ctx.author.avatar.url)
        em.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=em)

    @commands.command(aliases = ["setmulti"])
    @commands.has_permissions(administrator=True)
    async def setglobalmulti(self, ctx, multi: float):

        Settings = eco.find_one({"name":"Settings"})
        old_global_multi = Settings["global_multiplier"]

        eco.update_one({"name":"Settings"},{"$set":{"global_multiplier": multi}})
            
        em = discord.Embed(
            description = f"Set `global multiplier` from `{old_global_multi}x` to `{multi}x`  ",
            colour = discord.Colour.from_rgb(0, 208, 255)
        )
        em.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
        em.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=em)

    @commands.command(aliases = ["setpayout"])
    @commands.has_permissions(administrator=True)
    async def setincome(self, ctx, command, _range, amt: int):
        
        Settings = eco.find_one({"name":"Settings"})

        work_min = Settings["work_min_value"]
        work_max = Settings["work_max_value"]
        slut_min = Settings["slut_min_value"]
        slut_max = Settings["slut_max_value"]
        crime_min = Settings["crime_min_value"]
        crime_max = Settings["crime_max_value"]


        if command == "work" and _range == "min":

            eco.update_one({"name":"Settings"},{"$set":{"work_min_value": amt}})
            
            em = discord.Embed(
                description = f"Set `{_range}` payout for `{command}` to :gem: {amt:,}",
                colour = discord.Colour.from_rgb(0, 208, 255)
            )
            em.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
            em.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=em)

        elif command == "work" and _range == "max":

            eco.update_one({"name":"Settings"},{"$set":{"work_max_value": amt}})
            
            em = discord.Embed(
                description = f"Set `{_range}` payout for `{command}` to :gem: {amt:,}",
                colour = discord.Colour.from_rgb(0, 208, 255)
            )
            em.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
            em.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=em)

        elif command == "slut" and _range == "min":

            eco.update_one({"name":"Settings"},{"$set":{"slut_min_value": amt}})
            
            em = discord.Embed(
                description = f"Set `{_range}` payout for `{command}` to :gem: {amt:,}",
                colour = discord.Colour.from_rgb(0, 208, 255)
            )
            em.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
            em.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=em)

        elif command == "slut" and _range == "max":

            eco.update_one({"name":"Settings"},{"$set":{"slut_max_value": amt}})
            
            em = discord.Embed(
                description = f"Set `{_range}` payout for `{command}` to :gem: {amt:,}",
                colour = discord.Colour.from_rgb(0, 208, 255)
            )
            em.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
            em.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=em)

        elif command == "crime" and _range == "min":

            eco.update_one({"name":"Settings"},{"$set":{"crime_min_value": amt}})
            
            em = discord.Embed(
                description = f"Set `{_range}` payout for `{command}` to :gem: {amt:,}",
                colour = discord.Colour.from_rgb(0, 208, 255)
            )
            em.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
            em.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=em)

        elif command == "crime" and _range == "max":

            eco.update_one({"name":"Settings"},{"$set":{"crime_max_value": amt}})
            
            em = discord.Embed(
                description = f"Set `{_range}` payout for `{command}` to :gem: {amt:,}",
                colour = discord.Colour.from_rgb(0, 208, 255)
            )
            em.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
            em.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=em)

        else:

            em = discord.Embed(
                colour = discord.Colour.from_rgb(0, 208, 255)
            )

            em.description += f"\n\n`work`: min: :gem: {work_min} | max: :gem: {work_max}"
            em.description += f"\n\n`slut`: min: :gem: {slut_min} | max: :gem: {slut_max}"
            em.description += f"\n\n`crime`: min: :gem: {crime_min} | max: :gem: {crime_max}"
            em.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
            em.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=em)

    @commands.command(aliases = ["incomes"])
    async def payouts(self, ctx):

        Settings = eco.find_one({"name":"Settings"})

        work_min = Settings["work_min_value"]
        work_max = Settings["work_max_value"]
        slut_min = Settings["slut_min_value"]
        slut_max = Settings["slut_max_value"]
        crime_min = Settings["crime_min_value"]
        crime_max = Settings["crime_max_value"]
        global_multi = Settings["global_multiplier"]

        em = discord.Embed(
            description = "",
            colour = discord.Colour.from_rgb(0, 208, 255)
        )

        # Rank Multi Work
        rankmulti = 1
        
        if find(lambda r: r.name == "[I] Apprentice", ctx.message.guild.roles) in ctx.author.roles:
            rankmulti = 2

        if (find(lambda r: r.name == "[II] Legend", ctx.message.guild.roles)) in ctx.author.roles:
            rankmulti = 2.5
        
        if (find(lambda r: r.name == "[III] Guardian", ctx.message.guild.roles)) in ctx.author.roles:
            rankmulti = 3

        if (find(lambda r: r.name == "[IV] Elder", ctx.message.guild.roles)) in ctx.author.roles:
            rankmulti = 4

        if (find(lambda r: r.name == "[V] Heroic", ctx.message.guild.roles)) in ctx.author.roles:
            rankmulti = 5

        if (find(lambda r: r.name == "[VI] Overlord", ctx.message.guild.roles)) in ctx.author.roles:
            rankmulti = 6

        if (find(lambda r: r.name == "[VII] Daunter", ctx.message.guild.roles)) in ctx.author.roles:
            rankmulti = 8

        amulet = find(lambda r: r.name == "⚜️ Gryphon's Delirium", ctx.message.guild.roles)
        if amulet in ctx.author.roles:
            amuletmulti = 1.5
        else:
            amuletmulti = 1

        em.description += "Your current payout ranges based on global & rank multipliers:"
        em.description += f"\n\n**Global Multiplier** - {global_multi}x"
        em.description += f"\n**Rank Multiplier** - {rankmulti}x"
        em.description += f"\n**Personal Multiplier** - {amuletmulti}x (Amulets)\n"
        em.description += f"\n`work` - min: :gem: {round((work_min*global_multi*rankmulti*amuletmulti)):,} | max: :gem: {round((work_max*global_multi*rankmulti*amuletmulti)):,}"
        em.description += f"\n`slut` - min: :gem: {round((slut_min*global_multi*rankmulti*amuletmulti)):,} | max: :gem: {round((slut_max*global_multi*rankmulti*amuletmulti)):,}"
        em.description += f"\n`crime` -  min: :gem: {round((crime_min*global_multi*rankmulti*amuletmulti)):,} | max: :gem: {round((crime_max*global_multi*rankmulti*amuletmulti)):,}"
        em.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
        em.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=em)

    @commands.command(aliases = ["dpayouts"])
    async def defaultpayouts(self, ctx):

        Settings = eco.find_one({"name":"Settings"})

        work_min = Settings["work_min_value"]
        work_max = Settings["work_max_value"]
        slut_min = Settings["slut_min_value"]
        slut_max = Settings["slut_max_value"]
        crime_min = Settings["crime_min_value"]
        crime_max = Settings["crime_max_value"]
        global_multi = Settings["global_multiplier"]

        em = discord.Embed(
            description = "",
            colour = discord.Colour.from_rgb(0, 208, 255)
        )

        em.description += "Your current payout ranges based on global & rank multipliers:"
        em.description += f"\n\n**Global Multiplier** - {global_multi}x"
        em.description += f"\n`work` - min: :gem: {work_min:,} | max: :gem: {work_max:,}"
        em.description += f"\n`slut` - min: :gem: {slut_min:,} | max: :gem: {slut_max:,}"
        em.description += f"\n`crime` -  min: :gem: {crime_min:,} | max: :gem: {crime_max:,}"
        em.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
        em.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=em)

    @commands.command(aliases = ['np'])
    @commands.has_permissions(administrator=True)
    async def newprofile(self, ctx, user: discord.Member=None):

        if user is None:
            id = ctx.author.id

        else:
            id = user.id

        if eco.count_documents({"memberid":id}) == 0:
            eco.insert_one(
            {
            "memberid":id,
            "bal":0,
            "totalBossKills":0,
            "profileDesc":"None Set",
            "title":"None",
            "currentQuest":"Merlin1",
            "questObjectiveCounter":0,
            "cfWinStreak":0,
            "mineLevel":1,
            })

            em = discord.Embed(
                title = ":hammer_pick: Profile Created",
                description = f"Added `9` database entries for MemberID `{id}`.",
                colour = discord.Colour.from_rgb(0, 208, 255)
            )
            em.set_footer(text=f"Created by: {ctx.author}", icon_url=ctx.author.avatar.url)
            em.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=em)

        else:

            em = discord.Embed(
                title = ":hammer_pick: Existing Profile",
                description = f"There is already a profile created under the `{id}` MemberID.",
                colour = discord.Colour.from_rgb(255, 75, 75)
            )
            em.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=em)

    @commands.command()
    async def startprofile(self, ctx):

        id = ctx.author.id

        if eco.count_documents({"memberid":id}) == 0:
            eco.insert_one(
            {
            "memberid":id,
            "bal":0,
            "totalBossKills":0,
            "profileDesc":"None Set",
            "title":"None",
            "currentQuest":"Merlin1",
            "questObjectiveCounter":0,
            "cfWinStreak":0,
            "mineLevel":1,
            })

            em = discord.Embed(
                title = ":hammer_pick: Profile Created",
                description = f"Added `9` database entries for MemberID `{id}`.",
                colour = discord.Colour.from_rgb(0, 208, 255)
            )
            em.set_footer(text=f"Created by: {ctx.author}", icon_url=ctx.author.avatar.url)
            em.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=em)

    @commands.command(aliases = ['s'])
    @commands.has_permissions(administrator=True)
    async def stats(self, ctx, user: discord.Member=None):

        if user is None:
            id = ctx.author.id

        else:
            id = user.id

        Economy = eco.find_one({"memberid":id})

        em = discord.Embed(
            title = ":hammer_pick: Stats Display",
            description = f"`[MemberID]`: {id}",
            colour = discord.Colour.from_rgb(0, 208, 255)
        )
        
        bal = Economy["bal"]
        kills = Economy["totalBossKills"]
        quest = Economy["currentQuest"]
        questCounter = Economy["questObjectiveCounter"]
        winstreak = Economy["cfWinStreak"]
        mineLv = Economy["mineLevel"]

        em.description += f"\n`[Bal]`: {bal:,}"
        em.description += f"\n`[Boss Kills]`: {kills:,}"
        em.description += f"\n`[Quest]`: {quest}"
        em.description += f"\n`[Quest Counter]`: {questCounter}"
        em.description += f"\n`[Winstreak]`: {winstreak}"
        em.description += f"\n`[Mine Level]`: {mineLv}"

        em.set_footer(text=f"Admin Config", icon_url=ctx.author.avatar.url)
        em.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=em)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def upgrade(self, ctx):

        levels = {
            1:400000,
            2:1200000,
            3:5000000,
        }

        mineLevel = eco.find_one({"memberid":ctx.author.id})["mineLevel"]
        bal = eco.find_one({"memberid":ctx.author.id})["bal"]

        cost = levels[mineLevel]
        if bal < cost:
            await ctx.send(f"You do not have enough money to buy upgrade {mineLevel}")
        elif bal > cost:
            await ctx.send(f"Sucessfully bought Upgrade {mineLevel}!")

            newBal = bal - cost
            eco.update_one({"memberid":ctx.author.id},{"$set":{"bal": newBal}})
            eco.update_one({"memberid":ctx.author.id},{"$set":{"mineLevel": mineLevel+1}})

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def addmoney(self, ctx, user: discord.Member, amt):

        id = user.id

        if "e" in amt:

            string = amt.split("e")
            num = string[0]
            exponent = string[1]
            
            amt = int(num) * (10 ** int(exponent))

        elif "," in amt:

            string = amt.split(",")
            _string = ''
            for x in string:
                _string += x
                amt = int(_string)

        else:
            amt = int(amt)

        Economy = eco.find_one({"memberid":id})
        bal = Economy["bal"]
        eco.update_one({"memberid":id},{"$set":{"bal": bal+amt}})
        em = discord.Embed(description=f"Added :gem: {amt:,} to {user.mention}.", colour=discord.Colour.from_rgb(0, 208, 255))
        em.timestamp = datetime.datetime.utcnow()
        em.set_author(name=ctx.author, icon_url=ctx.author.display_avatar)
        await ctx.send(embed=em)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def removemoney(self, ctx, user: discord.Member, amt):

        id = user.id

        if "e" in amt:

            string = amt.split("e")
            num = string[0]
            exponent = string[1]
            
            amt = int(num) * (10 ** int(exponent))

        elif "," in amt:

            string = amt.split(",")
            _string = ''
            for x in string:
                _string += x
                amt = int(_string)

        else:
            amt = int(amt)

        Economy = eco.find_one({"memberid":id})
        
        bal = Economy["bal"]
        eco.update_one({"memberid":id},{"$set":{"bal": bal-amt}})

        em = discord.Embed(description=f"Added :gem: {amt:,} to {user.mention}.", colour=discord.Colour.from_rgb(0, 208, 255))
        em.timestamp = datetime.datetime.utcnow()
        em.set_author(name=ctx.author, icon_url=ctx.author.display_avatar)
        await ctx.send(embed=em)


def setup(client):
    client.add_cog(AdminConfig(client))