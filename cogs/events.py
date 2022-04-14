import nextcord as discord
from nextcord.utils import find
from nextcord.ext import commands
import io
import traceback
from datetime import datetime

class Events(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_member_join(self, user):

        # 
        guild = self.client.get_guild(581139467381768192)
        channel = self.client.get_channel(735765424108601386)

        member = find(lambda r: r.name == "Member", guild.roles)
        titles = find(lambda r: r.name == "━━━━━ Titles ━━━━━", guild.roles)
        levels = find(lambda r: r.name == "━━━━━ Levels ━━━━━", guild.roles)
        eco = find(lambda r: r.name == "━━━━━ Eco ━━━━━", guild.roles)

        embed = discord.Embed(
            description = f'Welcome to the server {user.mention}! We hope you enjoy your stay.',
            colour = discord.Colour.from_rgb(0, 208, 255)
        )

        embed.set_author(name="👋 New User", icon_url=user.display_avatar)
        embed.timestamp = datetime.utcnow()
        await self.client.get_channel(929330258816159815).edit(name=f"👤 Members: {len(self.client.get_guild(581139467381768192).members)}")
        await channel.send(embed=embed)
        await user.add_roles(member)
        await user.add_roles(titles)
        await user.add_roles(levels)
        await user.add_roles(eco)

    #@commands.Cog.listener()
    #async def on_message(self, ctx):

        # Making sure bot isn't replying to itself
        #if ctx.author.id == self.client.user.id:
        #    return

        # Making sure bot isn't replying to other bots
            #return
        #if ctx.author.bot:

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        
        errorColour = discord.Colour.from_rgb(255, 75, 75)

        if hasattr(ctx.command, 'on_error'):
            return

        # Missing Arguments for command
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                description = ":x: Invalid Arguments. Please try again.",
                colour = errorColour
            )
            embed.set_author(name="Error", icon_url=ctx.author.avatar.url)
            embed.timestamp = datetime.utcnow()
            return await ctx.send(embed=embed)

        # Command is on cooldown
        if isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(
                # {str(timedelta(seconds=round(error.retry_after, 1)))}
                description = f":stopwatch: Command is on cooldown, please try again in {round(error.retry_after, 2)}s",
                colour = errorColour
            )
            embed.set_author(name="Cooldown", icon_url=ctx.author.avatar.url)
            embed.timestamp = datetime.utcnow()
            return await ctx.send(embed=embed)

        # Missing Perms
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                description = ":x: You do not have enough permissions to run this command.",
                colour = errorColour
            )
            embed.set_author(name="Error", icon_url=ctx.author.avatar.url)
            embed.timestamp = datetime.utcnow()
            return await ctx.send(embed=embed)

        # Bot Missing Perms
        if isinstance(error, commands.BotMissingPermissions):
            embed = discord.Embed(
                description = ":x: I do not have enough permissions to run this command.",
                colour = errorColour
            )
            embed.set_author(name="Error", icon_url=ctx.author.avatar.url)
            embed.timestamp = datetime.utcnow()
            return await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Events(client))