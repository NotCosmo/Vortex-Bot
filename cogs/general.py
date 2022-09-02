# Main Imports

import nextcord as discord
import datetime
import asyncio
import random
import aiohttp
import typing

# Side Imports

from nextcord.ext import commands
from nextcord import Spotify
from nextcord.ext.commands import BucketType
from nextcord.utils import find
import math
#from pymongo import MongoClient

#cluster = MongoClient("mongodb+srv://Cosmo:1H1uqPGjo5CjtHQe@eco.5afje.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
#database = cluster["Discord"]
#levels = database["Levels"]

def xp_required(level: int) -> int:
    return 500 + (level - 1) * 250

def can_level_up(user_xp: int, user_level: int) -> bool:

    if user_xp >= 500 + (user_level - 1) * 250:
        return True
    else:
        return False

def xp_until(level: int, next_level: int):

    total_xp = 0
    while level < next_level:
        total_xp += xp_required(level)
        level += 1
    return total_xp

class General(commands.Cog, description="General commands"):

    def __init__(self, client):
        self.client = client

    async def type_check(self, input) -> None:

        if input == typing.Union[str, None]:
            return None
        return input

    def time_convert(self, time):
        if time[-1] == "m":
            return int(time[:-1]) * 60
        elif time[-1] == "h":
            return int(time[:-1]) * 3600
        elif time[-1] == "d":
            return int(time[:-1]) * 86400
        elif time[-1] == "w":
            return int(time[:-1]) * 604800
        elif time[-1] == "y":
            return int(time[:-1]) * 31536000
        else:
            return int(time[:-1])

    @commands.command()
    async def ping(self, ctx):
        ping = round(self.client.latency * 1000)

        embed = discord.Embed(
            title=":ping_pong: Pong!",
            description=f'**Bot Ping**: {ping}ms',
            colour=discord.Colour.from_rgb(0, 208, 255)
        )

        embed.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=embed)

    @commands.command()
    async def poll(
            self, ctx,
            title: str,
            a: str,
            b: str,
            c: str = typing.Optional[str],
            d: str = typing.Optional[str],
    ):

        embed = discord.Embed(title=title, description=f":regional_indicator_a: {a}\n\n:regional_indicator_b: {b}", colour=discord.Colour.from_rgb(0, 208, 255))

        if await self.type_check(c) is not None:
            embed.description += f"\n\n:regional_indicator_c: {c}"
            if await self.type_check(d) is not None:
                embed.description += f"\n\n:regional_indicator_d: {d}"

        embed.timestamp = datetime.datetime.utcnow()
        embed.set_footer(text=f"Poll by {ctx.author}")
        await ctx.message.delete()
        m = await ctx.send(embed=embed)
        await m.add_reaction('🇦')
        await m.add_reaction('🇧')
        if await self.type_check(c) is not None:
            await m.add_reaction('🇨')
            if await self.type_check(d) is not None:
                await m.add_reaction('🇩')

    @commands.command(
        name="bonk",
        aliases=["remindme", "remind"],
        description="Set a reminder to yourself for a certain time",
    )
    async def bonk(self, ctx, time: str, *, message: str = None):

        # convert time to seconds
        time = self.time_convert(time)

        # current time in timestamp
        current_time = datetime.datetime.utcnow().timestamp()

        # time to remind in timestamp
        time_to_remind = current_time + time

        if not message:
            try:
                # get the message author replied to
                message = ctx.message.reference.jump_url
                await ctx.reply(f":white_check_mark: ┃ Reminder set for <t:{int(time_to_remind)}:R>")
                await asyncio.sleep(time)
                return await ctx.reply(f":white_check_mark: ┃ Reminder set <t:{int(current_time)}:R>: {message}")
            except:
                return await ctx.reply(":x: ┃ You need to specify a message (or reply to a message) to remind you of!")

        await ctx.reply(f":white_check_mark: ┃ Reminder set for <t:{int(time_to_remind)}:R>")
        await asyncio.sleep(time)
        return await ctx.reply(f":white_check_mark: ┃ Reminder set <t:{int(current_time)}:R>: {message}")

    @commands.command()
    @commands.cooldown(1, 10, BucketType.user)
    async def encode(self, ctx, *, message):

        async with aiohttp.ClientSession() as cs:
            async with cs.get(f"https://some-random-api.ml/binary?encode={message}") as r:
                data = await r.json()
                text = data["binary"]

                embed = discord.Embed(
                    description=f":white_check_mark: | Encoded Data: **{text}**",
                    colour=discord.Colour.from_rgb(0, 208, 255)
                )
                embed.set_author(name="Binary Encoder", icon_url=ctx.author.avatar.url)
                embed.timestamp = datetime.datetime.utcnow()
                await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 10, BucketType.user)
    async def decode(self, ctx, *, message):

        async with aiohttp.ClientSession() as cs:
            async with cs.get(f"https://some-random-api.ml/binary?decode={message}") as r:
                data = await r.json()
                text = data["text"]

                embed = discord.Embed(
                    description=f":white_check_mark: | Encoded Data: **{text}**",
                    colour=discord.Colour.from_rgb(0, 208, 255)
                )
                embed.set_author(name="Binary Decoder", icon_url=ctx.author.avatar.url)
                embed.timestamp = datetime.datetime.utcnow()
                await ctx.send(embed=embed)

    @commands.command()
    async def astronomy(self, ctx):
        async with ctx.channel.typing():
            async with aiohttp.ClientSession() as cs:
                async with cs.get("https://www.reddit.com/r/Astronomy.json") as r:
                    res = await r.json()
            url = res['data']['children'][random.randint(0, 50)]['data']['url']

        em = discord.Embed(description='Random picture from r/astronomy!', colour=discord.Colour.from_rgb(127, 0, 255))
        em.timestamp = datetime.datetime.utcnow()
        em.set_author(name=ctx.author, icon_url=ctx.author.display_avatar)
        em.set_image(url=url)
        await ctx.reply(embed=em, mention_author=False)

    @commands.command(aliases=['source', 'git', 'gh'])
    @commands.cooldown(1, 10, BucketType.user)
    async def github(self, ctx):
        await ctx.send(":white_check_mark: ┃ You can find my source code on Github through this link: https://github.com/NotCosmo/Vortex")

    @commands.command(aliases=['si'])
    @commands.cooldown(1, 10, BucketType.user)
    async def serverinfo(self, ctx):
        name = str(ctx.guild.name)
        description = str(ctx.guild.description)

        owner = 'cosmo.#5056'
        id = str(ctx.guild.id)
        region = str(ctx.guild.region)
        memberCount = str(ctx.guild.member_count)

        icon = ctx.guild.icon.url

        embed = discord.Embed(
            title=name + " Server Information",
            description=description,
            colour=discord.Colour.random()
        )
        embed.set_thumbnail(url=icon)
        embed.add_field(name="Owner", value=owner, inline=True)
        embed.add_field(name="Server ID", value=id, inline=True)
        embed.add_field(name="Region", value=region, inline=True)
        embed.add_field(name="Member Count", value=memberCount, inline=True)

        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 3, BucketType.user)
    async def qotd(self, ctx, toggle="on"):

        role = discord.utils.find(lambda r: r.name == 'QOTD', ctx.message.guild.roles)

        if toggle == "on" and role not in ctx.author.roles:

            embed = discord.Embed(
                title="Toggled On!",
                description=":thumbsup: Successfully toggled QOTD Pings `on`.",
                colour=discord.Colour.from_rgb(95, 255, 95)
            )
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=embed)
            await ctx.author.add_roles(role)

        elif toggle == "on" and role in ctx.author.roles:

            embed = discord.Embed(
                title="Role Error",
                description="You already have QOTD Pings enabled!",
                colour=discord.Colour.from_rgb(255, 75, 55)
            )
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=embed)

        if toggle == "off" and role not in ctx.author.roles:

            embed = discord.Embed(
                title="Command Error",
                description="You do not have QOTD Pings enabled!",
                colour=discord.Colour.from_rgb(255, 75, 75)
            )
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=embed)

        elif toggle == "off" and role in ctx.author.roles:

            embed = discord.Embed(
                title="Toggled Off!",
                description=":thumbsup: Successfully toggled QOTD Pings `off`.",
                colour=discord.Colour.from_rgb(95, 255, 95)
            )
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=embed)
            await ctx.author.remove_roles(role)

    @commands.command()
    @commands.cooldown(1, 3, BucketType.user)
    async def youtube(self, ctx, toggle="on"):

        role = discord.utils.find(lambda r: r.name == 'YouTube', ctx.message.guild.roles)

        if toggle == "on" and role not in ctx.author.roles:

            embed = discord.Embed(
                title="Toggled On!",
                description=":thumbsup: Successfully toggled YT Pings `on`.",
                colour=discord.Colour.from_rgb(95, 255, 95)
            )
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=embed)
            await ctx.author.add_roles(role)

        elif toggle == "on" and role in ctx.author.roles:

            embed = discord.Embed(
                title="Role Error",
                description="You already have YT Pings enabled!",
                colour=discord.Colour.from_rgb(255, 75, 55)
            )
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=embed)

        if toggle == "off" and role not in ctx.author.roles:

            embed = discord.Embed(
                title="Command Error",
                description="You do not have YT Pings enabled!",
                colour=discord.Colour.from_rgb(255, 75, 75)
            )
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=embed)

        elif toggle == "off" and role in ctx.author.roles:

            embed = discord.Embed(
                title="Toggled Off!",
                description=":thumbsup: Successfully toggled YT Pings `off`.",
                colour=discord.Colour.from_rgb(95, 255, 95)
            )
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=embed)
            await ctx.author.remove_roles(role)

    @commands.command()
    @commands.cooldown(1, 3, BucketType.user)
    async def fotd(self, ctx, toggle="on"):

        role = discord.utils.find(lambda r: r.name == 'FOTD', ctx.message.guild.roles)

        if toggle == "on" and role not in ctx.author.roles:

            embed = discord.Embed(
                title="Toggled On!",
                description=":thumbsup: Successfully toggled FOTD Pings `on`.",
                colour=discord.Colour.from_rgb(95, 255, 95)
            )
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=embed)
            await ctx.author.add_roles(role)

        elif toggle == "on" and role in ctx.author.roles:

            embed = discord.Embed(
                title="Role Error",
                description="You already have FOTD Pings enabled!",
                colour=discord.Colour.from_rgb(255, 75, 55)
            )
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=embed)

        if toggle == "off" and role not in ctx.author.roles:

            embed = discord.Embed(
                title="Command Error",
                description="You do not have FOTD Pings enabled!",
                colour=discord.Colour.from_rgb(255, 75, 75)
            )
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=embed)

        elif toggle == "off" and role in ctx.author.roles:

            embed = discord.Embed(
                title="Toggled Off!",
                description=":thumbsup: Successfully toggled FOTD Pings `off`.",
                colour=discord.Colour.from_rgb(95, 255, 95)
            )
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=embed)
            await ctx.author.remove_roles(role)

    @commands.command(aliases=["avatar"])
    @commands.cooldown(1, 3, BucketType.user)
    async def av(self, ctx, user: discord.Member = None):

        embed = discord.Embed(
            colour=ctx.author.colour
        )

        if user is None:
            embed.set_image(url=ctx.author.display_avatar)

        else:
            embed.set_image(url=user.display_avatar)

        await ctx.send(embed=embed)

    @commands.command(aliases=["whois"])
    async def userinfo(self, ctx, *, user: discord.Member = None):  # b'\xfc'
        if user is None:
            user = ctx.author
        date_format = "%a, %d %b %Y %I:%M %p"

        embed = discord.Embed(
            colour=user.colour,
            description=user.mention
        )
        embed.set_author(name=str(user), icon_url=user.display_avatar)
        embed.set_thumbnail(url=user.display_avatar)

        if user.activity:
            activity = user.activity.name
        else:
            activity = "None"

        embed.add_field(name="Joined Server", value=f'`{user.joined_at.strftime(date_format)}`')
        embed.add_field(name="Account Creation", value=f'`{user.created_at.strftime(date_format)}`')
        embed.add_field(name="User Status", value=f"{activity}", inline=False)

        if len(user.roles) > 1:
            role_string = ' '.join([r.mention for r in user.roles][1:])
            embed.add_field(name="Roles [{}]\n \n".format(len(user.roles) - 1), value=role_string, inline=False)

        embed.set_footer(text='ID: ' + str(user.id))
        embed.timestamp = datetime.datetime.utcnow()
        return await ctx.send(embed=embed)

    @commands.command()
    async def spotify(self, ctx, user: discord.Member = None):

        if user is None:
            user = ctx.author

        else:
            user = user

        for activity in user.activities:
            if isinstance(activity, Spotify):

                em = discord.Embed(
                    title=f"Listening to {activity.title}..",
                    description=f"Track ID: {activity.track_id}",
                    colour=discord.Colour.from_rgb(30, 215, 96)
                )

                _artists = activity.artists
                artists = ""
                for i in _artists:
                    artists += i + ", "

                em.set_thumbnail(url=activity.album_cover_url)
                em.add_field(name="Artists", value=artists, inline=True)
                em.add_field(name="Album", value=activity.album, inline=True)
                em.add_field(name="Track Url", value=activity.track_url, inline=False)
                em.set_footer(text=f"{user.name}'s Spotify", icon_url=user.avatar.url)
                em.timestamp = datetime.datetime.utcnow()

                await ctx.send(embed=em)

    @commands.command(aliases=["colorlist", "colors", "colours"])
    async def colourlist(self, ctx):
        em = discord.Embed(
            title="Colour List",
            description="Use the command `>colour [id]` to select a colour!",
            colour=discord.Colour.from_rgb(0, 208, 255)
        )

        em.description += "\n\n1. <@&914028003904851988> - Red"
        em.description += "\n\n2. <@&914028022116548630> - Carmine"
        em.description += "\n\n3. <@&914028019826458715> - Rose Red"
        em.description += "\n\n4. <@&914028026747027476> - Orange"
        em.description += "\n\n5. <@&914028012876492871> - Dark Orange"
        em.description += "\n\n6. <@&914028024716988476> - Coral"
        em.description += "\n\n7. <@&914028017850933309> - Gold"
        em.description += "\n\n8. <@&914028031033634876> - Yellow"
        em.description += "\n\n9. <@&914028028852588584> - Light Yellow"
        em.description += "\n\n10. <@&914028037291536404> - Lime"
        em.description += "\n\n11. <@&914028033013346374> - Forest Green"
        em.description += "\n\n12. <@&914028043968864267> - Light Green"
        em.description += "\n\n13. <@&914028039485153280> - Sea Cyan"
        em.description += "\n\n14. <@&914028042299531354> - Teal"
        em.description += "\n\n15. <@&914028035215351848> - Aqua"
        em.description += "\n\n16. <@&914028015439192135> - Deep Sky"
        em.description += "\n\n17. <@&914031531012542504> - Indigo"
        em.description += "\n\n18. <@&914031523320168458> - Purple"
        em.description += "\n\n19. <@&914031520430309437> - Medium Purple"
        em.description += "\n\n20. <@&914031529217364018> - Hot Pink"
        em.description += "\n\n21. <@&914032029992124417> - Pink"
        em.description += "\n\n22. <@&914032028159209562> - Light Pink"
        em.description += "\n\n23. <@&914032033943138344> - White"
        em.description += "\n\n24. <@&914032034756841493> - Black"
        await ctx.send(embed=em)

        @commands.command(aliases=["colorlist", "colors", "colours"])
        async def colourlist(self, ctx):
            em = discord.Embed(
                title="Colour List",
                description="Use the command `>colour [id]` to select a colour!",
                colour=discord.Colour.from_rgb(0, 208, 255)
            )

            em.description += "\n\n1. <@&914028003904851988> - Red"
            em.description += "\n\n2. <@&914028022116548630> - Carmine"
            em.description += "\n\n3. <@&914028019826458715> - Rose Red"
            em.description += "\n\n4. <@&914028026747027476> - Orange"
            em.description += "\n\n5. <@&914028012876492871> - Dark Orange"
            em.description += "\n\n6. <@&914028024716988476> - Coral"
            em.description += "\n\n7. <@&914028017850933309> - Gold"
            em.description += "\n\n8. <@&914028031033634876> - Yellow"
            em.description += "\n\n9. <@&914028028852588584> - Light Yellow"
            em.description += "\n\n10. <@&914028037291536404> - Lime"
            em.description += "\n\n11. <@&914028033013346374> - Forest Green"
            em.description += "\n\n12. <@&914028043968864267> - Light Green"
            em.description += "\n\n13. <@&914028039485153280> - Sea Cyan"
            em.description += "\n\n14. <@&914028042299531354> - Teal"
            em.description += "\n\n15. <@&914028035215351848> - Aqua"
            em.description += "\n\n16. <@&914028015439192135> - Deep Sky"
            em.description += "\n\n17. <@&914031531012542504> - Indigo"
            em.description += "\n\n18. <@&914031523320168458> - Purple"
            em.description += "\n\n19. <@&914031520430309437> - Medium Purple"
            em.description += "\n\n20. <@&914031529217364018> - Hot Pink"
            em.description += "\n\n21. <@&914032029992124417> - Pink"
            em.description += "\n\n22. <@&914032028159209562> - Light Pink"
            em.description += "\n\n23. <@&914032033943138344> - White"
            em.description += "\n\n24. <@&914032034756841493> - Black"
            await ctx.send(embed=em)

    @commands.command(aliases=["color", "Colour", "Color"])
    async def colour(self, ctx, *, id: str):

        names = [
            "Red", "Carmine", "Rose Red", "Orange", "Dark Orange", "Coral", "Gold", "Yellow", "Light Yellow", "Lime", "Forest Green", "Light Green", "Sea Cyan", "Teal", "Aqua", "Deep Sky", "Indigo", "Purple", "Medium Purple", "Hot Pink",
            "Pink", "Light Pink", "White", "Black"
        ]

        for name in names:

            role = find(lambda r: r.name == name, ctx.message.guild.roles)
            if role in ctx.author.roles:
                await ctx.author.remove_roles(role)
            else:
                pass

        if id in ["1", "Red", "red"]:
            role = find(lambda r: r.name == names[0], ctx.message.guild.roles)
            await ctx.author.add_roles(role)
            em = discord.Embed(description=f"Colour set to {role.mention}!", colour=discord.Colour.from_rgb(0, 208, 255))
            em.timestamp = datetime.datetime.utcnow()
            await ctx.reply(embed=em, mention_author=False)

        elif id in ["2", "Carmine", "carmine"]:
            role = find(lambda r: r.name == names[1], ctx.message.guild.roles)
            await ctx.author.add_roles(role)
            em = discord.Embed(description=f"Colour set to {role.mention}!", colour=discord.Colour.from_rgb(0, 208, 255))
            em.timestamp = datetime.datetime.utcnow()
            await ctx.reply(embed=em, mention_author=False)

        elif id in ["3", "Rose Red", "rose red", "Rose red"]:
            role = find(lambda r: r.name == names[2], ctx.message.guild.roles)
            await ctx.author.add_roles(role)
            em = discord.Embed(description=f"Colour set to {role.mention}!", colour=discord.Colour.from_rgb(0, 208, 255))
            em.timestamp = datetime.datetime.utcnow()
            await ctx.reply(embed=em, mention_author=False)

        elif id in ["4", "Orange", "orange"]:
            role = find(lambda r: r.name == names[3], ctx.message.guild.roles)
            await ctx.author.add_roles(role)
            em = discord.Embed(description=f"Colour set to {role.mention}!", colour=discord.Colour.from_rgb(0, 208, 255))
            em.timestamp = datetime.datetime.utcnow()
            await ctx.reply(embed=em, mention_author=False)

        elif id in ["5", "dark orange", "Dark orange", "Dark Orange"]:
            role = find(lambda r: r.name == names[4], ctx.message.guild.roles)
            await ctx.author.add_roles(role)
            em = discord.Embed(description=f"Colour set to {role.mention}!", colour=discord.Colour.from_rgb(0, 208, 255))
            em.timestamp = datetime.datetime.utcnow()
            await ctx.reply(embed=em, mention_author=False)

        elif id in ["6", "Coral", "coral"]:
            role = find(lambda r: r.name == names[5], ctx.message.guild.roles)
            await ctx.author.add_roles(role)
            em = discord.Embed(description=f"Colour set to {role.mention}!", colour=discord.Colour.from_rgb(0, 208, 255))
            em.timestamp = datetime.datetime.utcnow()
            await ctx.reply(embed=em, mention_author=False)

        elif id in ["7", "Gold", "gold"]:
            role = find(lambda r: r.name == names[6], ctx.message.guild.roles)
            await ctx.author.add_roles(role)
            em = discord.Embed(description=f"Colour set to {role.mention}!", colour=discord.Colour.from_rgb(0, 208, 255))
            em.timestamp = datetime.datetime.utcnow()
            await ctx.reply(embed=em, mention_author=False)

        elif id in ["8", "Yellow", "yellow"]:
            role = find(lambda r: r.name == names[7], ctx.message.guild.roles)
            await ctx.author.add_roles(role)
            em = discord.Embed(description=f"Colour set to {role.mention}!", colour=discord.Colour.from_rgb(0, 208, 255))
            em.timestamp = datetime.datetime.utcnow()
            await ctx.reply(embed=em, mention_author=False)

        elif id in ["9", "Light Yellow", "light yellow", "Light yellow"]:
            role = find(lambda r: r.name == names[8], ctx.message.guild.roles)
            await ctx.author.add_roles(role)
            em = discord.Embed(description=f"Colour set to {role.mention}!", colour=discord.Colour.from_rgb(0, 208, 255))
            em.timestamp = datetime.datetime.utcnow()
            await ctx.reply(embed=em, mention_author=False)

        elif id in ["10", "Lime", "lime"]:
            role = find(lambda r: r.name == names[9], ctx.message.guild.roles)
            await ctx.author.add_roles(role)
            em = discord.Embed(description=f"Colour set to {role.mention}!", colour=discord.Colour.from_rgb(0, 208, 255))
            em.timestamp = datetime.datetime.utcnow()
            await ctx.reply(embed=em, mention_author=False)

        elif id in ["11", "Forest Green", "Forest green", "forest green"]:
            role = find(lambda r: r.name == names[10], ctx.message.guild.roles)
            await ctx.author.add_roles(role)
            em = discord.Embed(description=f"Colour set to {role.mention}!", colour=discord.Colour.from_rgb(0, 208, 255))
            em.timestamp = datetime.datetime.utcnow()
            await ctx.reply(embed=em, mention_author=False)

        elif id in ["12", "Light Green", "light green", "Light green"]:
            role = find(lambda r: r.name == names[11], ctx.message.guild.roles)
            await ctx.author.add_roles(role)
            em = discord.Embed(description=f"Colour set to {role.mention}!", colour=discord.Colour.from_rgb(0, 208, 255))
            em.timestamp = datetime.datetime.utcnow()
            await ctx.reply(embed=em, mention_author=False)

        elif id in ["13", "Sea Cyan", "Sea cyan", "sea cyan"]:
            role = find(lambda r: r.name == names[12], ctx.message.guild.roles)
            await ctx.author.add_roles(role)
            em = discord.Embed(description=f"Colour set to {role.mention}!", colour=discord.Colour.from_rgb(0, 208, 255))
            em.timestamp = datetime.datetime.utcnow()
            await ctx.reply(embed=em, mention_author=False)

        elif id in ["14", "Teal", "teal"]:
            role = find(lambda r: r.name == names[13], ctx.message.guild.roles)
            await ctx.author.add_roles(role)
            em = discord.Embed(description=f"Colour set to {role.mention}!", colour=discord.Colour.from_rgb(0, 208, 255))
            em.timestamp = datetime.datetime.utcnow()
            await ctx.reply(embed=em, mention_author=False)

        elif id in ["15", "Aqua", "aqua"]:
            role = find(lambda r: r.name == names[14], ctx.message.guild.roles)
            await ctx.author.add_roles(role)
            em = discord.Embed(description=f"Colour set to {role.mention}!", colour=discord.Colour.from_rgb(0, 208, 255))
            em.timestamp = datetime.datetime.utcnow()
            await ctx.reply(embed=em, mention_author=False)

        elif id in ["16", "Deep Sky", "Deep sky", "deep sky"]:
            role = find(lambda r: r.name == names[15], ctx.message.guild.roles)
            await ctx.author.add_roles(role)
            em = discord.Embed(description=f"Colour set to {role.mention}!", colour=discord.Colour.from_rgb(0, 208, 255))
            em.timestamp = datetime.datetime.utcnow()
            await ctx.reply(embed=em, mention_author=False)

        elif id in ["17", "Indigo", "indigo"]:
            role = find(lambda r: r.name == names[16], ctx.message.guild.roles)
            await ctx.author.add_roles(role)
            em = discord.Embed(description=f"Colour set to {role.mention}!", colour=discord.Colour.from_rgb(0, 208, 255))
            em.timestamp = datetime.datetime.utcnow()
            await ctx.reply(embed=em, mention_author=False)

        elif id in ["18", "Purple", "purple"]:
            role = find(lambda r: r.name == names[17], ctx.message.guild.roles)
            await ctx.author.add_roles(role)
            em = discord.Embed(description=f"Colour set to {role.mention}!", colour=discord.Colour.from_rgb(0, 208, 255))
            em.timestamp = datetime.datetime.utcnow()
            await ctx.reply(embed=em, mention_author=False)

        elif id in ["19", "Medium Purple", "medium purple", "Medium purple"]:
            role = find(lambda r: r.name == names[18], ctx.message.guild.roles)
            await ctx.author.add_roles(role)
            em = discord.Embed(description=f"Colour set to {role.mention}!", colour=discord.Colour.from_rgb(0, 208, 255))
            em.timestamp = datetime.datetime.utcnow()
            await ctx.reply(embed=em, mention_author=False)

        elif id in ["20", "Hot Pink", "Hot pink", "hot pink"]:
            role = find(lambda r: r.name == names[19], ctx.message.guild.roles)
            await ctx.author.add_roles(role)
            em = discord.Embed(description=f"Colour set to {role.mention}!", colour=discord.Colour.from_rgb(0, 208, 255))
            em.timestamp = datetime.datetime.utcnow()
            await ctx.reply(embed=em, mention_author=False)

        elif id in ["21", "Pink", "pink"]:
            role = find(lambda r: r.name == names[20], ctx.message.guild.roles)
            await ctx.author.add_roles(role)
            em = discord.Embed(description=f"Colour set to {role.mention}!", colour=discord.Colour.from_rgb(0, 208, 255))
            em.timestamp = datetime.datetime.utcnow()
            await ctx.reply(embed=em, mention_author=False)

        elif id in ["22", "Light Pink", "Light pink", "light pink"]:
            role = find(lambda r: r.name == names[21], ctx.message.guild.roles)
            await ctx.author.add_roles(role)
            em = discord.Embed(description=f"Colour set to {role.mention}!", colour=discord.Colour.from_rgb(0, 208, 255))
            em.timestamp = datetime.datetime.utcnow()
            await ctx.reply(embed=em, mention_author=False)

        elif id in ["23", "White", "white"]:
            role = find(lambda r: r.name == names[22], ctx.message.guild.roles)
            await ctx.author.add_roles(role)
            em = discord.Embed(description=f"Colour set to {role.mention}!", colour=discord.Colour.from_rgb(0, 208, 255))
            em.timestamp = datetime.datetime.utcnow()
            await ctx.reply(embed=em, mention_author=False)

        else:
            role = find(lambda r: r.name == names[23], ctx.message.guild.roles)
            await ctx.author.add_roles(role)
            em = discord.Embed(description=f"Colour set to {role.mention}!", colour=discord.Colour.from_rgb(0, 208, 255))
            em.timestamp = datetime.datetime.utcnow()
            await ctx.reply(embed=em, mention_author=False)

    """
    @commands.command(name="level")
    async def level(self, ctx):

        try:
            user = levels.find_one({"_id": ctx.author.id})
        except:
            return

        if user is None:
            return await ctx.send("No profile")

        em = discord.Embed(colour=discord.Colour.from_rgb(0, 208, 255))
        em.description = f"**Level**: {user['level']}\n**XP**: {user['xp']}/{xp_required(user['level'])}"
        em.set_author(name=ctx.author.name, icon_url=ctx.author.display_avatar)
        #em.set_thumbnail(url=ctx.author.display_avatar)

        percent_to_next_level = int(math.floor((user['xp'] / xp_required(user['level'])) * 10))

        em.add_field(name=f"XP to Level {user['level']+1} ({round(math.floor((user['xp'] / xp_required(user['level'])) * 100),0)}%)", value=f"{':blue_square:' * percent_to_next_level}{':white_large_square:' * (10 - percent_to_next_level)}")
        em.timestamp = datetime.datetime.utcnow()
        await ctx.reply(embed=em, mention_author=False)
    """

def setup(client):
    client.add_cog(General(client))