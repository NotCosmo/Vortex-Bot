import discord
import random
from random import choice
import datetime
from discord.ext import commands
from discord.ext.commands import BucketType
from io import BytesIO
from PIL import Image, ImageFilter, ImageFont, ImageDraw 

class Images(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.cooldown(1, 5, BucketType.user)
    async def wanted(self, ctx, member: discord.Member=None):

        if member is None:
            member = ctx.author

        wanted = Image.open("wanted.jpg")
        asset = member.avatar_url_as(size=128)
        data = BytesIO(await asset.read())
        profilepic = Image.open(data)

        profilepic = profilepic.resize((300, 300))

        wanted.paste(profilepic, (78, 219))
        wanted.save("wantedpic.jpg")

        await ctx.send(file = discord.File("wantedpic.jpg"))

    @wanted.error
    async def wanted_error(self, ctx: commands.Context, error: commands.CommandError):

        if isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(
                description = f"Command is on cooldown, try again after **{round(error.retry_after, 1)}** seconds.",
                colour = discord.Colour.from_rgb(255, 91, 91)
            )
            embed.timestamp = datetime.datetime.utcnow()
            embed.set_author(name=f'Cooldown', icon_url=ctx.author.avatar_url)

            await ctx.send(embed=embed)
    
    @commands.command()
    @commands.cooldown(1, 5, BucketType.user)
    async def rip(self, ctx, member: discord.Member=None):

        if member is None:
            member = ctx.author

        wanted = Image.open("rip.png")
        asset = member.avatar_url_as(size=128)
        data = BytesIO(await asset.read())
        profilepic = Image.open(data)

        profilepic = profilepic.resize((225, 225))

        wanted.paste(profilepic, (244, 276))
        wanted.save("rippic.png")
        await ctx.send(file = discord.File("rippic.png"))

    @rip.error
    async def rip_error(self, ctx: commands.Context, error: commands.CommandError):

        if isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(
                description = f"Command is on cooldown, try again after **{round(error.retry_after, 1)}** seconds.",
                colour = discord.Colour.from_rgb(255, 91, 91)
            )
            embed.timestamp = datetime.datetime.utcnow()
            embed.set_author(name=f'Cooldown', icon_url=ctx.author.avatar_url)

            await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 5, BucketType.user)
    async def ship(self, ctx, user: commands.MemberConverter=None, user2: commands.MemberConverter=None):
        x = random.randint(0, 100)
        str(x)

        if user2 is None:
            user2 = ctx.author
            
            if user is None:
                user = random.choice(ctx.guild.members)
            

        title_font = ImageFont.truetype('coolvetica condensed rg.ttf', 100)
        percent_font = ImageFont.truetype('coolvetica condensed rg.ttf', 175)
        title_text = f"{x}%"
        
        meter = Image.open("ship.png")

        image_editable = ImageDraw.Draw(meter)
        #495, 250
        image_editable.text((515, 250), title_text, (255, 255, 255), font=percent_font)
        image_editable.text((450, 70), "Ship Meter", (255, 255, 255), font=title_font)

        asset = user.avatar_url_as(size=512)
        asset2 = user2.avatar_url_as(size=512)
        data = BytesIO(await asset.read())
        data2 = BytesIO(await asset2.read())
        pic1 = Image.open(data)
        pic2 = Image.open(data2)

        pic1 = pic1.resize((300, 300))
        pic2 = pic2.resize((300, 300))

        pic1.save("pic1.png")
        pic2.save("pic2.png")

        meter.paste(pic1, (24, 225))
        meter.paste(pic2, (876, 224))
        meter.save("meter2.png")
        await ctx.send(f"{user.name} :heart: {user2.name}", file = discord.File("meter2.png"))

    @ship.error
    async def ship_error(self, ctx: commands.Context, error: commands.CommandError):

        if isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(
                description = f"Command is on cooldown, try again after **{round(error.retry_after, 1)}** seconds.",
                colour = discord.Colour.from_rgb(255, 91, 91)
            )
            embed.timestamp = datetime.datetime.utcnow()
            embed.set_author(name=f'Cooldown', icon_url=ctx.author.avatar_url)

            await ctx.send(embed=embed)

        elif isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                description = f"Invalid Arguments: `!ship <user>`.",
                colour = discord.Colour.from_rgb(255, 91, 91)
            )
            embed.timestamp = datetime.datetime.utcnow()
            embed.set_author(name=f'Command Failed', icon_url=ctx.author.avatar_url)

            await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Images(client))