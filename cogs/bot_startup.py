import nextcord as discord
import datetime, time
import os
import asyncio
from nextcord.ext import commands, tasks
from nextcord import Interaction, SlashOption
from main import version
from pymongo import MongoClient

cluster = MongoClient("mongodb+srv://Cosmo:1H1uqPGjo5CjtHQe@eco.5afje.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
database = cluster["Discord"]
utils = database["Server_Utils"]

#from main import uptimeCounter, ts, tm, th, td

class StartUp(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):

        global startTime #global variable to be used later in cog
        startTime = time.time() # snapshot of time when listener sends on_ready

        global latency
        latency = round(self.client.latency * 1000)

        #await self.client.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name="Pornhub LIVE"))
        print('> Bot is now online')
        print(f'> {latency}ms')
        await self.client.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name="Pornhub LIVE | .gg/ZUTBBya"))
        utils.update_one({"tag":"Bot Info"},{"$set":{"uptime_start":time.time()}})

    @discord.slash_command(name="moe",description="hehe",guild_ids=[581139467381768192])
    async def moe(
        self,
        interaction: Interaction,
    ):
        await interaction.user.move_to(None)
    
    @discord.slash_command(name="ping",description="Bot latency command!",guild_ids=[581139467381768192])
    async def ping(
        self,
        interaction: Interaction,
    ):
        ping = round(self.client.latency * 1000)

        embed = discord.Embed(
            title = ":ping_pong: Pong!",
            description = f'**Bot Ping**: {ping}ms',
            colour = discord.Colour.from_rgb(0, 208, 255)
        )

        embed.timestamp = datetime.datetime.utcnow()
        await interaction.response.send_message(embed=embed)

    @commands.command()
    @commands.is_owner()
    async def rules(self, ctx):
        
        embed2 = discord.Embed(
            title = "━━━━━ Economy Rules ━━━━━━",
            description = 
                "",
            colour = discord.Colour.from_rgb(0, 208, 255)
        )

        embed2.add_field(name="Rule 1: Alts", value="> Using any form of alts // second accounts in Economy is not allowed.", inline=False)
        embed2.add_field(name="Rule 2: Macros & Selfbots", value="> Using any form of macros, selfbots or auto typers in Economy is not allowed", inline=False)
        embed2.add_field(name="Rule 3: Blackmarket Deals", value="> Blackmarket deals and sorts are **completely allowed** in Economy.", inline=False)
        embed2.add_field(name="Rule 4: Glitches & Bugs", value="> Abusing glitches is not allowed and will get you wiped, please report any bugs or glitches with `>bug` if you find any.", inline=False)

        embed = discord.Embed(
            title = "━━━━━ Server Rules ━━━━━━",
            colour = discord.Colour.from_rgb(0, 208, 255)
        )

        embed.add_field(name="Rule 1: Mass Flood", value="> Mass Flooding the chat with huge walls of text/emojis is not allowed.", inline=False)
        embed.add_field(name="Rule 2: Pornography", value="> Discussion of porn and such topics is allowed (as it is a meme server) though actual porn & any type of pornographic content is __strictly not allowed__ on the server.", inline=False)
        embed.add_field(name="Rule 3: Advertising", value="> Advertising other discord servers is not allowed here, this is not a very strict rule but it would be preferred if you don't.", inline=False)
        embed.add_field(name="Rule 4: Don't be an Asshole", value="> We're all here for shits and giggles, usually nothing that happens here should be taken seriously, but if you are asked to stop doing something, stop and don't be an asshole here.", inline=False)

        embed3 = discord.Embed(
            title = "━━━━━ Extra Stuff ━━━━━━",
            colour = discord.Colour.from_rgb(0, 208, 255)
        )

        embed3.add_field(name="⚒️ Bot Updates Ping", value="> You can use the `>updates on` command to enable Vortex Update pings.", inline=False)
        embed3.add_field(name="💰 Economy Updates Ping", value="> You can use the `>economy on` command to enable Economy Update Pings.", inline=False)
        embed3.add_field(name="🎉 Retard Night Ping", value="> You can use the `>retardnight on` command to enable Retard Night Pings.", inline=False)

        await ctx.message.delete()
        await ctx.send(embed=embed)
        await ctx.send(embed=embed2)
        await ctx.send(embed=embed3)

def setup(client):
    client.add_cog(StartUp(client))