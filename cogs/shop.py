# Main Imports

import nextcord as discord
import asyncio
import time

# Other

from nextcord.ext import commands
from nextcord.ext.commands import BucketType
from nextcord.utils import get
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

class Shop(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.users = users
        self.settings = settings
        self.shop = shop

    async def convert_amount(self, amount: str) -> int:

        if amount == "0":
            return 0

        if "e" in amount:
            _s = amount.split("e")
            amount = int(_s[0]) * (10 ** int(_s[1]))

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

    # Get and return item object
    async def get_item(self, item_name: str) -> None:

        item = self.shop.find_one({"item_name": item_name})
        return item

    async def get_user(self, user: discord.Member) -> None:

        user = self.users.find_one({"_id": user.id})
        return user

    # Get and return role object
    async def get_role_id(self, ctx, role_id) -> None:

        role = get(ctx.guild.roles, id=role_id)
        return role

    async def get_role_name(self, ctx, role_name: str) -> discord.Role:

        role = get(ctx.guild.roles, name=role_name)
        return role

    # Get and return settings object
    async def get_settings(self) -> None:

        settings_ = self.settings.find_one({"_id": "settings"})
        return settings_

    async def get_item(self, item_name: str) -> None:

        for data in self.shop.find().sort("_id", 1):
            if item_name.lower() in data["item_name"].lower():
                return data
        return None

    async def update_bal(self, user_: discord.Member, amount: int) -> None:

        user = await self.get_user(user_)
        user["balance"] += amount
        return self.users.replace_one({"_id": user_.id}, user)

    # Message checker
    async def check_message(self, ctx):

        check = lambda m: m.author == ctx.author and m.channel == ctx.channel
        try:
            message = await self.client.wait_for('message', check=check, timeout=15.0)
            if "<@&" in message.content:
                return int(message.content[3:-1])
        except asyncio.TimeoutError:
            return None

        return message

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

        settings_ = await self.get_settings()
        currency = settings_["currency"]
        embed = discord.Embed(title="Shop", description=f"You can buy different ranks and other items with {currency}", colour=discord.Colour.from_rgb(0, 208, 255))
        for data in self.shop.find().sort("_id", 1):

            item = await self.get_item(data["item_name"])
            if page == 1:
                # Only display first 10 items (id 1-10)
                if item["_id"] <= 9:

                    item_name = item["item_name"]
                    item_price = item["item_price"]
                    item_desc = item["item_desc"]
                    embed.add_field(name=f"<:transparent:911319446918955089>\n{item_name} - {currency} {numformat(item_price)}", value=f"{item_desc}", inline=False)
                elif item["_id"] >= 9:
                    pass
            elif page == 2:
                # Only display first 10 items (id 1-10)
                if item["_id"] <= 19:

                    item_name = item["item_name"]
                    item_price = item["item_price"]
                    item_desc = item["item_desc"]
                    embed.add_field(name=f"<:transparent:911319446918955089>\n{item_name} - {currency} {numformat(item_price)}", value=f"{item_desc}", inline=False)
                elif item["_id"] >= 19:
                    pass

        await ctx.send(embed=embed)

    @commands.command(name="buyitem", aliases=["buy"])
    async def buyitem(self, ctx, item_name: str):

        item_not_found = discord.Embed(description=f"Could not find that item in the shop, please try again.", colour=discord.Colour.from_rgb(255, 75, 75))
        item_not_found.set_footer(text="You can also use the shop command to see all items")
        user_not_found = discord.Embed(description=":exclamation: You need an account to play eco. Type `!start` to create one.",colour=discord.Colour.from_rgb(0, 208, 255))
        user_not_found.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar)
        user_not_found.timestamp = datetime.utcnow()
        
        settings_ = await self.get_settings()
        currency = settings_["currency"]
        user = await self.get_user(ctx.author)

        item = await self.get_item(item_name)
        if item is None: return await ctx.send(f"{ctx.author.mention} Item not found.")
        if user is None: return await ctx.send(f"{ctx.author.mention} You are not registered.")

        if item["item_price"] > user["balance"]:
            embed = discord.Embed(description=f"You need {currency} {numformat(item['item_price'] - user['balance'])} more to buy this item.", colour=discord.Colour.from_rgb(255, 75, 75))
            return await ctx.reply(embed=embed, mention_author=False)

        if item["item_role"]:
            role = await self.get_role_name(ctx, item["item_role"])
            if role in ctx.author.roles:
                embed = discord.Embed(description=f"You already have this role.", colour=discord.Colour.from_rgb(255, 75, 75))
                return await ctx.reply(embed=embed, mention_author=False)
            await ctx.author.add_roles(role)

        await self.update_bal(ctx.author, -item["item_price"])
        embed = discord.Embed(description=f"You have bought {item['item_name']} for {currency} {numformat(item['item_price'])}", colour=discord.Colour.from_rgb(75, 255, 75))
        embed.set_author(name="Item Bought", icon_url=ctx.author.display_avatar)
        embed.timestamp = datetime.utcnow()
        return await ctx.reply(embed=embed, mention_author=False)

    @commands.command(name="createitem", aliases=["ci", "create"])
    @commands.has_permissions(administrator=True)
    async def create_item(self, ctx):

        st = await self.get_settings()
        currency = st["currency"]

        timeout_embed = discord.Embed(title="Timeout", description="Command cancelled, you took too long.", colour=discord.Colour.from_rgb(255, 75, 75))
        timeout_embed.timestamp = datetime.utcnow()

        embed = discord.Embed(colour=discord.Colour.from_rgb(0, 208, 255))
        embed.set_author(name="Item Creator", icon_url=ctx.author.display_avatar)
        embed.timestamp = datetime.utcnow()

        embed.add_field(name="Item Name", value="?", inline=True)
        original = await ctx.send(embed=embed)
        item_name = await self.check_message(ctx)
        if item_name is None: return await ctx.send(embed=timeout_embed)
        embed.remove_field(0)
        embed.add_field(name="Item Name", value=item_name.content, inline=True)
        await original.edit(embed=embed)

        embed.add_field(name="Item Price", value="?", inline=True)
        await original.edit(embed=embed)
        _price = await self.check_message(ctx)
        if _price is None: return await ctx.send(embed=timeout_embed)
        item_price = await self.convert_amount(_price.content)
        embed.remove_field(1)
        embed.add_field(name="Item Price", value=f"{currency} {item_price}", inline=True)
        await original.edit(embed=embed)

        embed.add_field(name="Item Description", value="?", inline=True)
        await original.edit(embed=embed)
        item_desc = await self.check_message(ctx)
        if item_desc is None: return await ctx.send(embed=timeout_embed)
        embed.remove_field(2)
        embed.add_field(name="Item Description", value=item_desc.content, inline=True)
        await original.edit(embed=embed)

        embed.add_field(name="Role Assigned", value="?", inline=True)
        await original.edit(embed=embed)
        _role = await self.check_message(ctx)
        if _role is None: return await ctx.send(embed=timeout_embed)
        item_role = await self.get_role_name(ctx, _role.content) # Get role object
        embed.remove_field(3)
        embed.add_field(name="Role Assigned", value=item_role.mention, inline=True)
        await original.edit(embed=embed)

        return self.shop.insert_one({
            "_id": self.shop.count_documents({}),
            "item_name": item_name.content,
            "item_price": item_price,
            "item_desc": item_desc.content,
            "item_role": item_role.name
        })

    @commands.command(name="iteminfo", aliases=["ii", "iinfo"])
    async def item_info(self, ctx, *, item_name: str):
        """
        Get information about an item.
        """
        st = await self.get_settings()
        currency = st["currency"]

        for data in self.shop.find().sort("_id",-1):

            item = await self.get_item(data["item_name"])
            if item is None:
                return await ctx.send(f"Item `{item_name}` not found.")
            if item_name.lower() in item["item_name"].lower():
                embed = discord.Embed(colour=discord.Colour.from_rgb(0, 208, 255))
                embed.set_author(name=item["item_name"], icon_url=ctx.author.display_avatar)
                embed.timestamp = datetime.utcnow()
                embed.add_field(name="Item Price", value=f"{currency} {item['item_price']:,}", inline=False)
                embed.add_field(name="Item Description", value=item["item_desc"], inline=False)
                embed.add_field(name="Role Assigned", value=await self.get_role_name(ctx, item["item_role"]), inline=False)
                return await ctx.send(embed=embed)
            else: continue

    
    @commands.command(name="deleteitem", aliases=["di", "delete"])
    @commands.has_permissions(administrator=True)
    async def delete_item(self, ctx, item_name: str):
        
        for data in self.shop.find().sort("_id", 1):

            item = await self.get_item(data["item_name"])
            if item is None: continue
            if item_name.lower() in item["item_name"].lower():
                n = item["item_name"]
                await ctx.send(f"Item {n} deleted.")
                return self.shop.delete_one({"_id": data["_id"]})

def setup(client):
    client.add_cog(Shop(client))