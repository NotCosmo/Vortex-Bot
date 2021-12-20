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

# ------------------------------- #
''' Cluster '''
# ------------------------------- #

cluster = MongoClient("mongodb+srv://Cosmo:1H1uqPGjo5CjtHQe@eco.5afje.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
database = cluster["Discord"]
eco = database["Economy"]

# ------------------------------- #
''' Client '''
# ------------------------------- #

class Shop(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @commands.command(aliases = ['potionshop', 'potionsshop'])
    @commands.has_permissions(administrator=True)
    async def potions(self, ctx, page: int=1):

        ''' Page 1 '''
        if page == 1:
            
            em = discord.Embed(
                description = "Use `!buy [item-name]` to buy an item.", #\nYou can also use `!iteminfo [item-name]` to get information on a shop item.",
                colour = discord.Colour.from_rgb(0, 208, 255)
            )

            # RANKS
            em.add_field(name="[Tier I] Damage Potion - :gem: 100,000", value="- Gives you +5% damage in boss fights.\n<:transparent:911319446918955089>", inline=False)
            
            em.timestamp = datetime.datetime.utcnow()
            em.set_author(name="Cosmo's Lounge Shop", icon_url=ctx.guild.icon.url)
            em.set_footer(text="Page 1/1")

            await ctx.send(embed=em)

        else:
            return

    @commands.command()
    async def shop(self, ctx, page: int=1):

        ''' Page 1'''
        if page == 1:

            bal = eco.find_one({"memberid":ctx.author.id})["bal"]

            em = discord.Embed(
                description = f"Use `!buy [item-name]` to buy an item.\nBalance: :gem: {bal}", #\nYou can also use `!iteminfo [item-name]` to get information on a shop item.",
                colour = discord.Colour.from_rgb(0, 208, 255)
            )

            # RANKS
            em.add_field(name="[I] Apprentice - :gem: 50,000", value=":star: Gives you :gem: 5,000 every 6 hours.\n:zap: Rank Boost: **2x**\n<:transparent:911319446918955089>", inline=False)
            em.add_field(name="[II] Legend - :gem: 100,000", value=":star: Gives you :gem: 25,000 every 6 hours.\n:zap: Rank Boost: **2.5x**\n<:transparent:911319446918955089>", inline=False)
            em.add_field(name="[III] Guardian - :gem: 750,000", value=":star: Gives you :gem: 100,000 every 6 hours.\n:zap: Rank Boost: **3x**\n<:transparent:911319446918955089>", inline=False)
            em.add_field(name="[IV] Elder - :gem: 2,500,000", value=":star: Gives you :gem: 375,000 every 6 hours.\n:zap: Rank Boost: **4x**\n<:transparent:911319446918955089>", inline=False)
            em.add_field(name="[V] Heroic - :gem: 5,000,000", value=":star: Gives you :gem: 500,000 every 6 hours.\n:zap: Rank Boost: **5x**\n<:transparent:911319446918955089>", inline=False)
            em.add_field(name="[VI] Overlord - :gem: 15,000,000", value=":star: Gives you :gem: 1,500,000 every 6 hours.\n:zap: Rank Boost: **6x**\n<:transparent:911319446918955089>", inline=False)
            em.add_field(name="[VII] Daunter - :gem: 30,000,000", value=":star: Gives you :gem: 3,500,000 every 6 hours.\n:zap: Rank Boost: **8x**\n<:transparent:911319446918955089>", inline=False)
            
            em.timestamp = datetime.datetime.utcnow()
            em.set_author(name="Cosmo's Lounge Shop", icon_url=ctx.guild.icon.url)
            em.set_footer(text="Page 1/1")

            await ctx.send(embed=em)

        else:
            return

    @commands.command()
    async def buy(self, ctx, *, item=None):

        id = ctx.author.id
        Economy = eco.find_one({"memberid":id})
        bal = Economy["bal"]
        quest = Economy["currentQuest"]

        if not item:

            await ctx.send("What are you trying to buy?")

        # ------------------------------- #
        # ''' Quest '''
        # ------------------------------- #

        elif item in ['magic potion']:

            if bal >= 50000 and quest == "Amethyst1":

                    em = discord.Embed(title="Quest Completed!",description="Successfully completed Amethyst's quest. Head back to >quest Amethyst to get your next quest.",colour=discord.Colour.from_rgb(95, 255, 95))
                    em.set_author(name=ctx.author, icon_url=ctx.author.display_avatar)
                    em.timestamp = datetime.datetime.utcnow()
                    await ctx.send(embed=em)

                    newBal = bal - 50000
                    eco.update_one({"memberid":id},{"$set":{"bal": newBal}})
                    eco.update_one({"memberid":id},{"$set":{"currentQuest":"Amethyst2"}})

                # If user is too poor
            elif quest != "Amethyst1":
                return

            else:

                em = discord.Embed(description = f"You do not have enough money to buy this item, you need :gem: {(50000-bal):,} more!", colour=discord.Colour.from_rgb(0, 208, 255))
                em.timestamp = datetime.datetime.utcnow()
                em.set_author(name="Purchase Failed", icon_url=ctx.message.guild.icon.url)
                await ctx.send(embed=em)

        # ------------------------------- #
        # ''' Potions '''
        # ------------------------------- #

        elif item in ["damage1", "damage 1"]:

            potion = find(lambda r: r.name == "[⚔️] Damage I", ctx.message.guild.roles)
            price = 100000

            # User does not have a potion
            if potion not in ctx.author.roles:

                if bal >= price:

                    em = discord.Embed(description = "You have bought a Tier 1 **Damage Potion**!", colour=discord.Colour.from_rgb(0, 208, 255))
                    em.timestamp = datetime.datetime.utcnow()
                    em.set_author(name="Purchase Successful", icon_url=ctx.message.guild.icon.url)
                    
                    await ctx.author.add_roles(potion)
                    await ctx.send(embed=em)

                    newBal = bal - price
                    eco.update_one({"memberid":id},{"$set":{"bal": newBal}})
            
            # User already has a potion
            else:
                em = discord.Embed(description = f"You already have a damage potion equipped, enter a boss fight to consume it!", colour=discord.Colour.from_rgb(0, 208, 255))
                em.timestamp = datetime.datetime.utcnow()
                em.set_author(name="Purchase Failed", icon_url=ctx.message.guild.icon.url)
                await ctx.send(embed=em)

        # ------------------------------- #
        # ''' Ranks '''
        # ------------------------------- #

        elif item in ['Apprentice', 'apprentice']:

            rank = find(lambda r: r.name == "[I] Apprentice", ctx.message.guild.roles)
            price = 50000

            # If user has rank
            if rank not in ctx.author.roles:

                if bal >= price:
                    
                    em = discord.Embed(description = "You have bought **[I] Apprentice** rank!", colour=discord.Colour.from_rgb(0, 208, 255))
                    em.timestamp = datetime.datetime.utcnow()
                    em.set_author(name="Purchase Successful", icon_url=ctx.message.guild.icon.url)
                    
                    await ctx.author.add_roles(rank)
                    await ctx.send(embed=em)

                    newBal = bal - price
                    eco.update_one({"memberid":id},{"$set":{"bal": newBal}})

                # If user is too poor
                else:
                    em = discord.Embed(description = f"You do not have enough money to buy this item, you need :gem: {(price-bal):,} more!", colour=discord.Colour.from_rgb(0, 208, 255))
                    em.timestamp = datetime.datetime.utcnow()
                    em.set_author(name="Purchase Failed", icon_url=ctx.message.guild.icon.url)
                    await ctx.send(embed=em)
            
            else:
                em = discord.Embed(description = f"You already own this rank, consider buying a higher tier rank!", colour=discord.Colour.from_rgb(0, 208, 255))
                em.timestamp = datetime.datetime.utcnow()
                em.set_author(name="Purchase Failed", icon_url=ctx.message.guild.icon.url)
                await ctx.send(embed=em)

        elif item in ['Legend', 'legend']:
    
            rank = find(lambda r: r.name == "[II] Legend", ctx.message.guild.roles)
            prev_rank = find(lambda r: r.name == "[I] Apprentice", ctx.message.guild.roles)
            price = 100000

            # If user has rank
            if (rank not in ctx.author.roles) and (prev_rank in ctx.author.roles):

                if bal >= price:
                    
                    em = discord.Embed(description = "You have bought **[II] Legend** rank!", colour=discord.Colour.from_rgb(0, 208, 255))
                    em.timestamp = datetime.datetime.utcnow()
                    em.set_author(name="Purchase Successful", icon_url=ctx.message.guild.icon.url)
                    
                    await ctx.author.add_roles(rank)
                    await ctx.send(embed=em)

                    newBal = bal - price
                    eco.update_one({"memberid":id},{"$set":{"bal": newBal}})

                # If user is too poor
                else:
                    em = discord.Embed(description = f"You do not have enough money to buy this item, you need :gem: {(price-bal):,} more!", colour=discord.Colour.from_rgb(0, 208, 255))                    
                    em.timestamp = datetime.datetime.utcnow()
                    em.set_author(name="Purchase Failed", icon_url=ctx.message.guild.icon.url)
                    await ctx.send(embed=em)

            # User does not have previous rank
            elif prev_rank not in ctx.author.roles:
                em = discord.Embed(description = f"You do not meet the requirements for this rank. Purchase {prev_rank.mention} first!", colour=discord.Colour.from_rgb(0, 208, 255))
                em.timestamp = datetime.datetime.utcnow()
                em.set_author(name="Purchase Failed", icon_url=ctx.message.guild.icon.url)
                await ctx.send(embed=em)
            
            else:
                em = discord.Embed(description = f"You already own this rank, consider buying a higher tier rank!", colour=discord.Colour.from_rgb(0, 208, 255))
                em.timestamp = datetime.datetime.utcnow()
                em.set_author(name="Purchase Failed", icon_url=ctx.message.guild.icon.url)
                await ctx.send(embed=em)

        elif item in ['Guardian', 'guardian']:
    
            rank = find(lambda r: r.name == "[III] Guardian", ctx.message.guild.roles)
            prev_rank = find(lambda r: r.name == "[II] Legend", ctx.message.guild.roles)
            price = 750000

            # If user has rank
            if (rank not in ctx.author.roles) and (prev_rank in ctx.author.roles):

                if bal >= price:
                    
                    em = discord.Embed(description = "You have bought **[III] Guardian** rank!", colour=discord.Colour.from_rgb(0, 208, 255))
                    em.timestamp = datetime.datetime.utcnow()
                    em.set_author(name="Purchase Successful", icon_url=ctx.message.guild.icon.url)
                    
                    await ctx.author.add_roles(rank)
                    await ctx.send(embed=em)

                    newBal = bal - price
                    eco.update_one({"memberid":id},{"$set":{"bal": newBal}})

                # If user is too poor
                else:
                    em = discord.Embed(description = f"You do not have enough money to buy this item, you need :gem: {(price-bal):,} more!", colour=discord.Colour.from_rgb(0, 208, 255))                    
                    em.timestamp = datetime.datetime.utcnow()
                    em.set_author(name="Purchase Failed", icon_url=ctx.message.guild.icon.url)
                    await ctx.send(embed=em)

            # User does not have previous rank
            elif prev_rank not in ctx.author.roles:
                em = discord.Embed(description = f"You do not meet the requirements for this rank. Purchase {prev_rank.mention} first!", colour=discord.Colour.from_rgb(0, 208, 255))
                em.timestamp = datetime.datetime.utcnow()
                em.set_author(name="Purchase Failed", icon_url=ctx.message.guild.icon.url)
                await ctx.send(embed=em)

            else:
                em = discord.Embed(description = f"You already own this rank, consider buying a higher tier rank!", colour=discord.Colour.from_rgb(0, 208, 255))
                em.timestamp = datetime.datetime.utcnow()
                em.set_author(name="Purchase Failed", icon_url=ctx.message.guild.icon.url)
                await ctx.send(embed=em)

        elif item in ['Elder', 'elder']:
    
            rank = find(lambda r: r.name == "[IV] Elder", ctx.message.guild.roles)
            prev_rank = find(lambda r: r.name == "[III] Guardian", ctx.message.guild.roles)
            price = 2500000

            # If user has rank
            if (rank not in ctx.author.roles) and (prev_rank in ctx.author.roles):

                if bal >= price:
                    
                    em = discord.Embed(description = "You have bought **[IV] Elder** rank!", colour=discord.Colour.from_rgb(0, 208, 255))
                    em.timestamp = datetime.datetime.utcnow()
                    em.set_author(name="Purchase Successful", icon_url=ctx.message.guild.icon.url)
                    
                    await ctx.author.add_roles(rank)
                    await ctx.send(embed=em)

                    newBal = bal - price
                    eco.update_one({"memberid":id},{"$set":{"bal": newBal}})

                # If user is too poor
                else:
                    em = discord.Embed(description = f"You do not have enough money to buy this item, you need :gem: {(price-bal):,} more!", colour=discord.Colour.from_rgb(0, 208, 255))                    
                    em.timestamp = datetime.datetime.utcnow()
                    em.set_author(name="Purchase Failed", icon_url=ctx.message.guild.icon.url)
                    await ctx.send(embed=em)

            # User does not have previous rank
            elif prev_rank not in ctx.author.roles:
                em = discord.Embed(description = f"You do not meet the requirements for this rank. Purchase {prev_rank.mention} first!", colour=discord.Colour.from_rgb(0, 208, 255))
                em.timestamp = datetime.datetime.utcnow()
                em.set_author(name="Purchase Failed", icon_url=ctx.message.guild.icon.url)
                await ctx.send(embed=em)
                
            else:
                em = discord.Embed(description = f"You already own this rank, consider buying a higher tier rank!", colour=discord.Colour.from_rgb(0, 208, 255))
                em.timestamp = datetime.datetime.utcnow()
                em.set_author(name="Purchase Failed", icon_url=ctx.message.guild.icon.url)
                await ctx.send(embed=em)

        elif item in ['Heroic', 'heroic']:
    
            rank = find(lambda r: r.name == "[V] Heroic", ctx.message.guild.roles)
            prev_rank = find(lambda r: r.name == "[IV] Elder", ctx.message.guild.roles)
            price = 5000000

            # If user has rank
            if (rank not in ctx.author.roles) and (prev_rank in ctx.author.roles):

                if bal >= price:
                    
                    em = discord.Embed(description = "You have bought **[V] Heroic** rank!", colour=discord.Colour.from_rgb(0, 208, 255))                    
                    em.timestamp = datetime.datetime.utcnow()
                    em.set_author(name="Purchase Successful", icon_url=ctx.message.guild.icon.url)
                    
                    await ctx.author.add_roles(rank)
                    await ctx.send(embed=em)

                    newBal = bal - price
                    eco.update_one({"memberid":id},{"$set":{"bal": newBal}})

                # If user is too poor
                else:
                    em = discord.Embed(description = f"You do not have enough money to buy this item, you need :gem: {(price-bal):,} more!", colour=discord.Colour.from_rgb(0, 208, 255))                    
                    em.timestamp = datetime.datetime.utcnow()
                    em.set_author(name="Purchase Failed", icon_url=ctx.message.guild.icon.url)
                    await ctx.send(embed=em)

            # User does not have previous rank
            elif prev_rank not in ctx.author.roles:
                em = discord.Embed(description = f"You do not meet the requirements for this rank. Purchase {prev_rank.mention} first!", colour=discord.Colour.from_rgb(0, 208, 255))
                em.timestamp = datetime.datetime.utcnow()
                em.set_author(name="Purchase Failed", icon_url=ctx.message.guild.icon.url)
                await ctx.send(embed=em)
                
            else:
                em = discord.Embed(description = f"You already own this rank, consider buying a higher tier rank!", colour=discord.Colour.from_rgb(0, 208, 255))
                em.timestamp = datetime.datetime.utcnow()
                em.set_author(name="Purchase Failed", icon_url=ctx.message.guild.icon.url)
                await ctx.send(embed=em)

        elif item in ['Overlord', 'overlord']:
    
            rank = find(lambda r: r.name == "[VI] Overlord", ctx.message.guild.roles)
            prev_rank = find(lambda r: r.name == "[V] Heroic", ctx.message.guild.roles)
            price = 15000000

            # If user has rank
            if (rank not in ctx.author.roles) and (prev_rank in ctx.author.roles):

                if bal >= price:
                    
                    em = discord.Embed(description = "You have bought **[VI] Overlord** rank!", colour=discord.Colour.from_rgb(0, 208, 255))
                    em.timestamp = datetime.datetime.utcnow()
                    em.set_author(name="Purchase Successful", icon_url=ctx.message.guild.icon.url)
                    
                    await ctx.author.add_roles(rank)
                    await ctx.send(embed=em)

                    newBal = bal - price
                    eco.update_one({"memberid":id},{"$set":{"bal": newBal}})

                else:
                    em = discord.Embed(description = f"You do not have enough money to buy this item, you need :gem: {(price-bal):,} more!", colour=discord.Colour.from_rgb(0, 208, 255))                    
                    em.timestamp = datetime.datetime.utcnow()
                    em.set_author(name="Purchase Failed", icon_url=ctx.message.guild.icon.url)
                    await ctx.send(embed=em)

            # User does not have previous rank
            elif prev_rank not in ctx.author.roles:
                em = discord.Embed(description = f"You do not meet the requirements for this rank. Purchase {prev_rank.mention} first!", colour=discord.Colour.from_rgb(0, 208, 255))
                em.timestamp = datetime.datetime.utcnow()
                em.set_author(name="Purchase Failed", icon_url=ctx.message.guild.icon.url)
                await ctx.send(embed=em)
                
            else:
                em = discord.Embed(description = f"You do not meet the requirements for this rank. Purchase {prev_rank.mention} first!", colour=discord.Colour.from_rgb(0, 208, 255))
                em.timestamp = datetime.datetime.utcnow()
                em.set_author(name="Purchase Failed", icon_url=ctx.message.guild.icon.url)
                await ctx.send(embed=em)

        elif item in ['Daunter', 'daunter']:
    
            rank = find(lambda r: r.name == "[VII] Daunter", ctx.message.guild.roles)
            prev_rank = find(lambda r: r.name == "[VI] Overlord", ctx.message.guild.roles)
            price = 30000000

            # If user has rank
            if (rank not in ctx.author.roles) and (prev_rank in ctx.author.roles):

                if bal >= price:
                    
                    em = discord.Embed(description = "You have bought **[VII] Daunter** rank!", colour=discord.Colour.from_rgb(0, 208, 255))
                    em.timestamp = datetime.datetime.utcnow()
                    em.set_author(name="Purchase Successful", icon_url=ctx.message.guild.icon.url)
                    
                    await ctx.author.add_roles(rank)
                    await ctx.send(embed=em)

                    newBal = bal - price
                    eco.update_one({"memberid":id},{"$set":{"bal": newBal}})

                # If user is too poor
                else:
                    em = discord.Embed(description = f"You do not have enough money to buy this item, you need :gem: {(price-bal):,} more!", colour=discord.Colour.from_rgb(0, 208, 255))                    
                    em.timestamp = datetime.datetime.utcnow()
                    em.set_author(name="Purchase Failed", icon_url=ctx.message.guild.icon.url)
                    await ctx.send(embed=em)

            # User does not have previous rank
            elif prev_rank not in ctx.author.roles:
                em = discord.Embed(description = f"You do not meet the requirements for this rank. Purchase {prev_rank.mention} first!", colour=discord.Colour.from_rgb(0, 208, 255))
                em.timestamp = datetime.datetime.utcnow()
                em.set_author(name="Purchase Failed", icon_url=ctx.message.guild.icon.url)
                await ctx.send(embed=em)
                
            else:
                em = discord.Embed(description = f"You already own this rank, consider buying a higher tier rank!", colour=discord.Colour.from_rgb(0, 208, 255))
                em.timestamp = datetime.datetime.utcnow()
                em.set_author(name="Purchase Failed", icon_url=ctx.message.guild.icon.url)
                await ctx.send(embed=em)
def setup(client):

    client.add_cog(Shop(client))