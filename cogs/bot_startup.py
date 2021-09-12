import discord
import datetime, time
import asyncio
from discord.ext import commands
from main import version

class StartUp(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):

        global startTime #global variable to be used later in cog
        global latency
        startTime = time.time() # snapshot of time when listener sends on_ready

        latency = round(self.client.latency * 1000)
        #await self.client.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name="Pornhub LIVE"))
        print('> Bot is now online')
        print(f'> {latency}ms')

        while True:

            await self.client.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name="Pornhub LIVE | .gg/n9me32WTz3"))
            await asyncio.sleep(900)
            await self.client.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name="Chat | !help | .gg/n9me32WTz3"))
            await asyncio.sleep(900)
            
    @commands.command()
    async def ping(self, ctx):
        
        embed = discord.Embed(
        description = f'🏓 Pong! {latency}ms',
        colour = discord.Colour.from_rgb(0, 155, 180)
        ) 
        await ctx.send(embed=embed)

    #create a command in the cog
    @commands.command(aliases = ["stats"])
    async def botstats(self,ctx):

        # what this is doing is creating a variable called 'uptime' and assigning it
        # a string value based off calling a time.time() snapshot now, and subtracting
        # the global from earlier
        uptime = str(datetime.timedelta(seconds=int(round(time.time()-startTime))))
        embed = discord.Embed(
            title = 'Bot Status',
            colour = discord.Colour.from_rgb(0, 208, 255)
        )
        embed.add_field(name='Uptime', value=f'`{uptime}`', inline=True)
        embed.add_field(name='Latency', value=f'`{latency}ms`', inline=True)
        embed.add_field(name='Version', value=f'`{version}`', inline=True)
        embed.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=embed)

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
    
    #@commands.command()
    #async def help(self, ctx):

    #    embed = discord.Embed(
    #        colour = discord.Colour.from_rgb(0, 155, 180)
    #    )

    #    embed.add_field(name='🏓  !ping', value='Shows bot ping.', inline=False)
    #    embed.add_field(name='🍆  !pp', value='Reveals your pp size.', inline=False)
    #    embed.add_field(name='🎱  !8ball', value='Ask the bot a question and get a response.', inline=False)
    #    embed.add_field(name='🎮  !rps', value='Play a game of Rock Paper Scissors with the bot!', inline=False)
    #    embed.add_field(name='✋  !slap', value='Slap a user.', inline=False)
    #    embed.add_field(name='☝️  !thousandyearsofdeath', value='Use Thousand Years of Death on a user.', inline=False)
    #    embed.add_field(name=':coin:  !coinflip', value='Flip a coin to get either heads or tails.', inline=False)
    #    embed.add_field(name='🔢  !randomnumber', value='Get a random number from a min to max number.', inline=False)
    #    embed.add_field(name='🗣️  !say', value='Make the bot say a string of text!', inline=False)
    #    embed.set_footer(text='Bot Version v0.61')

    #    await ctx.send(embed=embed)

def setup(client):
    client.add_cog(StartUp(client))