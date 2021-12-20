# Main Imports

import nextcord as discord
import datetime
import asyncio
import random
import aiohttp

# Side Imports

from main import timeNow
from nextcord.ext import commands
from nextcord.utils import find
from nextcord.ext.commands import BucketType

class Colours(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases = ["colorlist", "colors", "colours"])
    async def colourlist(self, ctx):

        em = discord.Embed(
            title = "Colour List",
            description = "Use the command `>colour [id]` to select a colour!",
            colour = discord.Colour.from_rgb(0, 208, 255)
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

    @commands.command(aliases = ["color", "Colour", "Color"])
    async def colour(self, ctx, *, id: str):

        names = [
            "Red", "Carmine", "Rose Red", "Orange", "Dark Orange", "Coral", "Gold", "Yellow", "Light Yellow", "Lime", "Forest Green", "Light Green", "Sea Cyan", "Teal", "Aqua", "Deep Sky", "Indigo", "Purple", "Medium Purple", "Hot Pink", "Pink", "Light Pink", "White", "Black"
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

def setup(client):
    client.add_cog(Colours(client))