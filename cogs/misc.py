import nextcord as discord
import datetime
from time import strftime
import random
from nextcord.ext import commands
from nextcord import Spotify
from nextcord.ext.commands import BucketType

def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))


def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % rgb

class misc(commands.Cog):

    @commands.command(aliases = ['source', 'git', 'gh'])
    @commands.cooldown(1, 10, BucketType.user)
    async def github(self, ctx):
        await ctx.send(":white_check_mark: ┃ You can find my source code on Github through this link: https://github.com/NotCosmo/Vortex")

    @commands.command(aliases = ['si'])
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
            colour = discord.Colour.random()
        )
        embed.set_thumbnail(url=icon)
        embed.add_field(name="Owner", value=owner, inline=True)
        embed.add_field(name="Server ID", value=id, inline=True)
        embed.add_field(name="Region", value=region, inline=True)
        embed.add_field(name="Member Count", value=memberCount, inline=True)

        await ctx.send(embed=embed)

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
            embed.set_author(name=f'Cooldown', icon_url=ctx.author.avatar.url)  
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
            embed.set_author(name=f'Cooldown', icon_url=ctx.author.avatar.url)  
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
            embed.set_author(name=f'Cooldown', icon_url=ctx.author.avatar.url)  
            await ctx.send(embed=embed)

    @commands.command(aliases = ["avatar"])
    @commands.cooldown(1, 3, BucketType.user)
    async def av(self, ctx, user: discord.Member=None):
        
        embed = discord.Embed(
            colour = ctx.author.colour
        )

        if user is None:
            embed.set_image(url=ctx.author.avatar.url)

        else:
            embed.set_image(url=user.avatar.url)
        
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
            embed.set_author(name=f'Cooldown', icon_url=ctx.author.avatar.url)    
        
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

    @commands.command(aliases = ["whois"])
    async def userinfo(self, ctx, *, user: discord.Member=None): # b'\xfc'
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
        embed2.set_author(name=f"Bug Reported - {ctx.author}", icon_url=ctx.author.avatar.url)
        embed2.timestamp = datetime.datetime.utcnow()

        embed.set_thumbnail(url=ctx.author.avatar.url)
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

    @commands.command()
    async def spotify(self, ctx, user: discord.Member=None):

        if user is None:
            user = ctx.author

        else:
            user = user

        for activity in user.activities:
            if isinstance(activity, Spotify):

                em = discord.Embed(
                    title = f"Listening to {activity.title}..",
                    description = f"Track ID: {activity.track_id}",
                    colour = discord.Colour.from_rgb(30, 215, 96)
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

def setup(client):
    client.add_cog(misc(client))