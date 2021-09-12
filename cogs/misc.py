import discord
import datetime
import random
from discord.ext import commands
from discord.ext.commands import BucketType

class misc(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.cooldown(1, 3, BucketType.user)
    async def retardnight(self, ctx, toggle="on"):

        role = discord.utils.find(lambda r: r.name == 'Retard Night', ctx.message.guild.roles)

        if toggle == "on" and role not in ctx.author.roles:
            
            embed = discord.Embed(
                title = "Toggled On!",
                description = ":thumbsup: Successfully toggled VRetard Night Pings `on`.",
                colour = discord.Colour.from_rgb(95, 255, 95)
            )
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=embed)
            await ctx.author.add_roles(role)

        elif toggle == "on" and role in ctx.author.roles:
            
            embed = discord.Embed(
                title = "Role Error",
                description = "You already have Retard Night enabled!",
                colour = discord.Colour.from_rgb(255, 75, 55)
            )
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=embed)

        if toggle == "off" and role not in ctx.author.roles:
            
            embed = discord.Embed(
                title = "Command Error",
                description = "You do not have Retard Night enabled!",
                colour = discord.Colour.from_rgb(255, 75, 75)
            )
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=embed)

        elif toggle == "off" and role in ctx.author.roles:
            
            embed = discord.Embed(
                title = "Toggled Off!",
                description = ":thumbsup: Successfully toggled Retard Night Pings `off`.",
                colour = discord.Colour.from_rgb(95, 255, 95)
            )
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=embed)
            await ctx.author.remove_roles(role)

    @retardnight.error
    async def retardnight_error(self, ctx: commands.Context, error: commands.CommandError):

        if isinstance(error, commands.MissingRequiredArgument):

            embed = discord.Embed(
                title = "Argument Error",
                description = "Missing Argument: `!retardnight <on/off>`.",
                colour = discord.Colour.from_rgb(255, 75, 75)
            )
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=embed)

        if isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(
                description = f"Command is on cooldown, try again after **{round(error.retry_after, 1)}** seconds.",
                colour = discord.Colour.from_rgb(255, 91, 91)
            )
            embed.timestamp = datetime.datetime.utcnow()
            embed.set_author(name=f'Cooldown', icon_url=ctx.author.avatar_url)  
            await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 3, BucketType.user)
    async def updates(self, ctx, toggle="on"):

        vortexPing = discord.utils.find(lambda r: r.name == 'Vortex Ping', ctx.message.guild.roles)

        if toggle == "on" and vortexPing not in ctx.author.roles:
            
            embed = discord.Embed(
                title = "Toggled On!",
                description = ":thumbsup: Successfully toggled Vortex Update Pings `on`.",
                colour = discord.Colour.from_rgb(95, 255, 95)
            )
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=embed)
            await ctx.author.add_roles(vortexPing)

        elif toggle == "on" and vortexPing in ctx.author.roles:
            
            embed = discord.Embed(
                title = "Role Error",
                description = "You already have Vortex Update Pings enabled!",
                colour = discord.Colour.from_rgb(255, 75, 55)
            )
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=embed)

        if toggle == "off" and vortexPing not in ctx.author.roles:
            
            embed = discord.Embed(
                title = "Command Error",
                description = "You do not have Vortex Update Pings enabled!",
                colour = discord.Colour.from_rgb(255, 75, 75)
            )
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=embed)

        elif toggle == "off" and vortexPing in ctx.author.roles:
            
            embed = discord.Embed(
                title = "Toggled Off!",
                description = ":thumbsup: Successfully toggled Vortex Update Pings `off`.",
                colour = discord.Colour.from_rgb(95, 255, 95)
            )
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=embed)
            await ctx.author.remove_roles(vortexPing)

    @updates.error
    async def updates_error(self, ctx: commands.Context, error: commands.CommandError):

        if isinstance(error, commands.MissingRequiredArgument):

            embed = discord.Embed(
                title = "Argument Error",
                description = "Missing Argument: `!updates <on/off>`.",
                colour = discord.Colour.from_rgb(255, 75, 75)
            )
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=embed)

        if isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(
                description = f"Command is on cooldown, try again after **{round(error.retry_after, 1)}** seconds.",
                colour = discord.Colour.from_rgb(255, 91, 91)
            )
            embed.timestamp = datetime.datetime.utcnow()
            embed.set_author(name=f'Cooldown', icon_url=ctx.author.avatar_url)  
            await ctx.send(embed=embed)

    @commands.command(aliases = ["eco"])
    @commands.cooldown(1, 3, BucketType.user)
    async def economy(self, ctx, toggle="on"):

        eco = discord.utils.find(lambda r: r.name == 'Economy', ctx.message.guild.roles)

        if toggle == "on" and eco not in ctx.author.roles:
            
            embed = discord.Embed(
                title = "Toggled On!",
                description = ":thumbsup: Successfully toggled Economy Pings `on`.",
                colour = discord.Colour.from_rgb(95, 255, 95)
            )
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=embed)
            await ctx.author.add_roles(eco)

        elif toggle == "on" and eco in ctx.author.roles:
            
            embed = discord.Embed(
                title = "Role Error",
                description = "You already have Economy Pings enabled!",
                colour = discord.Colour.from_rgb(255, 75, 55)
            )
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=embed)

        if toggle == "off" and eco not in ctx.author.roles:
            
            embed = discord.Embed(
                title = "Command Error",
                description = "You do not have Economy Pings enabled!",
                colour = discord.Colour.from_rgb(255, 75, 75)
            )
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=embed)

        elif toggle == "off" and eco in ctx.author.roles:
            
            embed = discord.Embed(
                title = "Toggled Off!",
                description = ":thumbsup: Successfully toggled Economy Pings `off`.",
                colour = discord.Colour.from_rgb(95, 255, 95)
            )
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=embed)
            await ctx.author.remove_roles(eco)

    @economy.error
    async def economy_error(self, ctx: commands.Context, error: commands.CommandError):

        if isinstance(error, commands.MissingRequiredArgument):

            embed = discord.Embed(
                title = "Argument Error",
                description = "Missing Argument: `!eco <on/off>`.",
                colour = discord.Colour.from_rgb(255, 75, 75)
            )
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=embed)

        if isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(
                description = f"Command is on cooldown, try again after **{round(error.retry_after, 1)}** seconds.",
                colour = discord.Colour.from_rgb(255, 91, 91)
            )
            embed.timestamp = datetime.datetime.utcnow()
            embed.set_author(name=f'Cooldown', icon_url=ctx.author.avatar_url)  
            await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 3, BucketType.user)
    async def av(self, ctx, user: discord.Member=None):
        
        embed = discord.Embed(
            colour = ctx.author.colour
        )

        if user is None:
            embed.set_image(url=ctx.author.avatar_url)

        else:
            embed.set_image(url=user.avatar_url)
        
        await ctx.send(embed=embed)

    #--------------#
    @av.error
    async def av_error(self, ctx: commands.Context, error: commands.CommandError):

        if isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(
                description = f"Command is on cooldown, try again after **{round(error.retry_after, 1)}** seconds.",
                colour = discord.Colour.from_rgb(255, 91, 91)
            )
            embed.timestamp = datetime.datetime.utcnow()
            embed.set_author(name=f'Cooldown', icon_url=ctx.author.avatar_url)    
        
        await ctx.send(embed=embed)
        
    @commands.command(pass_context=True)
    async def poll(self, ctx, question, *options: str):

        if len(options) > 2:
            await ctx.send('```Error! Syntax = [!poll "question" "option1" "option2"] ```')
            return

        if len(options) == 2 and options[0] == "yes" and options[1] == "no":
            reactions = ['🅰️', '🅱️'] #['🅰️', '🅱️']
        else:
            reactions = ['🅰️', '🅱️'] #['🅰️', '🅱️']

        description = []
        for x, option in enumerate(options):
            description += '\n {} {} {}\n'.format(reactions[x], "-", option)

        poll_embed = discord.Embed(title=question, colour=discord.Colour.from_rgb(0, 208, 255), description=''.join(description))

        react_message = await ctx.send(embed=poll_embed)

        for reaction in reactions[:len(options)]:
            await react_message.add_reaction(reaction)

    @poll.error
    async def poll_error(self, ctx: commands.Context, error: commands.CommandError):

        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('error')

    @commands.command()
    async def userinfo(self, ctx, *, user: discord.Member=None): # b'\xfc'
        if user is None:
            user = ctx.author      
        date_format = "%a, %d %b %Y %I:%M %p"

        embed = discord.Embed(
            colour=user.colour, 
            description=user.mention
        )
        embed.set_author(name=str(user), icon_url=user.avatar_url)
        embed.set_thumbnail(url=user.avatar_url)

        embed.add_field(name="Joined Server", value=f'`{user.joined_at.strftime(date_format)}`')
        embed.add_field(name="Account Creation", value=f'`{user.created_at.strftime(date_format)}`')
        embed.add_field(name="User Status", value=f"{user.activity}", inline=False)

        if len(user.roles) > 1:
            role_string = ' '.join([r.mention for r in user.roles][1:])
            embed.add_field(name="Roles [{}]\n \n".format(len(user.roles)-1), value=role_string, inline=False)

        embed.set_footer(text='ID: ' + str(user.id))
        embed.timestamp = datetime.datetime.utcnow()
        return await ctx.send(embed=embed)

    @commands.command(aliases = ["report"])
    async def bug(self, ctx, *, bug):

        log = self.client.get_channel(882210144837042256)
        embed = discord.Embed(
            title = f"Bug Reported - {ctx.author}",
            description = bug,
            colour = discord.Colour.from_rgb(255, 75, 75)
        )
        embed2 = discord.Embed(
            description = ":thumbsup: Thank you for the bug report! We have received it and will notify you upon it being fixed.",
            colour = discord.Colour.from_rgb(75, 255, 75)
        )
        embed2.set_author(name=f"Bug Reported - {ctx.author}", icon_url=ctx.author.avatar_url)
        embed2.timestamp = datetime.datetime.utcnow()

        embed.set_thumbnail(url=ctx.author.avatar_url)
        embed.set_footer(text = "Bug Reported")
        embed.timestamp = datetime.datetime.utcnow()

        await ctx.channel.send(embed=embed2)
        await log.send(embed=embed)

    @bug.error
    async def bug_error(self, ctx: commands.Context, error: commands.CommandError):

        if isinstance(error, commands.MissingRequiredArgument):

            embed = discord.Embed(
                title = "Argument Error",
                description = "Missing Arguments: `!bug <description of bug>`.",
                colour = discord.Colour.from_rgb(255, 75, 75)
            )
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=embed)

def setup(client):
    client.add_cog(misc(client))