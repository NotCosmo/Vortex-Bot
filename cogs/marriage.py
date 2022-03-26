# Main Imports

import nextcord as discord
import asyncio
import time

# Other

from nextcord.ext import commands
from nextcord.utils import find
from datetime import datetime
from pymongo import MongoClient

# ------------------------------- #
''' Cluster '''
# ------------------------------- #

cluster = MongoClient("mongodb+srv://Cosmo:1H1uqPGjo5CjtHQe@eco.5afje.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
database = cluster["Discord"]
db = database['Marriage']

class Marriage(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def adopt(self, ctx, user: discord.Member=None):

        if user is None:
            return

        else:
            parent_one = ctx.author.id
            parent_one_data = db.find_one({"_id":ctx.author.id})
            parent_two = parent_one_data["spouse"]
            parent_two_data = db.find_one({"_id":parent_two})

            # Update child data
            try:
                child_data = db.find_one({"_id":user.id})
                parents = child_data["parents"]
                parents.append(parent_one)
                parents.append(parent_two)
                db.update_one({"_id":user.id},{"$set":{"parents":parents}})
                # Update data for parent 1

                parent_one_children = parent_one_data['kids']
                parent_two_children = parent_two_data['kids']
                parent_one_children.append(user.id)
                parent_two_children.append(user.id)
                
                db.update_one({"_id":parent_one},{"$set":{"kids":parent_one_children}})
                db.update_one({"_id":parent_two},{"$set":{"kids":parent_two_children}})
                return
                
            except:
                db.insert_one({
                    "_id":user.id,
                    "spouse":"None",
                    "kids":[],
                    "parents":[parent_one, parent_two],
                })

    @commands.command()
    async def marry(self, ctx, user: discord.Member=None):
        
        if db.count_documents({"_id":ctx.author.id}) != 0:
            em = discord.Embed(description = "What are you doing? You're already married!", colour=discord.Colour.from_rgb(255, 75, 75))
            em.set_footer(text="Use !family to check your relationships!")
            return await ctx.send(embed=em)

        if db.count_documents({"_id":user.id}) != 0:
            em = discord.Embed(description = "Appears that person doesn't like you! They're already married!", colour=discord.Colour.from_rgb(255, 75, 75))
            em.set_footer(text="Use !family to check your relationships!")
            return await ctx.send(embed=em)
        
        if user.id == ctx.author.id:
            em = discord.Embed(description = "I get that you're lonely, but you can't marry yourself!", colour=discord.Colour.from_rgb(255, 75, 75))
            em.set_footer(text="Use !family to check your relationships!")
            return await ctx.send(embed=em)

        # write check to see if user is married

        em = discord.Embed(description = f"{user.mention}, {ctx.author.mention} has gone down on one knee and asked you to marry them, do you accept?", colour=discord.Colour.from_rgb(255, 75, 75))
        await ctx.send(embed=em)
        
        def check(m):
            return user.id == m.author.id #To make sure it is the only message author is getting
            
        msg = await self.client.wait_for('message', timeout=60.0, check=check)

        if msg.content.lower() in ['yes', 'i do', 'yes, i do', 'yes i do', 'sure', 'yeah', 'ye', 'yea']:

            if db.count_documents({"_id":ctx.author.id}) == 0:
            # First User
                db.insert_one({
                    "_id":ctx.author.id,
                    "spouse":user.id,
                    "kids":[],
                    "parents":[],
                })

            else:
                db.update_one({"_id":ctx.author.id},{"$set":{"spouse":user.id}})

            if db.count_documents({"_id":user.id}) == 0:

                # second User
                db.insert_one({
                    "_id":user.id,
                    "spouse":ctx.author.id,
                    "kids":[],
                    "parents":[],
                })

            else:
                db.update_one({"_id":user.id},{"$set":{"spouse":ctx.author.id}})
            return await ctx.send('Congrats!')

    @commands.command(aliases = ['relationship'])
    async def family(self, ctx):
        
        data = db.find_one({"_id":ctx.author.id})

        try:
            spouse = ctx.guild.get_member(data["spouse"])
            
            await ctx.send(
                f"**User**: {ctx.author.mention}\n\n**Spouse**:{spouse.mention}"
            )
        except:
            pass

        try:
            parents = data["parents"]
            parent_one = ctx.guild.get_member(parents[0])
            parent_two = ctx.guild.get_member(parents[1])
            await ctx.send(f"{parent_one.mention}, {parent_two.mention}")
        except:
            pass

def setup(client):
    client.add_cog(Marriage(client))