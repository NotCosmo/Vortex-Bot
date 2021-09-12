import discord
from discord.ext import commands
from discord.utils import get

class on_msg(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, ctx):

        if ctx.author.id == self.client.user.id:
            return

        if ctx.author.bot:
            return
                
        await self.client.process_commands(ctx)

def setup(client):
    client.add_cog(on_msg(client))