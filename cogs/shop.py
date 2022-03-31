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

# ------------------------------- #
''' Cluster '''
# ------------------------------- #

cluster = MongoClient(
    "mongodb+srv://Cosmo:1H1uqPGjo5CjtHQe@eco.5afje.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
database = cluster["Discord"]
users = database["Users"]
shop = database["Shop"]
settings = database["EcoSettings"]

class Shop(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.users = users
        self.settings = settings
        self.shop = shop

    # Get and return item object
    async def get_item(self, item_name: str) -> None:

        item = self.shop.find_one({"item_name": item_name})
        return item

    async def get_settings(self) -> None:

        settings_ = self.settings.find_one({"_id": "settings"})
        return settings_

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def shopinit(self, ctx):

        self.shop.insert_one({
            "_id": 1,
            "item_name": "Second Item",
            "item_price": 200,
            "item_desc": "This is the second item in the shop",
            "item_role": "Test Role2",
        })

    @commands.command(name="shop")
    async def shop(self, ctx, page: int = 1):

        embed = discord.Embed()
        settings_ = await self.get_settings()
        currency = settings_["currency"]
        for data in self.shop.find().sort("_id",1):

            item = await self.get_item(data["item_name"])
            if page == 1:
                if item["_id"] <= 9:
    
                    item_name = item["item_name"]
                    item_price = item["item_price"]
                    item_desc = item["item_desc"]
                    embed.add_field(name=f"{item_name} - {currency} {item_price}", value=f"{item_desc}\n<:transparent:911319446918955089>", inline=False)
                elif item["_id"] >= 9:
                    pass 

        await ctx.send(embed=embed)
            
def setup(client):
    client.add_cog(Shop(client))