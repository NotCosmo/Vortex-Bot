import discord
import datetime
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType

class AdminCmds(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
	    pass

    #Ban#--------------#
    @commands.command()
    @commands.cooldown(1, 3, BucketType.user)
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, user: discord.Member, *, reason=None):

        try:
            embed = discord.Embed(
                description = f'{user.mention} was banned from **{ctx.guild.name}** for {reason}.',
                colour = discord.Colour.from_rgb(119, 178, 86)
            )

            embed.set_author(name=f'User Banned', icon_url = ctx.author.avatar_url)
            embed.set_footer(text = f'User banned by {ctx.author}')

            await user.ban(reason=reason)
            await ctx.message.delete()
            await ctx.send(embed=embed)

        except Exception:
            embed = discord.Embed(
                description = f'Bot does not have enough permissions to ban member.',
                colour = discord.Colour.from_rgb(255, 91, 91)
            )
            embed.set_author(name=f'Command Failed', icon_url = ctx.author.avatar_url)
            embed.set_footer(text = f'{ctx.author}')
            await ctx.send(embed=embed)


    #--------------#
    @ban.error
    async def ban_error(self, ctx: commands.Context, error: commands.CommandError):

        if isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(
                description = f"Command is on cooldown, try again after **{round(error.retry_after, 1)}** seconds.",
                colour = discord.Colour.from_rgb(255, 91, 91)
            )
            embed.set_author(name=f'Cooldown', icon_url = ctx.author.avatar_url)
            await ctx.send(embed=embed)

        elif isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                description = 
                f'**Command Format**\n• `!ban <user> (reason)`\n \n**Example**\n• `!ban @cosmo.#5056`\n• `!ban @cosmo.#5056 Using bad words!`',
                colour = discord.Colour.from_rgb(255, 91, 91)
            )
            embed.set_author(name=f'Ban Command', icon_url = ctx.author.avatar_url)
            embed.set_footer(text='- Arguments in () are optional.')
            await ctx.send(embed=embed)

        elif isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                description = f'You do not have enough permissions to run this command.',
                colour = discord.Colour.from_rgb(255, 91, 91)
            )
            embed.set_author(name=f'Permission Error', icon_url = ctx.author.avatar_url)
            await ctx.send(embed=embed)

    #Kick#--------------#
    @commands.command()
    @commands.cooldown(1, 3, BucketType.user)
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, user: discord.Member, *, reason=None):

        try:
            embed = discord.Embed(
                description = f'{user.mention} was kicked from **{ctx.guild.name}** for {reason}.',
                colour = discord.Colour.from_rgb(119, 178, 86)
            )

            embed.set_author(name=f'User Kicked', icon_url = ctx.author.avatar_url)
            embed.set_footer(text = f'User kicked by {ctx.author}')

            await user.kick(reason=reason)
            await ctx.message.delete()
            await ctx.send(embed=embed)

        except Exception:
            embed = discord.Embed(
                description = f'Bot does not have enough permissions to kick member.',
                colour = discord.Colour.from_rgb(255, 91, 91)
            )
            embed.set_author(name=f'Command Failed', icon_url = ctx.author.avatar_url)
            embed.set_footer(text = f'{ctx.author}')
            await ctx.send(embed=embed)


    #--------------#
    @kick.error
    async def kick_error(self, ctx: commands.Context, error: commands.CommandError):

        if isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(
                description = f"Command is on cooldown, try again after **{round(error.retry_after, 1)}** seconds.",
                colour = discord.Colour.from_rgb(255, 91, 91)
            )
            embed.set_author(name=f'Cooldown', icon_url = ctx.author.avatar_url)
            await ctx.send(embed=embed)

        elif isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                description = 
                f'**Command Format**\n• `!kick <user> (reason)`\n \n**Example**\n• `!kick @cosmo.#5056`\n• `!kick @cosmo.#5056 Being rude!`',
                colour = discord.Colour.from_rgb(255, 91, 91)
            )
            embed.set_author(name=f'Kick Command', icon_url = ctx.author.avatar_url)
            embed.set_footer(text='- Arguments in () are optional.')
            await ctx.send(embed=embed)

        elif isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                description = f'You do not have enough permissions to run this command.',
                colour = discord.Colour.from_rgb(255, 91, 91)
            )
            embed.set_author(name=f'Permission Error', icon_url = ctx.author.avatar_url)
            await ctx.send(embed=embed)

    #Role#--------------#
    @commands.command()
    @commands.cooldown(1, 3, BucketType.user)
    @commands.has_permissions(manage_roles=True)
    async def role(self, ctx, user : discord.Member, *, role : commands.RoleConverter):

        if role.position > ctx.author.top_role.position: 
            embed = discord.Embed(
                description = f'Cannot assign role, that role is above your highest role.',
                colour = discord.Colour.from_rgb(255, 91, 91)
            )
            
            embed.set_author(name=f'Command Failed', icon_url = ctx.author.avatar_url)            
            await ctx.send(embed=embed)

        if role in user.roles:
            embed = discord.Embed(
                description = f'{role.mention} role removed from {user.mention}.',
                colour = discord.Colour.from_rgb(119, 178, 86)
            )

            embed.set_author(name=f'Role Removed', icon_url = ctx.author.avatar_url)
            embed.set_footer(text = f'Role removed by {ctx.author}')
            await user.remove_roles(role) 
            await ctx.send(embed=embed)

        else:
            embed = discord.Embed(
                description = f'{role.mention} role added to {user.mention}.',
                colour = discord.Colour.from_rgb(119, 178, 86)
            )

            embed.set_author(name=f'Role Added', icon_url = ctx.author.avatar_url)
            embed.set_footer(text = f'Role added by {ctx.author}')
            await user.add_roles(role) 
            await ctx.send(embed=embed)

    #--------------#
    @role.error
    async def role_error(self, ctx: commands.Context, error: commands.CommandError):

        if isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(
                description = f"Command is on cooldown, try again after **{round(error.retry_after, 1)}** seconds.",
                colour = discord.Colour.from_rgb(255, 91, 91)
            )
            embed.set_author(name=f'Cooldown', icon_url = ctx.author.avatar_url)

        elif isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                description = f'Invalid Arguments. `!role <user> <role name>`.',
                colour = discord.Colour.from_rgb(255, 91, 91)
            )
            embed.set_author(name=f'Command Failed', icon_url = ctx.author.avatar_url)

        elif isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                description = f'You do not have enough permissions to run this command.',
                colour = discord.Colour.from_rgb(255, 91, 91)
            )
            embed.set_author(name=f'Command Failed', icon_url = ctx.author.avatar_url)

        await ctx.send(embed=embed)

    @commands.command(aliases = ["clear", "clean"])
    @commands.has_permissions(administrator=True)
    async def purge(self, ctx, amt: int, silent: str=None):

        if amt <= 100:

            if silent is None:
                embed = discord.Embed(
                    title = "Purge Complete",
                    description = f"**{amt}** messages cleared by {ctx.author.mention}.",
                    colour = discord.Colour.from_rgb(255, 50, 50)
                )

                embed.timestamp = datetime.datetime.utcnow()
                await ctx.message.delete()
                await ctx.channel.purge(limit=amt)
                await ctx.send(embed=embed)

            if silent == "-s":

                await ctx.message.delete()
                await ctx.channel.purge(limit=amt)

            else:
                pass

        else:

            embed = discord.Embed(
                title = "Error",
                description = "Please input an amount below 100.",
                colour = discord.Colour.from_rgb(255, 75, 75)
            )
            
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=embed)
            await ctx.message.delete()

    @purge.error
    async def purge_error(self, ctx: commands.Context, error: commands.CommandError):

        if isinstance(error, commands.MissingPermissions):

            embed = discord.Embed(
                title = "Permission Error",
                description = "You do not have enough permissions to run this command.",
                colour = discord.Colour.from_rgb(255, 75, 75)
            )

            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=embed)

        if isinstance(error, commands.MissingRequiredArgument):

            embed = discord.Embed(
                title = "Argument Error",
                description = "Missing Argument: `!purge <amount>`.",
                colour = discord.Colour.from_rgb(255, 75, 75)
            )

            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def ecoupdate(self, ctx):

        embed = discord.Embed(
            title = 'Locked',
            description = f'New update in progress!',
            colour = discord.Colour.from_rgb(255, 91, 91)
        )
        embed.set_author(name='Lockdown', icon_url=ctx.author.icon_url)
        embed.set_footer(text=f'Lockdown initiated by {ctx.author.name}')
        
        eco1 = self.client.get_channel(735796560792780891)
        eco2 = self.client.get_channel(814787175576109067)
        eco3 = self.client.get_channel(814787195428405259)

        await eco1.channel.set_permissions(ctx.guild.default_role, send_messages=False)
        await eco1.send(embed=embed)

        await eco2.channel.set_permissions(ctx.guild.default_role, send_messages=False)
        await eco2.send(embed=embed)

        await eco3.channel.set_permissions(ctx.guild.default_role, send_messages=False)
        await eco3.send(embed=embed)
        await ctx.channel.send('Lockdown complete.')

def setup(client):
    client.add_cog(AdminCmds(client))