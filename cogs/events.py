import nextcord as discord
from nextcord.utils import find
from nextcord.ext import commands
import io
import traceback
import random
from datetime import datetime
from pymongo import MongoClient
from .general import can_level_up, xp_required

cluster = MongoClient("mongodb+srv://Cosmo:1H1uqPGjo5CjtHQe@eco.5afje.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
database = cluster["Discord"]
starboard_db = database["Starboard"]
levels = database["Levels"]

class Events(commands.Cog, description="a"):

    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_member_join(self, user: discord.User):

        #
        guild = self.client.get_guild(581139467381768192)
        channel = self.client.get_channel(735765424108601386)

        member = guild.get_role(870550585701695508)
        r1 = guild.get_role(888689564774973440)
        r2 = guild.get_role(843000224611172403)
        r3 = guild.get_role(889055273757581353)

        """
        embed = discord.Embed(
            description = f"Welcome to Cosmo's Lounge, {user.mention}! We hope you enjoy your stay\n\nYou can use `!colourlist` to see the list of colours available to you.",
            colour=discord.Colour.from_rgb(0, 208, 255)
        )
        """
        text = f":wave: **Welcome!**\n\n{user.mention} just slid into the server! You can run **`!help`** if you want a list of my commands"
        await self.client.get_channel(929330258816159815).edit(name=f"👤 Members: {len(self.client.get_guild(581139467381768192).members)}")
        await channel.send(text)
        await user.add_roles(member)
        await user.add_roles(r1)
        await user.add_roles(r2)
        await user.add_roles(r3)

    @commands.Cog.listener()
    async def on_message(self, ctx):

        # Making sure bot isn't replying to itself
        if ctx.author.id == self.client.user.id:
            return

        # Making sure bot isn't replying to other bots
        if ctx.author.bot:
            return

        
        """
        LEVELS
        if ctx.guild.id == 581139467381768192:

            user = levels.find_one({"_id": ctx.author.id})
            if user is None:
                return levels.insert_one({"_id": ctx.author.id, "level": 1, "xp": 0, "last_xp": 0})

            user_level = user['level']
            user_xp = user['xp']

            if int(datetime.now().timestamp()) >= user['last_xp']:

                # add random xp
                user['xp'] = user_xp + random.randint(15, 50)

                # check if user can level up
                if can_level_up(user_xp, user_level):
                    user['level'] = user_level + 1
                    user['xp'] = 0
                    user['last_xp'] = int(datetime.now().timestamp()) + 10

                    embed = discord.Embed(title="Level Up!", description=f"You levelled up to level **{user_level+1}**!", colour=discord.Colour.from_rgb(0, 208, 255))
                    embed.timestamp = datetime.utcnow()
                    embed.set_author(name=ctx.author.name, icon_url=ctx.author.display_avatar)
                    await ctx.channel.send(embed=embed)
                    return levels.replace_one({"_id": ctx.author.id}, user)

                user['last_xp'] = int(datetime.now().timestamp()) + 10
                return levels.replace_one({"_id": ctx.author.id}, user)
        """
    """
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        emoji = payload.emoji
        guild = self.client.get_guild(581139467381768192)
        starboard = guild.get_channel(999607944599572492)
        channel = guild.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)

        # check if emoji name is the star
        if emoji.name == "⭐":
            for reaction in message.reactions:
                if reaction.emoji == "⭐":
                    if reaction.count >= 3:
                        if message.attachments:
                            if message.content:
                                embed = discord.Embed(description=f"{message.content}\n\n [Jump to message]({message.jump_url})", colour=discord.Colour.from_rgb(0, 208, 255))
                            else:
                                embed = discord.Embed(description=f"[Jump to message]({message.jump_url})", colour=discord.Colour.from_rgb(0, 208, 255))
                            embed.set_image(url=message.attachments[0])
                            embed.set_author(name=message.author.name, icon_url=message.author.display_avatar)
                            embed.set_footer(text=f"#{channel.name}")
                            embed.timestamp = datetime.utcnow()
                            await starboard.send(embed=embed)
                        else:
                            embed = discord.Embed(description=f"{message.content}\n\n[Jump to message]({message.jump_url})", colour=discord.Colour.from_rgb(0, 208, 255))
                            embed.set_author(name=message.author.name, icon_url=message.author.display_avatar)
                            embed.set_footer(text=f"#{channel.name}")
                            embed.timestamp = datetime.utcnow()
                            await starboard.send(embed=embed)

    """
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        emoji = payload.emoji
        guild = self.client.get_guild(581139467381768192)
        starboard = guild.get_channel(999607944599572492)
        channel = guild.get_channel(payload.channel_id)

        # message reacted to
        message = await channel.fetch_message(payload.message_id)

        # check if emoji name is the star
        if emoji.name == "⭐":
            for reaction in message.reactions:
                if reaction.emoji == "⭐":
                    if reaction.count >= 3:

                        # check if message has been starred before
                        if starboard_db.find_one({"message_id": message.id}) is None:


                            # check if message has any images
                            if message.attachments:
                                if message.content:
                                    embed = discord.Embed(description=f"{message.content}\n\n:star: **{reaction.count}**     [Jump to message]({message.jump_url})", colour=discord.Colour.from_rgb(0, 208, 255))
                                else:  # check if message has content or is just plain image
                                    embed = discord.Embed(description=f":star: **{reaction.count}**     [Jump to message]({message.jump_url})", colour=discord.Colour.from_rgb(0, 208, 255))
                                embed.set_image(url=message.attachments[0])
                                embed.set_author(name=message.author.name, icon_url=message.author.display_avatar)
                                embed.set_footer(text=f"#{channel.name}")
                                embed.timestamp = datetime.utcnow()
                                starboard_message = await starboard.send(embed=embed)

                                starboard_db.insert_one({
                                    "message_id": message.id,
                                    "starboard_message_id": starboard_message.id,
                                })

                            # if message has no images
                            else:
                                embed = discord.Embed(description=f"{message.content}\n\n:star: **{reaction.count}**     [Jump to message]({message.jump_url})", colour=discord.Colour.from_rgb(0, 208, 255))
                                embed.set_author(name=message.author.name, icon_url=message.author.display_avatar)
                                embed.set_footer(text=f"#{channel.name}")
                                embed.timestamp = datetime.utcnow()
                                starboard_message = await starboard.send(embed=embed)

                                starboard_db.insert_one({
                                    "message_id": message.id,
                                    "starboard_message_id": starboard_message.id,
                                })

                        else:

                            msg_id = starboard_db.find_one({"message_id": message.id})['starboard_message_id']
                            starboard_message =  await starboard.fetch_message(msg_id)

                            # check if message has any images
                            if message.attachments:
                                if message.content:
                                    embed = discord.Embed(description=f"{message.content}\n\n:star: **{reaction.count}**     [Jump to message]({message.jump_url})", colour=discord.Colour.from_rgb(0, 208, 255))
                                else:  # check if message has content or is just plain image
                                    embed = discord.Embed(description=f":star: **{reaction.count}**     [Jump to message]({message.jump_url})", colour=discord.Colour.from_rgb(0, 208, 255))
                                embed.set_image(url=message.attachments[0])
                                embed.set_author(name=message.author.name, icon_url=message.author.display_avatar)
                                embed.set_footer(text=f"#{channel.name}")
                                embed.timestamp = datetime.utcnow()
                                await starboard_message.edit(embed=embed)

                            # if message has no images
                            else:
                                embed = discord.Embed(description=f"{message.content}\n\n:star: **{reaction.count}**    [Jump to message]({message.jump_url})", colour=discord.Colour.from_rgb(0, 208, 255))
                                embed.set_author(name=message.author.name, icon_url=message.author.display_avatar)
                                embed.set_footer(text=f"#{channel.name}")
                                embed.timestamp = datetime.utcnow()
                                await starboard_message.edit(embed=embed)
    
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        
        errorColour = discord.Colour.from_rgb(255, 75, 75)

        if hasattr(ctx.command, 'on_error'):
            return

        # Missing Arguments for command
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                title = f":x: Argument Error",
                description=f"**Usage**\n`!{ctx.command.name} {ctx.command.signature}`",
                colour = errorColour
            )
            embed.timestamp = datetime.utcnow()
            #embed.set_thumbnail(url=ctx.author.display_avatar)
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