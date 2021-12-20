import nextcord as discord
import sys
import os
from datetime import datetime
from nextcord.ext import commands

def restart():
    os.execv(sys.executable, ['python'] + sys.argv)

class Dev(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['rs'], hidden=True)
    @commands.is_owner()
    async def restart(self, ctx):

        embed = discord.Embed(
            title = "Restarting Bot",
            description = "> Bot is restarting, this could take a few seconds.",
            colour = discord.Colour.from_rgb(0, 208, 255)
        )
        embed.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=embed)
        restart()

def setup(client):
    client.add_cog(Dev(client))