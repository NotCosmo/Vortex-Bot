# Main Imports

import nextcord as discord
import random
import asyncio
import time

# Other

from nextcord.ext import commands
from nextcord.ext.commands import BucketType
from nextcord.utils import find
import datetime
from pymongo import MongoClient
from .utils.replies import workReplies, crimeReplies, slutReplies

# ------------------------------- #
''' Cluster '''
# ------------------------------- #

cluster = MongoClient("mongodb+srv://Cosmo:1H1uqPGjo5CjtHQe@eco.5afje.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
database = cluster["Discord"]
eco = database["Economy"]
collectdb = database["Collect"]

def numformat(num):
    num = float('{:.3g}'.format(num))
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['', 'K', 'M', 'B', 'T'][magnitude])

# ------------------------------- #
''' Setup '''
# ------------------------------- #

class Income(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    #@commands.cooldown(1, 21600, BucketType.user)
    async def collect(self, ctx):
        
        x = False
        Economy = eco.find_one({"memberid":ctx.author.id})
        bal = Economy["bal"]
        
        try:

            collect = collectdb.find_one({"memberid":ctx.author.id})
            can_collect_in = collect["can_collect_in"]

            # User collected
            if can_collect_in <= int(datetime.datetime.now().timestamp()):
                amulet = find(lambda r: r.name == "⚜️ Gryphon's Delirium", ctx.message.guild.roles)
                dimensional = find(lambda r: r.name == "🔮 Dimensional Amulet", ctx.message.guild.roles)

                embed = discord.Embed(
                    description = "",
                    colour = discord.Colour.from_rgb(0, 208, 255)
                )

                embed.set_author(name=ctx.author, icon_url=ctx.author.display_avatar)
                embed.timestamp = datetime.datetime.utcnow()

                total = 0

                apprentice = find(lambda r: r.name == "[I] Apprentice", ctx.message.guild.roles)
                legend = find(lambda r: r.name == "[II] Legend", ctx.message.guild.roles)
                guardian = find(lambda r: r.name == "[III] Guardian", ctx.message.guild.roles)
                elder = find(lambda r: r.name == "[IV] Elder", ctx.message.guild.roles)
                heroic = find(lambda r: r.name == "[V] Heroic", ctx.message.guild.roles)
                overlord = find(lambda r: r.name == "[VI] Overlord", ctx.message.guild.roles)
                daunter = find(lambda r: r.name == "[VII] Daunter", ctx.message.guild.roles)
                magician = find(lambda r: r.name == "[VIII] Magician", ctx.message.guild.roles)
                spirit = find(lambda r: r.name == "[IX] Spirit", ctx.message.guild.roles)
                divine = find(lambda r: r.name == "[X] Divine", ctx.message.guild.roles)

                if apprentice in ctx.author.roles:
                    total += 5000
                    embed.description += f"\n{apprentice.mention} - :gem: 5,000"

                if legend in ctx.author.roles:
                    total += 25000
                    embed.description += f"\n{legend.mention} - :gem: 25,000"
                
                if guardian in ctx.author.roles:
                    total += 100000
                    embed.description += f"\n{guardian.mention} - :gem: 100,000"

                if elder in ctx.author.roles:
                    total += 375000
                    embed.description += f"\n{elder.mention} - :gem: 375,000"

                if heroic in ctx.author.roles:
                    total += 500000
                    embed.description += f"\n{heroic.mention} - :gem: 500,000"

                if overlord in ctx.author.roles:
                    total += 3000000
                    embed.description += f"\n{overlord.mention} - :gem: 3,000,000"

                if daunter in ctx.author.roles:
                    total += 7500000
                    embed.description += f"\n{daunter.mention} - :gem: 7,500,000"
                
                if magician in ctx.author.roles:
                    total += 15000000
                    embed.description += f"\n{magician.mention} - :gem: 15,000,000"

                if spirit in ctx.author.roles:
                    total += 25000000
                    embed.description += f"\n{spirit.mention} - :gem: 25,000,000"

                if divine in ctx.author.roles:
                    total += 50000000
                    embed.description += f"\n{divine.mention} - :gem: 50,000,000"

                if amulet in ctx.author.roles or dimensional in ctx.author.roles:
                    total = int(round(total * 1.5))

                embed.description += f"\n\n**Total Collected**: :gem: {numformat(total)}"
                newMoney = bal + total
                eco.update_one({"memberid":ctx.author.id},{"$set":{"bal": newMoney}})
                collectdb.update_one({"memberid":ctx.author.id},{"$set":{"can_collect_in":datetime.datetime.now().timestamp() + int(1*21600)}})
                await ctx.reply(embed=embed,mention_author=False)

            # User cooldown has passed
            else:

                embed = discord.Embed(
                    description = f"You're on cooldown! You can only collect again <t:{int(can_collect_in)}:R>.",
                    colour = discord.Colour.from_rgb(0, 208, 255)
                )

                embed.set_author(name=ctx.author, icon_url=ctx.author.display_avatar)
                embed.timestamp = datetime.datetime.utcnow()
                await ctx.reply(embed=embed,mention_author=False)

        # last_collect = 0; Can Collect
        except:
            collectdb.insert_one({
                "memberid":ctx.author.id,
                "can_collect_in":datetime.datetime.now().timestamp() + int(1*21600)
            })

            amulet = find(lambda r: r.name == "⚜️ Gryphon's Delirium", ctx.message.guild.roles)
            dimensional = find(lambda r: r.name == "🔮 Dimensional Amulet", ctx.message.guild.roles)

            embed = discord.Embed(
                description = "",
                colour = discord.Colour.from_rgb(0, 208, 255)
            )

            embed.set_author(name=ctx.author, icon_url=ctx.author.display_avatar)
            embed.timestamp = datetime.datetime.utcnow()

            total = 0

            apprentice = find(lambda r: r.name == "[I] Apprentice", ctx.message.guild.roles)
            legend = find(lambda r: r.name == "[II] Legend", ctx.message.guild.roles)
            guardian = find(lambda r: r.name == "[III] Guardian", ctx.message.guild.roles)
            elder = find(lambda r: r.name == "[IV] Elder", ctx.message.guild.roles)
            heroic = find(lambda r: r.name == "[V] Heroic", ctx.message.guild.roles)
            overlord = find(lambda r: r.name == "[VI] Overlord", ctx.message.guild.roles)
            daunter = find(lambda r: r.name == "[VII] Daunter", ctx.message.guild.roles)
            magician = find(lambda r: r.name == "[VIII] Magician", ctx.message.guild.roles)
            spirit = find(lambda r: r.name == "[IX] Spirit", ctx.message.guild.roles)
            divine = find(lambda r: r.name == "[X] Divine", ctx.message.guild.roles)

            if apprentice in ctx.author.roles:
                total += 5000
                embed.description += f"\n{apprentice.mention} - :gem: 5,000"

            if legend in ctx.author.roles:
                total += 25000
                embed.description += f"\n{legend.mention} - :gem: 25,000"
            
            if guardian in ctx.author.roles:
                total += 100000
                embed.description += f"\n{guardian.mention} - :gem: 100,000"

            if elder in ctx.author.roles:
                total += 375000
                embed.description += f"\n{elder.mention} - :gem: 375,000"

            if heroic in ctx.author.roles:
                total += 500000
                embed.description += f"\n{heroic.mention} - :gem: 500,000"

            if overlord in ctx.author.roles:
                total += 3000000
                embed.description += f"\n{overlord.mention} - :gem: 3,000,000"

            if daunter in ctx.author.roles:
                total += 7500000
                embed.description += f"\n{daunter.mention} - :gem: 7,500,000"
            
            if magician in ctx.author.roles:
                total += 15000000
                embed.description += f"\n{magician.mention} - :gem: 15,000,000"

            if spirit in ctx.author.roles:
                total += 25000000
                embed.description += f"\n{spirit.mention} - :gem: 25,000,000"

            if divine in ctx.author.roles:
                total += 50000000
                embed.description += f"\n{divine.mention} - :gem: 50,000,000"

            if amulet in ctx.author.roles or dimensional in ctx.author.roles:
                total = int(round(total * 1.5))

            embed.description += f"\n\n**Total Collected**: :gem: {numformat(total)}"
            newMoney = bal + total
            eco.update_one({"memberid":ctx.author.id},{"$set":{"bal": newMoney}})
            await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 10, BucketType.user)
    async def old_work(self, ctx):

        replyMsg = ""

        id = ctx.author.id

        Economy = eco.find_one({"memberid":id})
        Settings = eco.find_one({"name":"Settings"})
        money = Economy["bal"]
        min_val = Settings["work_min_value"]
        max_val = Settings["work_max_value"]
        global_multi = Settings["global_multiplier"]

        # Rank Multi Work
        rankmulti = 1
        amulet_multi = 1
        
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

        if (find(lambda r: r.name == "[VIII] Magician", ctx.message.guild.roles)) in ctx.author.roles:
            rankmulti = 10

        if (find(lambda r: r.name == "[IX] Spirit", ctx.message.guild.roles)) in ctx.author.roles:
            rankmulti = 12

        if (find(lambda r: r.name == "[X] Divine", ctx.message.guild.roles)) in ctx.author.roles:
            rankmulti = 15

        amulet = find(lambda r: r.name == "⚜️ Gryphon's Delirium", ctx.message.guild.roles)
        dimensional = find(lambda r: r.name == "🔮 Dimensional Amulet", ctx.message.guild.roles)

        if amulet in ctx.author.roles:
            amulet_multi = 1.5
        
        if dimensional in ctx.author.roles:
            amulet_multi = 3

        amount = random.randint(round(min_val*rankmulti*global_multi*amulet_multi), round(max_val*rankmulti*global_multi*amulet_multi))

        newMoney = money + amount
        eco.update_one({"memberid":id},{"$set":{"bal": newMoney}})

        c = random.randint(1, 100)
        if c == 1:
            replyMsg = "You work as a teacher, and somehow you made :gem: -6!"

        else:
            replyMsg = random.choice(workReplies).format(f"{amount:,}")

        embed = discord.Embed(
            description = replyMsg,
            colour = discord.Colour.from_rgb(0, 208, 255)
        )

        embed.set_author(name=ctx.author, icon_url=ctx.author.display_avatar)
        embed.set_footer(text=f"Rank Boost: {rankmulti}x")
        embed.timestamp = datetime.datetime.utcnow()
        await ctx.reply(embed=embed, mention_author=False)

    @commands.command()
    async def reset(self, ctx):

        eco.update_one({"memberid":ctx.author.id},{"$set":{"bal": 0}})

    @commands.command()
    @commands.cooldown(1, 10, BucketType.user)
    async def crime(self, ctx):

        replyMsg = ""

        id = ctx.author.id

        Economy = eco.find_one({"memberid":id})
        Settings = eco.find_one({"name":"Settings"})
        money = Economy["bal"]
        min_val = Settings["crime_min_value"]
        max_val = Settings["crime_max_value"]
        global_multi = Settings["global_multiplier"]

        # Rank Multi Work
        rankmulti = 1
        amulet_multi = 1
        
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

        if (find(lambda r: r.name == "[VIII] Magician", ctx.message.guild.roles)) in ctx.author.roles:
            rankmulti = 10

        if (find(lambda r: r.name == "[IX] Spirit", ctx.message.guild.roles)) in ctx.author.roles:
            rankmulti = 12

        if (find(lambda r: r.name == "[X] Divine", ctx.message.guild.roles)) in ctx.author.roles:
            rankmulti = 15

        amulet = find(lambda r: r.name == "⚜️ Gryphon's Delirium", ctx.message.guild.roles)
        dimensional = find(lambda r: r.name == "🔮 Dimensional Amulet", ctx.message.guild.roles)

        if amulet in ctx.author.roles:
            amulet_multi = 1.5
        
        if dimensional in ctx.author.roles:
            amulet_multi = 3

        amount = random.randint(round(min_val*rankmulti*global_multi*amulet_multi), round(max_val*rankmulti*global_multi*amulet_multi))

        newMoney = money + amount
        eco.update_one({"memberid":id},{"$set":{"bal": newMoney}})

        replyMsg = random.choice(crimeReplies).format(f"{amount:,}")

        embed = discord.Embed(
            description = replyMsg,
            colour = discord.Colour.from_rgb(0, 208, 255)
        )

        embed.set_author(name=ctx.author, icon_url=ctx.author.display_avatar)
        embed.set_footer(text=f"Rank Boost: {rankmulti}x")
        embed.timestamp = datetime.datetime.utcnow()
        await ctx.reply(embed=embed, mention_author=False)

    @commands.command()
    @commands.cooldown(1, 10, BucketType.user)
    async def slut(self, ctx):

        replyMsg = ""

        id = ctx.author.id

        Economy = eco.find_one({"memberid":id})
        Settings = eco.find_one({"name":"Settings"})
        money = Economy["bal"]
        min_val = Settings["slut_min_value"]
        max_val = Settings["slut_max_value"]
        global_multi = Settings["global_multiplier"]

        # Rank Multi Work
        rankmulti = 1
        amulet_multi = 1
        
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

        if (find(lambda r: r.name == "[VIII] Magician", ctx.message.guild.roles)) in ctx.author.roles:
            rankmulti = 10

        if (find(lambda r: r.name == "[IX] Spirit", ctx.message.guild.roles)) in ctx.author.roles:
            rankmulti = 12

        if (find(lambda r: r.name == "[X] Divine", ctx.message.guild.roles)) in ctx.author.roles:
            rankmulti = 15

        amulet = find(lambda r: r.name == "⚜️ Gryphon's Delirium", ctx.message.guild.roles)
        dimensional = find(lambda r: r.name == "🔮 Dimensional Amulet", ctx.message.guild.roles)

        if amulet in ctx.author.roles:
            amulet_multi = 1.5
        
        if dimensional in ctx.author.roles:
            amulet_multi = 3

        amount = random.randint(round(min_val*rankmulti*global_multi*amulet_multi), round(max_val*rankmulti*global_multi*amulet_multi))

        newMoney = money + amount
        eco.update_one({"memberid":id},{"$set":{"bal": newMoney}})

        replyMsg = random.choice(slutReplies).format(f"{amount:,}")

        embed = discord.Embed(
            description = replyMsg,
            colour = discord.Colour.from_rgb(0, 208, 255)
        )

        embed.set_author(name=ctx.author, icon_url=ctx.author.display_avatar)
        embed.set_footer(text=f"Rank Boost: {rankmulti}x")
        embed.timestamp = datetime.datetime.utcnow()
        await ctx.reply(embed=embed, mention_author=False)

    @commands.command()
    async def bal(self, ctx, user: discord.Member=None):

        if user is None:
            id = ctx.author.id
            name = ctx.author
            av = ctx.author.display_avatar
        else:
            id = user.id
            name = user
            av = user.display_avatar


        Economy = eco.find_one({"memberid":id})
        bal = Economy["bal"]

        embed = discord.Embed(
            colour = discord.Colour.from_rgb(0, 208, 255),
        )
        embed.add_field(name="Balance", value=f":gem: {numformat(bal)} ({bal:,})", inline=True)
        embed.add_field(name="<:transparent:911319446918955089>", value="<:transparent:911319446918955089>", inline=True)

        i = 1
        rankings = eco.find().sort("bal",-1)
        for x in rankings:
            try:
                temp = ctx.guild.get_member(x["memberid"])
                if temp.id == ctx.author.id:
                    embed.add_field(name=f"Ranking", value=f"{i}/{len(ctx.guild.members)}", inline=True)
                i += 1
            except:
                pass
            if i == 11:
                break


        embed.set_author(name=name, icon_url=av)
        embed.timestamp = datetime.datetime.utcnow()
        await ctx.reply(embed=embed, mention_author=False)

    ''' Extra Commands '''

    @commands.command(aliases = ["titles"])
    async def title(self, ctx, *, title=None):

        id = ctx.author.id

        if not title:
            
            em = discord.Embed(
                title = "Titles",
                description = "You can set a title that you have unlocked from this menu.",
                colour = discord.Colour.from_rgb(0, 208, 255)
            )

            titles = [
                find(lambda r: r.name == "Le Pornhub", ctx.message.guild.roles),
                find(lambda r: r.name == "Season 11 Champion", ctx.message.guild.roles),
                find(lambda r: r.name == "Title 2", ctx.message.guild.roles)
            ]

            for _title in titles:

                if _title in ctx.author.roles:
                    em.add_field(name=f":unlock: {_title}", value=f"- Use >title `{_title}` to enable this title!", inline=False)
                else:
                    em.add_field(name=f":lock: {_title}", value="- You do not have this title unlocked!", inline=False)
            
            em.add_field(name=f":tools: **Poggers**", value="- This title is only available to administrators.", inline=False)
            em.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=em)

        else:

            AdminTitles = [
                "Poggers"
            ]

            titles = [
                find(lambda r: r.name == "Le Pornhub", ctx.message.guild.roles).name,
                find(lambda r: r.name == "Season 11 Champion", ctx.message.guild.roles).name,
                find(lambda r: r.name == "Title 2", ctx.message.guild.roles).name
            ]

            selectedTitle = find(lambda r: r.name == title, ctx.message.guild.roles)

            if title in titles and selectedTitle in ctx.author.roles:
                em = discord.Embed(
                    title = "Profile Updated!",
                    description = f"Your profile title has been updated! You can do `>profile` to view it!",
                    colour = discord.Colour.from_rgb(75, 255, 75)
                )
                em.timestamp = datetime.datetime.utcnow()
                await ctx.reply(embed=em)
                eco.update_one({"memberid":id},{"$set":{"title": title}})

            elif title in AdminTitles and ctx.author.guild_permissions.administrator:
                embed = discord.Embed(
                    title = "Profile Updated!",
                    description = f"Your profile title has been updated! You can do `>profile` to view it!",
                    colour = discord.Colour.from_rgb(75, 255, 75)
                )

                if title == AdminTitles[0]:
                    newTitle = "**Poggers**"

                embed.timestamp = datetime.datetime.utcnow()
                await ctx.reply(embed=embed)
                eco.update_one({"memberid":id},{"$set":{"title": newTitle}})
            else:
                
                em = discord.Embed(
                    title = "Title Error",
                    description = f"Seems you do not have that title unlocked! You can find info about unlocking titles (insert here) or you might be able to purchase it from `>shop`.",
                    colour = discord.Colour.from_rgb(255, 75, 75)
                )
                em.timestamp = datetime.datetime.utcnow()
                await ctx.reply(embed=em)

    @commands.command(aliases = ["give", "pay", "paymoney"])
    async def givemoney(self, ctx, user: discord.Member, amt):

        donator = eco.find_one({"memberid":ctx.author.id})
        receiver = eco.find_one({"memberid":user.id})

        donator_bal = donator["bal"]
        receiver_bal = receiver["bal"]

        if amt == "all":
            amt = int(donator_bal)

        elif amt == "0":
            return

        elif amt == "half":
            amt = int(donator_bal/2)

        elif "e" in amt:

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

        if amt < 0:
            em = discord.Embed(
                description = ":x: Please provide a positive number!",
                colour = discord.Colour.from_rgb(0, 208, 255)
            )

            em.set_author(name=ctx.author, icon_url=ctx.author.display_avatar)
            em.timestamp = datetime.datetime.utcnow()
            return await ctx.send(embed=em)

        amt = abs(amt)
        if amt == None:

            em = discord.Embed(
                description = ":x: Not enough arguments given!\n\nUsage:\n`bj <bet>`",
                colour = discord.Colour.from_rgb(0, 208, 255)
            )

            em.set_author(name=ctx.author, icon_url=ctx.author.display_avatar)
            em.timestamp = datetime.datetime.utcnow()
            return await ctx.send(embed=em)

        if amt == 0:
            return

        if donator_bal >= amt:


            eco.update_one({"memberid":user.id},{"$set":{"bal": receiver_bal+amt}})
            eco.update_one({"memberid":ctx.author.id},{"$set":{"bal": donator_bal-amt}})


            em = discord.Embed(description=f"Gave :gem: {amt:,} to {user.mention}", colour=discord.Colour.from_rgb(0, 208, 255))
            em.timestamp = datetime.datetime.utcnow()
            em.set_author(name=ctx.author, icon_url=ctx.author.display_avatar)
            await ctx.send(embed=em)

        else:

            em = discord.Embed(description=f"You do not have enough money to do that, you need :gem: {(amt-donator_bal):,} more.", colour=discord.Colour.from_rgb(255, 75, 75))
            em.timestamp = datetime.datetime.utcnow()
            em.set_author(name=ctx.author, icon_url=ctx.author.display_avatar)
            await ctx.send(embed=em)

    @commands.command(aliases = ["ecostats", "economystats"])
    async def serverstats(self, ctx):

        i = 1
        embed = discord.Embed(
            description = "",
            colour = discord.Colour.from_rgb(0, 208, 255)
        )

        Economy = eco.find_one({"memberid":ctx.author.id})
        authorbal = Economy["bal"]

        total = 0
        rankings = eco.find().sort("bal",-1)
        for x in rankings:
            try:
                temp = ctx.guild.get_member(x["memberid"])
                bal = x["bal"]
                total += bal
            except:
                pass

        embed.description = f"__**Total Bank**__\n:gem: {total:,}\n\nYou are contributing :gem: {authorbal:,} ({round((authorbal/total)*100, 2)}%) to the server total."
        embed.timestamp = datetime.datetime.utcnow()
        embed.set_author(name=ctx.author, icon_url=ctx.guild.icon.url) 
        await ctx.send(embed=embed)
    
    @commands.command()
    @commands.is_owner()
    async def editstats(self, ctx, stat, newStat, user: discord.Member=None):

        id = user.id
        Stats = eco.find_one({"memberid":id})

        if stat == "bal":
            newStat = int(newStat)
            eco.update_one({"memberid":id},{"$set":{"bal": newStat}})
            await ctx.send(f"Changed {user.mention}'s balance to :gem: {newStat}")

        if stat == "kills":
            newStat = int(newStat)
            eco.update_one({"memberid":id},{"$set":{"totalBossKills": newStat}})
            await ctx.send(f"Changed {user.mention}'s Boss Kills to {newStat}")

# ------------------------------- #
''' Client '''
# ------------------------------- #
def setup(client):
    client.add_cog(Income(client))