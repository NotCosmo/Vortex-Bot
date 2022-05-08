import nextcord as discord
from nextcord import Interaction
from datetime import datetime
from nextcord.ext import commands
from nextcord.ext.commands import BucketType
from pymongo import MongoClient

cluster = MongoClient("mongodb+srv://Cosmo:1H1uqPGjo5CjtHQe@eco.5afje.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
database = cluster["Discord"]
db = database["Warns"]
lockdown = database["Lockdown"]
utils = database["Server_Utils"]

class Staff(commands.Cog, description="Moderation and Economy config commands."):

    def __init__(self, client):
        self.client = client
        self.db = db
        self.lockdown = lockdown
        self.utils = utils

    @commands.command(aliases=['dm', 'send'])
    @commands.is_owner()
    async def dm_user(self, ctx, user: discord.User, *, message: str) -> None:
        await ctx.message.delete()
        try:
            return await user.send(message)
        except Exception:
            return await ctx.author.send("Could not dm user.")
            
    
    @commands.command(aliases=['cr', 'createrole'])
    async def create_role(self, ctx, *, name: str='new role'):

        role = await ctx.guild.create_role(name=name)
        em = discord.Embed(
            colour = discord.Colour.from_rgb(47, 49, 55),
            title = f':gear: Created role {role.mention}.'
        )
        em.timestamp = datetime.utcnow()
        return await ctx.send(embed=em)
    
    @discord.user_command(name="Bot Info", guild_ids=[581139467381768192])
    async def bot_info(self, i: Interaction, member):

        data = self.utils.find_one({"tag":"Bot Info"})
        created = data["create_date"]
        uptime = int(data["uptime_start"])
        em = discord.Embed(colour = discord.Colour.from_rgb(0, 208, 255))
        em.add_field(name="__About__", value=f"Hey, I'm Vortex. I'm a multi-purpose bot made for this server for any purpose you would need. From basic fun modules, to a fully fledged economy system!\n\n**Developer** `cosmo.#5056`\n**Created** <t:{created}:R> using `nextcord`.\n\n",inline=False)
        em.add_field(name="__Bot Stats__", value=f":robot: **Bot Ping** {round(self.client.latency * 1000, 2)}ms\n:stopwatch: **Uptime** <t:{uptime}:R>",inline=False)
        em.set_author(name="Bot Info",icon_url=self.client.user.display_avatar)
        em.timestamp = datetime.utcnow()
        await i.send(embed=em)
    
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def warn(self, ctx, user: discord.Member, *, reason: str="No reason provided."):

        user_warns = self.db.count_documents({"user_id":user.id})
        data = self.db.find_one({"tag":"Cases"})
        cases = data["count"]
        time_now = datetime.now().timestamp()
        
        self.db.insert_one({
            "_case_id":cases+1,
            "case_type":"warning",
            "user_id":user.id,
            "reason":reason,
            "moderator_id":ctx.author.id,
            "time":time_now,
            "deleted":False
        })
        
        # Update total warns
        self.db.update_one({"tag":"Cases"},{"$set":{"count":cases+1}})
        
        em = discord.Embed(
            title = ":warning: Warning",
            colour = discord.Colour.from_rgb(47, 49, 55),
            description = f'{user.mention} has been warned for: __{reason}__'
        ).set_footer(text=f"Warn ID: {cases+1}")
        em.timestamp = datetime.utcnow()
        await ctx.message.delete()
        await ctx.send(embed=em)

        logs = self.client.get_channel(944574562589356092)
        log_embed = discord.Embed(
            title = f":warning: Warning (Case {cases+1})",
            colour = discord.Colour.from_rgb(47, 49, 55)
        )
        log_embed.set_thumbnail(url=user.display_avatar)
        log_embed.add_field(name="User", value=f"{user.mention}",inline=False)
        log_embed.add_field(name="Moderator", value=f"{ctx.author.mention}",inline=False)
        log_embed.add_field(name="Warned At", value=f"<t:{int(time_now)}:t> | <t:{int(time_now)}:R>",inline=False)
        log_embed.add_field(name="Reason", value=f"{reason}",inline=False)
        log_embed.timestamp = datetime.utcnow()
        await logs.send(embed=log_embed)

    #Ban#--------------#
    @commands.command()
    @commands.cooldown(1, 3, BucketType.user)
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, user: discord.Member, *, reason="No reason provided."):

        user_warns = self.db.count_documents({"user_id":user.id})
        data = self.db.find_one({"tag":"Cases"})
        cases = data["count"]
        time_now = datetime.now().timestamp()

        try:

            await user.ban(reason=reason)
        
            self.db.insert_one({
                "_case_id":cases+1,
                "case_type":"ban",
                "user_id":user.id,
                "reason":reason,
                "moderator_id":ctx.author.id,
                "time":time_now,
                "deleted":False
            })
            
            # Update total warns
            self.db.update_one({"tag":"Cases"},{"$set":{"count":cases+1}})
            
            em = discord.Embed(
                title = ":warning: Ban",
                colour = discord.Colour.from_rgb(47, 49, 55),
                description = f'{user.mention} has been banned for: __{reason}__'
            ).set_footer(text=f"Ban ID: {cases+1}")
            em.timestamp = datetime.utcnow()
            await ctx.message.delete()
            await ctx.send(embed=em)
    
            logs = self.client.get_channel(944574562589356092)
            log_embed = discord.Embed(
                title = f":warning: Ban (Case {cases+1})",
                colour = discord.Colour.from_rgb(47, 49, 55)
            )
            log_embed.set_thumbnail(url=user.display_avatar)
            log_embed.add_field(name="User", value=f"{user.mention}",inline=False)
            log_embed.add_field(name="Moderator", value=f"{ctx.author.mention}",inline=False)
            log_embed.add_field(name="Banned At", value=f"<t:{int(time_now)}:t> | <t:{int(time_now)}:R>",inline=False)
            log_embed.add_field(name="Reason", value=f"{reason}",inline=False)
            log_embed.timestamp = datetime.utcnow()
            return await logs.send(embed=log_embed)

        except:
            em = discord.Embed(
                title = f":warning: Protection Error",
                description = 'That user is protected, I cannot ban them!',
                colour = discord.Colour.from_rgb(47, 49, 55)
            )
            em.timestamp = datetime.utcnow()
            return await ctx.send(embed=em)

    #Ban#--------------#
    @commands.command()
    @commands.cooldown(1, 3, BucketType.user)
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, user: discord.Member, *, reason="No reason provided."):

        user_warns = self.db.count_documents({"user_id":user.id})
        data = self.db.find_one({"tag":"Cases"})
        cases = data["count"]
        time_now = datetime.now().timestamp()

        try:

            await user.kick(reason=reason)
        
            self.db.insert_one({
                "_case_id":cases+1,
                "case_type":"kick",
                "user_id":user.id,
                "reason":reason,
                "moderator_id":ctx.author.id,
                "time":time_now,
                "deleted":False
            })
            
            # Update total warns
            self.db.update_one({"tag":"Cases"},{"$set":{"count":cases+1}})
            
            em = discord.Embed(
                title = ":warning: Kick",
                colour = discord.Colour.from_rgb(47, 49, 55),
                description = f'{user.mention} has been kicked for: __{reason}__'
            ).set_footer(text=f"Kick ID: {cases+1}")
            em.timestamp = datetime.utcnow()
            await ctx.message.delete()
            await ctx.send(embed=em)
    
            logs = self.client.get_channel(944574562589356092)
            log_embed = discord.Embed(
                title = f":warning: Kick (Case {cases+1})",
                colour = discord.Colour.from_rgb(47, 49, 55)
            )
            log_embed.set_thumbnail(url=user.display_avatar)
            log_embed.add_field(name="User", value=f"{user.mention}",inline=False)
            log_embed.add_field(name="Moderator", value=f"{ctx.author.mention}",inline=False)
            log_embed.add_field(name="Kicked At", value=f"<t:{int(time_now)}:t> | <t:{int(time_now)}:R>",inline=False)
            log_embed.add_field(name="Reason", value=f"{reason}",inline=False)
            log_embed.timestamp = datetime.utcnow()
            return await logs.send(embed=log_embed)

        except:
            em = discord.Embed(
                title = f":warning: Protection Error",
                description = 'That user is protected, I cannot kick them!',
                colour = discord.Colour.from_rgb(47, 49, 55)
            )
            em.timestamp = datetime.utcnow()
            return await ctx.send(embed=em)
    
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def case(self, ctx, case_id: int):

        try:
            data = self.db.find_one({"_case_id":case_id})

            user_id = data['user_id']
            mod_id = data['moderator_id']
            reason = data['reason']
            time = data['time']
            type = data['case_type']
    
            em = discord.Embed(
                title = f':warning: Case {case_id} [{type[0].upper() + type[1:]}]',
                description = "",
                colour = discord.Colour.from_rgb(47, 49, 55)
            )
            
            user = await self.client.fetch_user(user_id)
            mod = ctx.guild.get_member(mod_id)
                
            em.set_thumbnail(url=user.display_avatar)
            if data["deleted"] == True:
                em.description += ":lock: **This case has been deleted.**"
            em.description += f"\n\n**User:** {user.mention}\n**Moderator**: {mod.mention}\n\n**Reason**: {reason}\n**Time**: <t:{int(time)}:t> | <t:{int(time)}:R>"
            em.timestamp = datetime.utcnow()
            return await ctx.send(embed=em)
            
        except:
            em = discord.Embed(
                title = ':warning: Error',
                description = f'Could not find a case with the ID `{case_id}`.',
                colour = discord.Colour.from_rgb(47, 49, 55)
            )
            return await ctx.send(embed=em)
    
    @commands.command(aliases=['logs', 'history'])
    @commands.has_permissions(administrator=True)
    async def cases(self, ctx, user: discord.Member):

        em = discord.Embed(
            title = f'Cases for {user}',
            description = '',
            colour = discord.Colour.from_rgb(47, 49, 55)
        )

        if self.db.count_documents({'user_id':ctx.author.id}) == 0:
            return await ctx.send("no history L bozo")
        
        data = self.db.find().sort("_case_id",-1)
        for entry in data:
            try:
                if entry['user_id'] == user.id:
                    mod_id = entry['moderator_id']
                    reason = entry['reason']
                    time = entry['time']
                    type = entry['case_type']
    
                    mod = ctx.guild.get_member(mod_id).mention
                    if entry['deleted'] != True:
                        em.description += f"\n\n**{type[0].upper() + type[1:]} - Case {entry['_case_id']}**\n- `Reason`: {reason}\n- `Mod`: {mod}\n- `Time`: <t:{int(time)}:t> | <t:{int(time)}:R>"
            except:
                pass
            
        await ctx.send(embed=em)
        
    @commands.command() 
    @commands.has_permissions(administrator=True)
    async def delcase(self, ctx, case_id: int):

        self.db.update_one({"_case_id":case_id},{"$set":{"deleted":True}})
        em = discord.Embed(
            title = ':warning: Case Deleted',
            description = f'Deleted case ID `{case_id}`.',
            colour = discord.Colour.from_rgb(47, 49, 55)
        )
        return await ctx.send(embed=em)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def clearcases(self, ctx, user: discord.Member):

        em = discord.Embed(
            title = ':warning: Cases Cleared',
            description = f'Cases cleared for {user.mention}.',
            colour = discord.Colour.from_rgb(47, 49, 55)
        )
        
        data = self.db.find().sort("_case_id",-1)
        for entry in data:
            try:
                if entry['user_id'] == user.id:
                    case_id = entry['case_id']
                    self.db.update_one({"_case_id":case_id},{"$set":{"deleted":True}})
            except:
                pass
        await ctx.send(embed=em)
    
    @commands.command(aliases = ['umc'], hidden=True)
    @commands.has_permissions(administrator=True)
    async def updatemembercount(self, ctx):

        await self.client.get_channel(929330258816159815).edit(name=f"👤 Members: {len(ctx.guild.members)}")
        await ctx.message.add_reaction('✅')

    @commands.command(aliases=['add-lock','addlock'])
    @commands.has_permissions(administrator=True)
    async def add_lock(self, ctx, channel: discord.TextChannel):

        self.lockdown.insert_one({"_channelid":channel.id})
            
        em = discord.Embed(
            title = ':hammer_pick: Channel Added',
            description = f'Added <#{channel.id}> to lock database.',
            colour = discord.Colour.from_rgb(47, 49, 55)
        )
        em.timestamp = datetime.utcnow()
        await ctx.send(embed=em)

    @commands.command(aliases=['remove-lock','removelock'])
    @commands.has_permissions(administrator=True)
    async def remove_lock(self, ctx, channel: discord.TextChannel):

        self.lockdown.delete_one({"_channelid":channel.id})
            
        em = discord.Embed(
            title = ':hammer_pick: Channel Added',
            description = f'Removed <#{channel.id}> from lock database.',
            colour = discord.Colour.from_rgb(47, 49, 55)
        )
        em.timestamp = datetime.utcnow()
        await ctx.send(embed=em)

    @commands.command(aliases=['lockdown-display', 'lockchannels', 'lc'])
    @commands.has_permissions(administrator=True)
    async def lockdowndisplay(self, ctx):

        data = self.lockdown.find().sort("_channelid",-1)
        desc = ''
        
        for i in data:

            id = i['_channelid']
            desc += f'<#{id}>, '

        await ctx.send(f"Lockdown list: {desc}")
        
    #Lockdown#----------#
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def lockdown(self, ctx, *, reason='No reason provided.'):

        things = self.lockdown.find().sort("_channelid",-1)
        for data in things:
            try:
                _channel = data["_channelid"]
                channel = self.client.get_channel(_channel)
                await channel.set_permissions(ctx.guild.default_role, send_messages=False)
                em = discord.Embed(
                    title = ':lock: Lockdown',
                    description = f'{reason}',
                    colour = discord.Colour.from_rgb(47, 49, 55)
                )
                em.timestamp = datetime.utcnow()
                await channel.send(embed=em)
            except:
                raise
    
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def unlockdown(self, ctx):

        things = self.lockdown.find().sort("_channelid",-1)
        for data in things:
            try:
                _channel = data["_channelid"]
                channel = self.client.get_channel(_channel)
                await channel.set_permissions(ctx.guild.default_role, send_messages=None)
            except:
                pass
        
            
    #Role#--------------#
    @commands.command(aliases=['addrole', 'ar'])
    @commands.cooldown(1, 3, BucketType.user)
    @commands.has_permissions(manage_roles=True)
    async def role(self, ctx, user : discord.Member, *, _role):

        for r in ctx.guild.roles:

            if r.name.lower().startswith(_role.lower()):
                role = r

                if r.position > ctx.author.top_role.position:

                    embed = discord.Embed(
                        description = f'Cannot assign role, that role is above your highest role.',
                        colour = discord.Colour.from_rgb(255, 91, 91)
                    )
                    
                    embed.set_author(name=f'Command Failed', icon_url = ctx.author.avatar.url)            
                    return await ctx.send(embed=embed)

                if r in user.roles:

                    embed = discord.Embed(
                        description = f'{role.mention} role removed from {user.mention}.',
                        colour = discord.Colour.from_rgb(119, 178, 86)
                    )

                    embed.set_author(name=f'Role Removed', icon_url = ctx.author.avatar.url)
                    embed.set_footer(text = f'Role removed by {ctx.author}')
                    await user.remove_roles(role) 
                    return await ctx.send(embed=embed)

                else:
                    await ctx.author.add_roles(r)
                    embed = discord.Embed(
                        description = f'{role.mention} role added to {user.mention}.',
                        colour = discord.Colour.from_rgb(119, 178, 86)
                    )

                    embed.set_author(name=f'Role Added', icon_url = ctx.author.avatar.url)
                    embed.set_footer(text = f'Role added by {ctx.author}')
                    await user.add_roles(role) 
                    return await ctx.send(embed=embed) 

            else:
                pass

    #--------------#
    @role.error
    async def role_error(self, ctx: commands.Context, error: commands.CommandError):

        if isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(
                description = f"Command is on cooldown, try again after **{round(error.retry_after, 1)}** seconds.",
                colour = discord.Colour.from_rgb(255, 91, 91)
            )
            embed.set_author(name=f'Cooldown', icon_url = ctx.author.avatar.url)
            await ctx.send(embed=embed)

        elif isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                description = f'Invalid Arguments. `!role <user> <role name>`.',
                colour = discord.Colour.from_rgb(255, 91, 91)
            )
            embed.set_author(name=f'Command Failed', icon_url = ctx.author.avatar.url)
            await ctx.send(embed=embed)

        elif isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                description = f'You do not have enough permissions to run this command.',
                colour = discord.Colour.from_rgb(255, 91, 91)
            )
            embed.set_author(name=f'Command Failed', icon_url = ctx.author.avatar.url)

            await ctx.send(embed=embed)

    @commands.command(aliases = ["clear", "clean"])
    @commands.has_permissions(administrator=True)
    async def purge(self, ctx, amt: int, announce: str=None):

        if amt <= 100:

            if announce is not None:
                embed = discord.Embed(
                    title = "Purge Complete",
                    description = f"**{amt}** messages cleared by {ctx.author.mention}.",
                    colour = discord.Colour.from_rgb(255, 50, 50)
                )

                embed.timestamp = datetime.utcnow()
                await ctx.message.delete()
                await ctx.channel.purge(limit=amt)
                await ctx.send(embed=embed)

            if announce is None:

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
            
            embed.timestamp = datetime.utcnow()
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

            embed.timestamp = datetime.utcnow()
            await ctx.send(embed=embed)

        if isinstance(error, commands.MissingRequiredArgument):

            embed = discord.Embed(
                title = "Argument Error",
                description = "Missing Argument: `!purge <amount>`.",
                colour = discord.Colour.from_rgb(255, 75, 75)
            )

            embed.timestamp = datetime.utcnow()
            await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Staff(client))