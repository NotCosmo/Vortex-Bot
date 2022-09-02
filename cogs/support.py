# Main Imports

import nextcord as discord
from nextcord import Interaction
from nextcord.ext import commands
from datetime import datetime
import asyncio

class SupportButtons(discord.ui.View):

    def __init__(self):
        self.type = None
        super().__init__()

    @discord.ui.button(label="General Issue", style=discord.ButtonStyle.green)
    async def general_issue(self, button: discord.Button, i: discord.Interaction):

        self.type = "general"

    @discord.ui.button(label="Economy Bug", style=discord.ButtonStyle.blurple)
    async def economy_bug(self, button: discord.Button, i: discord.Interaction):

        self.type = "economy"

    @discord.ui.button(label="Breaking Bug", style=discord.ButtonStyle.danger)
    async def breaking_bug(self, button: discord.Button, i: discord.Interaction):

        self.type = "breaking"

class Support(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(
        name="support",
        aliases=["report"],
    )
    async def support(self, ctx, *, issue: str):

        embed = discord.Embed(title="Support Ticket", description="Please press which buttons best describes your issue.", colour=discord.Colour.from_rgb(255, 75, 75))

        view = SupportButtons()
        await ctx.send(embed=embed, view=view)
        await asyncio.sleep(3)
        await ctx.reply(":white_check_mark: Thank you for your report!", mention_author=False)
        
        if view.type is None:
            return
        
        if view.type == "general":

            embed = discord.Embed(title=":hammer_pick: General Issue", description=f"{issue}\n\n[Jump to message]({ctx.message.jump_url})", colour=discord.Colour.from_rgb(0, 208, 255))
            embed.set_author(name=str(ctx.author), icon_url=ctx.author.display_avatar)
            #embed.set_thumbnail(url=ctx.author.display_avatar)
            embed.timestamp = datetime.utcnow()
            c = ctx.guild.get_channel(999036729224876122)
            await c.send(embed=embed)
        
        if view.type == "economy":

            embed = discord.Embed(title=":gem: Economy Bug", description=f"{issue}\n\n[Jump to message]({ctx.message.jump_url})", colour=discord.Colour.from_rgb(0, 208, 255))
            embed.set_author(name=str(ctx.author), icon_url=ctx.author.display_avatar)
            embed.timestamp = datetime.utcnow()
            #embed.set_thumbnail(url=ctx.author.display_avatar)
            c = ctx.guild.get_channel(999036729224876122)
            await c.send(embed=embed)

        if view.type == "breaking":

            embed = discord.Embed(title=":warning: Breaking Bug", description=f"{issue}\n\n[Jump to message]({ctx.message.jump_url})", colour=discord.Colour.from_rgb(255, 75, 75))
            embed.set_author(name=str(ctx.author), icon_url=ctx.author.display_avatar)
            embed.timestamp = datetime.utcnow()
            #embed.set_thumbnail(url=ctx.author.display_avatar)            
            c = ctx.guild.get_channel(999036729224876122)
            await c.send(content="<@455971566199767040>", embed=embed)

def setup(client):
    client.add_cog(Support(client))