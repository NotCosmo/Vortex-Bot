# Main Imports

import nextcord as discord
import random
import asyncio
import time

# Other

from nextcord.ext import commands
import asyncio
import datetime
from pymongo import MongoClient
from .utils.utils_dict import levels
import PIL
from easy_pil import Canvas, Editor, Font, load_image_async

# ------------------------------- #
''' Cluster '''
# ------------------------------- #

cluster = MongoClient("mongodb+srv://Cosmo:xerZgSrxBcK9H4k@discordprofiles.ghx93.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
database = cluster["Discord"]
db = database["Profiles"]

no_xp_channels = [814787632776609812, 771679224716197899, 842812145791402004]

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

class Levels(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, ctx):

        id = ctx.author.id
        try:

            if ctx.channel.id in no_xp_channels:
                return

            data = db.find_one({"memberid":id})
            user_level = data["level"]
            xp = data["xp"]

        except:
            
            if ctx.author.bot:
                return
            
            db.insert_one(
            {
            "memberid":ctx.author.id,
            "profile_name":"None",
            "profile_desc":"None",
            "level":1,
            "xp":0,
            "background":"",
            })
            return
        
        xp_required = levels[user_level]
        if xp >= xp_required:

            user_level += 1
            db.update_one({"memberid":id},{"$set":{"level": user_level}})
            db.update_one({"memberid":id},{"$set":{"xp": 0}})

            await ctx.channel.send(f"{ctx.author.mention} levelled up to **Level {user_level}**")

        else:

            xp += random.randint(5, 15)
            db.update_one({"memberid":id},{"$set":{"xp": xp}})
            if xp >= xp_required:

                user_level += 1
                db.update_one({"memberid":id},{"$set":{"level": user_level}})
                db.update_one({"memberid":id},{"$set":{"xp": 0}})

                await ctx.channel.send(f"{ctx.author.mention} levelled up to **Level {user_level}**")

    @commands.command(aliases = ['llb'])
    async def ltop(self, ctx):

        embed = discord.Embed(
            description = '',
            colour = discord.Colour.from_rgb(0, 208, 255)
        )

        i = 1
        rankings = db.find().sort("level",-1)
        for x in rankings:
            try:
                temp = ctx.guild.get_member(x["memberid"])
                level = x["level"]
                xp = x["xp"]
                    #embed.add_field(name=f"`[#{i}]` {temp.name}", value=f":gem: {bal:,}", inline=False)

                if temp.id == ctx.author.id:
                    embed.set_footer(text=f"Your Rank: {i}/{len(ctx.guild.members)}")

                if i in [1, 2, 3]:
                    embed.description += f"<:transparent:911319446918955089>\n**#{i}.** {temp.mention} - LVL: {level} ┃ XP: {xp}\n<:transparent:911319446918955089>"
                elif i == 10:
                    embed.description += f"\n#{i}. {temp.mention} - LVL: {level} ┃ XP: {xp}"
                else:
                    embed.description += f"\n#{i}. {temp.mention} - LVL: {level} ┃ XP: {xp}\n"
                i += 1
            except:
                pass
            if i == 11:
                break

        embed.timestamp = datetime.datetime.utcnow()
        embed.set_author(name="Levels Leaderboard", icon_url=ctx.guild.icon.url) 
        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def desc(self, ctx, *, text):

        id = ctx.author.id
        name = ctx.author.name

        try:

            db.update_one({"memberid":id},{"$set":{"profileDesc": text}})
            em = discord.Embed(
                title = "Profile Updated!",
                description = f"Your profile description has been updated! You can do `>profile` to view it!",
                colour = discord.Colour.from_rgb(75, 255, 75)
            )
            em.timestamp = datetime.datetime.utcnow()
            await ctx.reply(embed=em)

        except:
            em = discord.Embed(
                title = "Profile Error",
                description = f"You do not have an active profile, please do `>profile` to create one.",
                colour = discord.Colour.from_rgb(255, 75, 75)
            )
            em.timestamp = datetime.datetime.utcnow()
            await ctx.reply(embed=em)

    @commands.command()
    async def rank(self, ctx):

        try:
            data = db.find_one({"memberid":ctx.author.id})
            user_level = data["level"]
            xp = data["xp"]

        except:
            
            if ctx.author.bot:
                return
            else:

                db.insert_one(
                {
                "memberid":ctx.author.id,
                "profile_name":"None",
                "profile_desc":"None",
                "level":1,
                "xp":0,
                })
                return

        user_data = {
            "name": str(ctx.author),
            "bio": "",
            "level": str(user_level),
            "xp": f"{numformat(xp)} / {numformat(levels[user_level])}",
            "percentage": round((xp/levels[user_level])*100),
        }


        background = Editor(Canvas((800, 240), color="#23272A"))
        profile_image = await load_image_async(str(ctx.author.display_avatar))
        profile = Editor(profile_image).resize((200, 200))


        font_40 = Font.poppins(size=40)
        font_20 = Font.montserrat(size=20)
        font_25 = Font.poppins(size=25)
        font_40_bold = Font.poppins(size=40, variant="bold")

        background.paste(profile, (20, 20))
        background.text((240, 30), user_data["name"], font=font_40, color="white")
        background.text((240, 80), user_data["bio"], font=font_20, color="white")
        background.text((250, 170), "LVL", font=font_25, color="white")
        background.text((310, 160), user_data["level"], font=font_40_bold, color="white")

        background.rectangle((390, 170), 360, 25, outline="white", stroke_width=2)
        background.bar(
            (394, 174),
            352,
            17,
            percentage=user_data["percentage"],
            fill="white",
            stroke_width=2,
        )
        
        i = 1
        rankings = db.find().sort("level",-1)
        for x in rankings:
            try:
                temp = ctx.guild.get_member(x["memberid"])
                #embed.add_field(name=f"`[#{i}]` {temp.name}", value=f":gem: {bal:,}", inline=False)

                if temp.id == ctx.author.id:
                    pos = i
                
                i += 1
            except:
                pass

        background.text((390, 135), f"Rank: #{pos}", font=font_25, color="white")
        background.text(
            (750, 130), f"XP : {user_data['xp']}", font=font_25, color="white", align="right"
        )
        background.text(
            (750, 210), f"{user_data['percentage']}%", font=Font.poppins(size=20), color="white", align="right"
        )

        background.save("level.png")
        await ctx.send(file=discord.File("level.png"))

    @commands.command()
    async def baltest(self, ctx):

        try:
            data = db.find_one({"memberid":ctx.author.id})
            user_level = data["level"]
            xp = data["xp"]

        except:
            
            if ctx.author.bot:
                return
            else:

                db.insert_one(
                {
                "memberid":ctx.author.id,
                "profile_name":"None",
                "profile_desc":"None",
                "level":1,
                "xp":0,
                })
                return

        user_data = {
            "name": str(ctx.author),
            "bio": "",
            "level": str(user_level),
            "xp": f"{numformat(xp)} / {numformat(levels[user_level])}",
            "percentage": round((xp/levels[user_level])*100),
            "title":"Season 13 Champion",
        }


        background = Editor(Canvas((800, 240), color="#23272A"))
        profile_image = await load_image_async(str(ctx.author.display_avatar))
        profile = Editor(profile_image).circle_image().resize((200, 200))


        font_40 = Font.poppins(size=40)
        font_20 = Font.montserrat(size=20)
        font_25 = Font.poppins(size=25)
        font_40_bold = Font.poppins(size=40, variant="bold")
        bold = Font.poppins(size=40, variant="bold")

        background.paste(profile, (20, 20))
        # Username, underline and title
        background.text((375, 30), user_data["name"], font=bold, color="white")
        background.text((375, 80), user_data["title"], font=font_25, color="white")
        background.rectangle((250, 70), 500, 1, outline="white", stroke_width=2)
        #background.text((250, 170), "LVL", font=font_25, color="white")
        #!background.text((310, 160), user_data["level"], font=font_40_bold, color="white")
        background.text((240, 80), "Balance 💎 1.2M", font=font_20, color="white")
        
        background.rectangle((250, 170), 500, 25, outline="white", stroke_width=2)
        background.bar(
            (254, 174),500,17,
            percentage=user_data["percentage"],
            fill="white",
            stroke_width=2,
        )

        background.save("level.png")
        await ctx.send(file=discord.File("level.png"))

def setup(client):
    client.add_cog(Levels(client))