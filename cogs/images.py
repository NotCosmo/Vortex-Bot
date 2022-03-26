import nextcord as discord
from nextcord.ext import commands
from nextcord.ext.commands import BucketType
import random
from random import choice
import datetime
import io
from io import BytesIO
from PIL import Image, ImageFilter, ImageFont, ImageDraw 
import aiohttp

class Images(commands.Cog):

    def __init__(self, client):
        self.client = client

    #https://some-random-api.ml/canvas/color?avatar=https://cdn.discordapp.com/avatars/560789882738573324/bc220b0eeeabbe234026e4881f3c3b9c.png&username=Telk&displayname=Telk&comment=Hello

    @commands.command()
    @commands.cooldown(1, 10, BucketType.user)
    async def lolipolice(self, ctx, member: discord.Member=None):

        if member is None:
            member = ctx.author

        saved = member.avatar.with_format("png")
        embed = discord.Embed(colour=member.colour)

        embed.set_image(url=f"https://some-random-api.ml/canvas/lolice?avatar={saved}")
        embed.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 10, BucketType.user)
    async def hornylicense(self, ctx, member: discord.Member=None):

        if member is None:
            member = ctx.author

        saved = member.avatar.with_format("png")
        embed = discord.Embed(colour=member.colour)

        embed.set_image(url=f"https://some-random-api.ml/canvas/horny?avatar={saved}")
        embed.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 10, BucketType.user)
    async def simpcard(self, ctx, member: discord.Member=None):

        if member is None:
            member = ctx.author

        saved = member.avatar.with_format("png")
        embed = discord.Embed(colour=member.colour)

        embed.set_image(url=f"https://some-random-api.ml/canvas/simpcard?avatar={saved}")
        embed.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 10, BucketType.user)
    async def pixelate(self, ctx, member: discord.Member=None):

        if member is None:
            member = ctx.author

        saved = member.avatar.with_format("png")
        embed = discord.Embed(colour=member.colour)

        embed.set_image(url=f"https://some-random-api.ml/canvas/pixelate?avatar={saved}")
        embed.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 10, BucketType.user)
    async def jail(self, ctx, member: discord.Member=None):

        if member is None:
            member = ctx.author

        saved = member.avatar.with_format("png")
        embed = discord.Embed(colour=member.colour)

        embed.set_image(url=f"https://some-random-api.ml/canvas/jail?avatar={saved}")
        embed.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 10, BucketType.user)
    async def glass(self, ctx, member: discord.Member=None):

        if member is None:
            member = ctx.author

        saved = member.avatar.with_format("png")
        embed = discord.Embed(colour=member.colour)

        embed.set_image(url=f"https://some-random-api.ml/canvas/glass?avatar={saved}")
        embed.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=embed)

    @commands.command(aliases = ['missionsuccess', 'missionpassed'])
    @commands.cooldown(1, 10, BucketType.user)
    async def passed(self, ctx, member: discord.Member=None):

        if member is None:
            member = ctx.author

        saved = member.avatar.with_format("png")
        embed = discord.Embed(colour=member.colour)

        embed.set_image(url=f"https://some-random-api.ml/canvas/passed?avatar={saved}")
        embed.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 10, BucketType.user)
    async def wasted(self, ctx, member: discord.Member=None):

        if member is None:
            member = ctx.author

        saved = member.avatar.with_format("png")
        embed = discord.Embed(colour=member.colour)

        embed.set_image(url=f"https://some-random-api.ml/canvas/wasted?avatar={saved}")
        embed.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 10, BucketType.user)
    async def gaypic(self, ctx, member: discord.Member=None):

        if member is None:
            member = ctx.author

        saved = member.avatar.with_format("png")
        embed = discord.Embed(colour=discord.Colour.random())

        embed.set_image(url=f"https://some-random-api.ml/canvas/gay?avatar={saved}")
        embed.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 5, BucketType.user)
    async def wanted(self, ctx, member: discord.Member=None):

        if member is None:
            member = ctx.author

        wanted = Image.open("wanted.jpg")
        asset = member.avatar.with_format("png")
        data = BytesIO(await asset.read())
        profilepic = Image.open(data)

        profilepic = profilepic.resize((300, 300))

        wanted.paste(profilepic, (78, 219))
        wanted.save("wantedpic.jpg")

        await ctx.send(file = discord.File("wantedpic.jpg"))
    
    @commands.command()
    @commands.cooldown(1, 5, BucketType.user)
    async def rip(self, ctx, member: discord.Member=None):

        if member is None:
            member = ctx.author

        wanted = Image.open("rip.png")
        asset = member.avatar.with_format("png")
        data = BytesIO(await asset.read())
        profilepic = Image.open(data)

        profilepic = profilepic.resize((225, 225))

        wanted.paste(profilepic, (244, 276))
        wanted.save("rippic.png")
        await ctx.send(file = discord.File("rippic.png"))

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

        asset = user.avatar.with_format('png')
        asset2 = user2.avatar.with_format('png')
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

def setup(client):
    client.add_cog(Images(client))