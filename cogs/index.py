# Main Imports

import nextcord as discord
import random
import asyncio
import time

# Other

from nextcord.ext import commands
from nextcord.ext.commands import BucketType
from nextcord.utils import find
from datetime import datetime
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

class Index(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def index(self, ctx):

        cursed_staff = find(lambda r: r.name == "✧ Cursed Staff", ctx.message.guild.roles)
        raven_dagger = find(lambda r: r.name == "✪ Raven's Dagger", ctx.message.guild.roles)
        darkness_amulet = find(lambda r: r.name == "✪ Darkness Amulet", ctx.message.guild.roles)

        em = discord.Embed(description="Test description",colour=discord.Colour.from_rgb(0, 208, 255))

        if cursed_staff in ctx.author.roles:
            emoji1 = ":white_check_mark:"
        else:
            emoji1 = ":x:"
        em.add_field(name="Raven's Minion (T1)",value=f"{emoji1} - Cursed Staff\n<:transparent:911319446918955089>",inline=False)

        if raven_dagger in ctx.author.roles:
            emoji1 = ":white_check_mark:"
        else:
            emoji1 = ":x:"

        if darkness_amulet in ctx.author.roles:
            emoji2 = ":white_check_mark:"
        else:
            emoji2 = ":x:"
        em.add_field(name="Raven's Follower (T2)",value=f"{emoji1} - Raven's Dagger\n{emoji2} - Darkness Amulet\n\n<:transparent:911319446918955089>",inline=False)

        await ctx.send(embed=em)

def setup(client):
    client.add_cog(Index(client))