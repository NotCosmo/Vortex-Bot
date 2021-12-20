# Main Imports

import nextcord as discord
import datetime
import asyncio
import random
import aiohttp

# Side Imports

from main import timeNow
from nextcord.ext import commands
from nextcord.ext.commands import BucketType

#---------------------COG SETUP---------------------#

class FunCmds(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def elite(self, ctx):

        em = discord.Embed(
            title = "Elite YouTube",
            description = "Very cool youtuber that does videos and shit you should [subscribe](https://m.youtube.com/channel/UC0eLyb_Z4FKrDN7JS_duvWQ).",
            colour = discord.Colour.from_rgb(71, 160, 196)
        )
        em.timestamp = datetime.datetime.utcnow()
        await ctx.reply(embed=em, mention_author=False)

    #8ball#--------------#
    @commands.command(help = "- Ask the Magic 8ball a question.\n\n__**Usage**__\n- `!8ball <question>`", aliases = ['8ball'])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def _8ball(self, ctx, *, question):
        responses = [
			'It is certain.', 
			'It is decidedly so.', 
			'Without a doubt.',
			'Yes - definitely.', 
			'You may rely on it.', 
			'As I see it, yes',
			'Most likely.', 
			'Outlook is good.', 
			'Yes.', 
			'Signs point to yes.',
			'Reply hazy, try again.', 
			'Ask again later.',
			'It is better to not tell you now.', 
			'Cannot predict now.',
			'Concentrate and ask again.', 
			"Don't count on it.", 
			'My reply is no.',
			'My sources say no.', 
			'Outlook is not so good.', 
			'Very doubtful.']
        
        embed = discord.Embed(
            description = f'**{question}**: {random.choice(responses)}',
            colour = discord.Colour.from_rgb(0, 155, 180)
        )
        embed.set_author(name='🎱  8Ball Machine', icon_url=ctx.author.avatar.url)
        embed.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=embed)

    #pp#--------------#
    @commands.command()
    @commands.cooldown(1, 10, BucketType.user)
    async def pp(self, ctx, user: discord.Member=None):
        sizes = [
            '8D',
            '8=D',
            '8==D',
            '8===D',
            '8====D',
            '8=====D',
            '8======D',
            '8========D',
            '8=========D',
            '8==========D',
            '8===========D',
            '8============D',
            '8=============D',
            '8==============D',
            '8===============D',
            '8================D',
            '8=================D',
            '8==================D',
            '8===================D',
            '8====================D',
            '8=====================D',
            '8======================D',
            '8=======================D',
            '8========================D',
            'none existent.',
            'so small even Zeus himself is afraid.',
        ]
        text = random.choice(sizes)
        x = random.randint(0, 999)
        if x == 999:
            text = 'so small that you need to have a microscope in the Quantum Realm to see it.'
            
        if user is None:
            embed = discord.Embed(
                description = f"{ctx.author.mention}'s penis size is {text}",
                colour = discord.Colour.from_rgb(0, 155, 180)
            )

            embed.set_author(name=f'Penis Machine', icon_url=ctx.author.avatar.url)
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=embed)

        else:
            embed = discord.Embed(
                description = f"{user.mention}'s penis size is {text}",
                colour = discord.Colour.from_rgb(0, 155, 180)
            )

            embed.set_author(name=f'Penis Machine', icon_url=ctx.author.avatar.url)
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=embed)
    
    #luck#--------------#
    @commands.command()
    @commands.cooldown(1, 10, BucketType.user)
    async def luck(self, ctx, *, thing):
        x = random.randint(0, 100)
        if thing == 'baco falling down the stairs':
            x = 100

        embed = discord.Embed(
            description = f"The chance of **{thing}** is **{x}%**!",
            colour = discord.Colour.from_rgb(0, 155, 180)
        )
        embed.set_author(name=f'Luck Machine', icon_url=ctx.author.avatar.url)
        embed.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=embed)

    #rps#--------------#
    @commands.command()
    @commands.cooldown(1, 10, BucketType.user)
    async def rps(self, ctx, *, userchoice):
        
        winner = ''
        botchoices = ['Rock', 'Paper', 'Scissors']

        if userchoice == 'rock':
            userchoice = 'Rock'
        elif userchoice == 'paper':
            userchoice = 'Paper'
        elif userchoice == 'scissors':
            userchoice = 'Scissors'

        botchoice = random.choice(botchoices)
        if userchoice == 'Rock' and botchoice == 'Rock':
            winner = f":person_red_hair: {userchoice} VS. {botchoice} :robot: \n \n:trophy: It's a tie!"
            #winner = f":trophy: It's a tie!\n \n:robot: Bot Choice: {botchoice}"

        elif userchoice == 'Rock' and botchoice == 'Paper':
            winner = f":person_red_hair: {userchoice} VS. {botchoice} :robot: \n \n:trophy: Vortex Wins!"
            #winner = f":trophy: Vortex wins!\n \n:robot: Bot Choice: {botchoice}"

        elif userchoice == 'Rock' and botchoice == 'Scissors':
            winner = f":person_red_hair: {userchoice} VS. {botchoice} :robot: \n \n:trophy: {ctx.author.mention} Wins!"
            #winner = f":trophy: {ctx.author.mention} wins!\n \n:robot: Bot Choice: {botchoice}" 

        elif userchoice == 'Paper' and botchoice == 'Rock':
            winner = f":person_red_hair: {userchoice} VS. {botchoice} :robot: \n \n:trophy: {ctx.author.mention} Wins!"
            #winner = f":trophy: {ctx.author.mention} wins!\n \n:robot: Bot Choice: {botchoice}"

        elif userchoice == 'Paper' and botchoice == 'Paper':
            winner = f":person_red_hair: {userchoice} VS. {botchoice} :robot: \n \n:trophy: It's a tie!"
            #winner = f":trophy: It's a tie!\n \n:robot: Bot Choice: {botchoice}"

        elif userchoice == 'Paper' and botchoice == 'Scissors':
            winner = f":person_red_hair: {userchoice} VS. {botchoice} :robot: \n \n:trophy: Vortex Wins!"
            #winner = f":trophy: Vortex wins!\n \n:robot: Bot Choice: {botchoice}"

        elif userchoice == 'Scissors' and botchoice == 'Rock':
            winner = f":person_red_hair: {userchoice} VS. {botchoice} :robot: \n \n:trophy: Vortex Wins!"
            #winner = f":trophy: Vortex wins!\n \n:robot: Bot Choice: {botchoice}"

        elif userchoice == 'Scissors' and botchoice == 'Paper':
            winner = f":person_red_hair: {userchoice} VS. {botchoice} :robot: \n \n:trophy: {ctx.author.mention} Wins!"
            #winner = f":trophy: {ctx.author.mention} wins!\n \n:robot: Bot Choice: {botchoice}"

        elif userchoice == 'Scissors' and botchoice == 'Scissors':
            winner = f":person_red_hair: {userchoice} VS. {botchoice} :robot: \n \n:trophy: It's a tie!"
            #winner = f":trophy: It's a tie!\n \n:robot: Bot Choice: {botchoice}"

        if userchoice in botchoices:
            embed = discord.Embed(
                description = winner,
                colour = discord.Colour.from_rgb(0, 208, 255)
            )
            embed.set_author(name=f'{ctx.author}', icon_url=ctx.author.avatar.url)
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=embed)

        else:
            embed = discord.Embed(
                description = "**Invalid Input**: `!rps <rock/paper/scissors`.",
                colour = discord.Colour.from_rgb(255, 75, 75)
            )
            embed.set_author(name=f'Error', icon_url=ctx.author.avatar.url)
            embed.timestamp = datetime.datetime.utcnow()


    #Gay#--------------#
    @commands.command()
    @commands.cooldown(1, 10, BucketType.user)
    async def gay(self, ctx, user: discord.Member=None):
        percent = random.randint(0, 100)

        if user is None:
            embed = discord.Embed(
                description = f'{ctx.author.mention} is {percent}% gay.',
                colour = discord.Colour.from_rgb(0, 155, 180)
            )
            
        else:
            embed = discord.Embed(
                description = f'{user.mention} is {percent}% gay.',
                colour = discord.Colour.from_rgb(0, 155, 180)
            )

        embed.timestamp = datetime.datetime.utcnow()
        embed.set_author(name=f'Gay Machine', icon_url=ctx.author.avatar.url)
        await ctx.send(embed=embed)
    
    #Racist#--------------#
    @commands.command()
    @commands.cooldown(1, 10, BucketType.user)
    async def racist(self, ctx, user: discord.Member=None):
        percent = random.randint(0, 100)

        if user is None:
            embed = discord.Embed(
                description = f'{ctx.author.mention} is {percent}% racist.',
                colour = discord.Colour.from_rgb(0, 155, 180)
            )
            embed.timestamp = datetime.datetime.utcnow()
            embed.set_author(name=f'Racist Machine', icon_url=ctx.author.avatar.url)
            await ctx.send(embed=embed)

        else:
            embed = discord.Embed(
                description = f'{user.mention} is {percent}% racist.',
                colour = discord.Colour.from_rgb(0, 155, 180)
            )
            embed.timestamp = datetime.datetime.utcnow()
            embed.set_author(name=f'Racist Machine', icon_url=ctx.author.avatar.url)
            await ctx.send(embed=embed)
        

    #Pedo#--------------#
    @commands.command()
    @commands.cooldown(1, 10, BucketType.user)
    async def pedo(self, ctx, user: discord.Member=None):
        percent = random.randint(0, 100)

        if user is None:
            embed = discord.Embed(
            description = f'{ctx.author.mention} is {percent}% a pedophile.',
            colour = discord.Colour.from_rgb(0, 155, 180)
            )

        else:
            embed = discord.Embed(
                description = f'{user.mention} is {percent}% a pedophile.',
                colour = discord.Colour.from_rgb(0, 155, 180)
            )
        
        embed.timestamp = datetime.datetime.utcnow()
        embed.set_author(name=f'Pedo Machine', icon_url=ctx.author.avatar.url)
        await ctx.send(embed=embed)

    #Slap#--------------#
    @commands.command()
    @commands.cooldown(1, 10, BucketType.user)
    async def slap(self, ctx, user: discord.Member):

        embed = discord.Embed(
            description= f'{ctx.author.mention} slapped {user.mention}.',
            colour=discord.Colour.from_rgb(0, 155, 180)
        )

        url1 = 'https://media.giphy.com/media/Zau0yrl17uzdK/giphy.gif'
        url2 = 'https://media.giphy.com/media/xUO4t2gkWBxDi/giphy.gif'
        url3 = 'https://media.giphy.com/media/m6etefcEsTANa/source.gif'
        url4 = 'https://media.giphy.com/media/mEtSQlxqBtWWA/source.gif'
        url5 = 'https://media.giphy.com/media/j3iGKfXRKlLqw/giphy.gif'
        url6 = 'https://media.giphy.com/media/siS34ziU0gxsQ/giphy.gif'
        url7 = 'https://cdn.weeb.sh/images/ry2tWxcyf.gif'
        url8 = 'https://media.giphy.com/media/AlsIdbTgxX0LC/giphy.gif'
        url9 = 'https://media.giphy.com/media/Z5zuypybI5dYc/giphy.gif'
        url10 = 'https://media.giphy.com/media/CeDZGQE0qWjkc/giphy.gif'
        url11 = 'https://media.giphy.com/media/RrLbvyvatbi36/giphy.gif'
        url12 = 'https://media.giphy.com/media/vcShFtinE7YUo/giphy.gif'
        url13 = 'https://media.giphy.com/media/pPdNABXupIM2R7MCX2/giphy.gif'
        url14 = 'https://media.giphy.com/media/jEYH3RJVXK8Ba/giphy.gif'
        url15 = 'https://media.giphy.com/media/RXGNsyRb1hDJm/giphy.gif'

        gifs = [
            url1, url2, url3, url4, url5, url6, url7, url8, url9, url10, url11,
            url12, url13, url14, url15
        ]

        gif = random.choice(gifs)
        embed.set_image(url=gif)
        embed.set_author(name=f'{ctx.author}', icon_url=ctx.author.avatar.url)
        embed.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=embed)

    #TYOD#--------------#
    @commands.command(aliases = ['tyod'])
    @commands.cooldown(1, 10, BucketType.user)
    async def thousandyearsofdeath(self, ctx, user: discord.Member):

        embed = discord.Embed(
            description = f'{ctx.author.mention} has used Thousand Years of Death on {user.mention}',
            colour=discord.Colour.from_rgb(0, 155, 180)
        )

        embed.set_image(url='https://media.giphy.com/media/Do5GRTYRIhSFy/giphy.gif')
        embed.set_author(name=f'{ctx.author}', icon_url=ctx.author.avatar.url)
        embed.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=embed)

    #RandomNum#----------#
    @commands.command()
    @commands.cooldown(1, 10, BucketType.user)
    async def randomnumber(self, ctx, min: int, max: int):

        embed = discord.Embed(
            description = f'{random.randint(min,max)}',
            colour = discord.Colour.from_rgb(0, 155, 180)
        )   
        embed.set_author(name=f'{ctx.author}', icon_url=ctx.author.avatar.url)
        embed.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=embed)

    #Coinflip#--------------#
    @commands.command(aliases = ['cointoss'])
    @commands.cooldown(1, 10, BucketType.user)
    async def coinflip(self, ctx):
        possible = ['Heads.', 'Tails.']

        embed = discord.Embed(
            description = f':coin: You got: {random.choice(possible)}',
            colour = discord.Colour.from_rgb(0, 155, 180)
        )

        embed.set_author(name=f'{ctx.author}', icon_url=ctx.author.avatar.url)
        embed.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=embed)

    #Say#--------------#
    @commands.command()
    @commands.cooldown(1, 10, BucketType.user)
    async def say(self, ctx, *, message):
        embed = discord.Embed(
            description = message,
            colour = discord.Colour.from_rgb(0, 155, 180)
        )

        embed.set_author(name=f'{ctx.author}', icon_url=ctx.author.avatar.url)
        
        embed.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=embed)
        await ctx.message.delete()


    #sus#--------------#
    @commands.command()
    @commands.cooldown(1, 10, BucketType.user)
    async def sus(self, ctx, user: discord.Member=None):

        percent = random.randint(0, 100)
        if percent > 60:
            text1 = ', you are the impostor.'
            text2 = ', they are the impostor.'
        else:
            text1 = ', you are a crewmate.'
            text2 = ', they are a crewmate.'

        if user is None:
            embed = discord.Embed(
            description = f'{ctx.author.mention} you are {percent}% sus{text1}',
            colour = discord.Colour.from_rgb(0, 155, 180)
            )

        else:
            embed = discord.Embed(
                description = f'{user.mention} is {percent}% sus{text2}',
                colour = discord.Colour.from_rgb(0, 155, 180)
            )
        
        embed.timestamp = datetime.datetime.utcnow()
        embed.set_author(name=f'Sus Machine', icon_url=ctx.author.avatar.url)
        await ctx.send(embed=embed)

    #simp#--------------#
    @commands.command()
    @commands.cooldown(1, 10, BucketType.user)
    async def simp(self, ctx, user: discord.Member=None):

        percent = random.randint(0, 100)

        if user is None:
            embed = discord.Embed(
            description = f'{ctx.author.mention} you are {percent}% a simp.',
            colour = discord.Colour.from_rgb(0, 155, 180)
            )

        else:
            embed = discord.Embed(
                description = f'{user.mention} is {percent}% a simp.',
                colour = discord.Colour.from_rgb(0, 155, 180)
            )
        
        embed.timestamp = datetime.datetime.utcnow()
        embed.set_author(name=f'Simp Machine', icon_url=ctx.author.avatar.url)
        await ctx.send(embed=embed)

    #retard#--------------#
    @commands.command()
    @commands.cooldown(1, 10, BucketType.user)
    async def retard(self, ctx, user: discord.Member=None):

        percent = random.randint(0, 100)

        if user is None:
            embed = discord.Embed(
            description = f'{ctx.author.mention} you are {percent}% a retard.',
            colour = discord.Colour.from_rgb(0, 155, 180)
            )

        else:
            embed = discord.Embed(
                description = f'{user.mention} is {percent}% a retard.',
                colour = discord.Colour.from_rgb(0, 155, 180)
            )
        
        embed.timestamp = datetime.datetime.utcnow()
        embed.set_author(name=f'Retard Machine', icon_url=ctx.author.avatar.url)
        await ctx.send(embed=embed)

    #poggers#--------------#
    @commands.command()
    @commands.cooldown(1, 10, BucketType.user)
    async def pog(self, ctx, user: discord.Member=None):

        percent = random.randint(0, 100)

        if user is None:
            embed = discord.Embed(
            description = f'{ctx.author.mention} you are {percent}% poggers!',
            colour = discord.Colour.from_rgb(0, 155, 180)
            )

        else:
            embed = discord.Embed(
                description = f'{user.mention} is {percent}% poggers!',
                colour = discord.Colour.from_rgb(0, 155, 180)
            )
        embed.timestamp = datetime.datetime.utcnow()
        embed.set_author(name=f'Pog Machine', icon_url=ctx.author.avatar.url)
        await ctx.send(embed=embed)

    #poop#--------------#
    @commands.command(aliases=['poop'])
    @commands.cooldown(1, 10, BucketType.user)
    async def poopsize(self, ctx, user: discord.Member=None):

        poopsizes = [
            'extra very large',
            'very Large',
            'super large',
            'large',
            'mediocre size',
            'you just got into the poop industry size',
            'small',
            'super small',
        ]
        size = random.choice(poopsizes)
        x = random.randint(0, 42069)
        if x == 42069:
            size = 'Moe is afraid of you size'

        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)

        if user is None:
            embed = discord.Embed(
            description = f'{ctx.author.mention} your poop size is **{size}**',
            colour = discord.Colour.from_rgb(r, g, b)
            )

        else:
            embed = discord.Embed(
                description = f"{user.mention}'s poop size is **{size}**'",
                colour = discord.Colour.from_rgb(r, g, b)
            )

        embed.timestamp = datetime.datetime.utcnow()
        embed.set_author(name=f'Poop Machine', icon_url=ctx.author.avatar.url)
        embed.set_footer(text='*Embed Colour decides your shit colour!*')
        await ctx.send(embed=embed)

    #drip#--------------#
    @commands.command()
    @commands.cooldown(1, 10, BucketType.user)
    async def drip(self, ctx, user: discord.Member=None):

        dripamt = random.randint(0, 100)

        if user is None:
                embed = discord.Embed(
                    description = f'{ctx.author.mention} you are **{dripamt}%** drip!',
                    colour = discord.Colour.from_rgb(0, 155, 180)
                )
                embed.set_author(name=f'Drip Machine', icon_url=ctx.author.avatar.url)
                embed.timestamp = datetime.datetime.utcnow()
                await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                description = f"{user.mention} is **{dripamt}%** drip!",
                colour = discord.Colour.from_rgb(0, 155, 180)
            )
            
            embed.timestamp = datetime.datetime.utcnow()
            embed.set_author(name=f'Drip Machine', icon_url=ctx.author.avatar.url)
            await ctx.send(embed=embed)
    
    #halal#--------------#
    @commands.command()
    @commands.cooldown(1, 10, BucketType.user)
    async def halal(self, ctx, user: discord.Member=None):

        amt = random.randint(0, 100)

        if user is None:
            embed = discord.Embed(
            description = f'{ctx.author.mention} you are **{amt}%** halal!',
            colour = discord.Colour.from_rgb(0, 155, 180)
            )
            embed.timestamp = datetime.datetime.utcnow()
            embed.set_author(name=f'Halal Machine', icon_url=ctx.author.avatar.url)
            await ctx.send(embed=embed)

        else:
            embed = discord.Embed(
                description = f"{user.mention} is **{amt}%** halal!",
                colour = discord.Colour.from_rgb(0, 155, 180)
            )

            embed.timestamp = datetime.datetime.utcnow()
            embed.set_author(name=f'Halal Machine', icon_url=ctx.author.avatar.url)
            await ctx.send(embed=embed)

    #Horny#--------------#
    @commands.command()
    @commands.cooldown(1, 10, BucketType.user)
    async def horny(self, ctx, user: discord.Member=None):
        percent = random.randint(0, 100)

        if user is None:
            user = ctx.author
            
        else:
            user = user

        if ctx.author.id == 843131902290427974 or user.id == 843131902290427974:
            percent = 100
        
        elif ctx.author.id == 656277190916440065 or user.id == 656277190916440065:
            percent = -69

        embed = discord.Embed(
            description = f'{user.mention} is {percent}% horny.',
            colour = discord.Colour.from_rgb(0, 155, 180)
        )

        embed.timestamp = datetime.datetime.utcnow()
        embed.set_author(name=f'Horny Machine', icon_url=ctx.author.avatar.url)
        await ctx.send(embed=embed)

    #weeb#--------------#
    @commands.command()
    @commands.cooldown(1, 10, BucketType.user)
    async def weeb(self, ctx, user: discord.Member=None):
        percent = random.randint(0, 100)

        if user is None:
            user = ctx.author
            
        else:
            user = user

        embed = discord.Embed(
            description = f'{user.mention} is {percent}% a weeb.',
            colour = discord.Colour.from_rgb(0, 155, 180)
        )

        embed.timestamp = datetime.datetime.utcnow()
        embed.set_author(name=f'Weeb Machine', icon_url=ctx.author.avatar.url)
        await ctx.send(embed=embed)

    #weeb#--------------#
    @commands.command(aliases = ['les'])
    @commands.cooldown(1, 10, BucketType.user)
    async def lesbian(self, ctx, user: discord.Member=None):
        percent = random.randint(0, 100)

        if user is None:
            user = ctx.author
            
        else:
            user = user

        embed = discord.Embed(
            description = f'{user.mention} is {percent}% a lesbian.',
            colour = discord.Colour.from_rgb(0, 155, 180)
        )

        embed.timestamp = datetime.datetime.utcnow()
        embed.set_author(name=f'Lesbian Machine', icon_url=ctx.author.avatar.url)
        await ctx.send(embed=embed)

    #weeb#--------------#
    @commands.command(aliases = ['bisexual'])
    @commands.cooldown(1, 10, BucketType.user)
    async def bi(self, ctx, user: discord.Member=None):
        percent = random.randint(0, 100)

        if user is None:
            user = ctx.author
            
        else:
            user = user

        embed = discord.Embed(
            description = f'{user.mention} is {percent}% bi.',
            colour = discord.Colour.from_rgb(0, 155, 180)
        )

        embed.timestamp = datetime.datetime.utcnow()
        embed.set_author(name=f'Bi Machine', icon_url=ctx.author.avatar.url)
        await ctx.send(embed=embed)

    #cookie#-------------------------#
    @commands.command()
    @commands.cooldown(1, 5, BucketType.user)
    async def cookie(self, ctx, user: discord.Member=None):

        if user is None:
            embed = discord.Embed(
                description = f"You can't give a cookie to yourself! Give it to someone else {ctx.author.mention}!",
                colour = user.colour
            )
            embed.timestamp = datetime.datetime.utcnow()
            embed.set_author(name=f'Cookie', icon_url=ctx.author.avatar.url)
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                description = f"{ctx.author.mention} has given {user.mention} a cookie! :cookie:",
                colour = user.colour
            )
            embed.timestamp = datetime.datetime.utcnow()
            embed.set_author(name=f'Cookie', icon_url=ctx.author.avatar.url)
            await ctx.send(embed=embed)

    #shoot#------------------------#
    @commands.command()
    @commands.cooldown(1, 5, BucketType.user)
    async def shoot(self, ctx, user: discord.Member=None):

        if user is None:
            await ctx.send(f"You need to provide a user to shoot! {ctx.author.mention}")

        await ctx.send(f"Oh no, {ctx.author.mention} has shot :gun: {user.mention}")

    @commands.command()
    @commands.cooldown(1, 10, BucketType.user)
    async def deathmatch(self, ctx, user2: commands.MemberConverter):
        user = ctx.author

        embed = discord.Embed(
            title = f"{user.name} **VS** {user2.name}",
            colour = discord.Colour.red()
        )

        userHealth = 100
        user2Health = 100
        embed.add_field(name=f"{user.name} Health", value = f":heart: {userHealth}", inline=True)
        embed.add_field(name=f"{user2.name} Health", value = f":heart: {user2Health}", inline=True)

        hurtmsg = [", ouch that must've hurt!", ", ouch!"]
        
        msg = await ctx.send(embed=embed)
        while userHealth > 0 and user2Health > 0:
            embed2 = discord.Embed(
                title = f"{user.name} **VS** {user2.name}",
                colour = discord.Colour.red()
            )
            
            dmg1 = random.randint(1, 20)
            user2Health = user2Health - dmg1
            embed2.add_field(name=f"{user.name} Health", value = f":heart: **{userHealth}**", inline=True)
            embed2.add_field(name=f"{user2.name} Health", value = f":heart: **{user2Health}**", inline=True)
            embed2.add_field(name="Last Action", value=f"{user.name} hit {user2.name} for **{dmg1}**{random.choice(hurtmsg)}", inline=False)
            embed2.set_thumbnail(url=user.avatar.url)

            await msg.edit(embed=embed2)
            await asyncio.sleep(2)
            
            embed3 = discord.Embed(
                title = f"{user.name} **VS** {user2.name}",
                colour = discord.Colour.red()
            )

            dmg2 = random.randint(1, 20)
            userHealth = userHealth - dmg2
            embed3.add_field(name=f"{user.name} Health", value = f":heart: **{userHealth}**", inline=True)
            embed3.add_field(name=f"{user2.name} Health", value = f":heart: **{user2Health}**", inline=True)
            embed3.add_field(name="Last Action", value=f"{user2.name} hit {user.name} for **{dmg2}**{random.choice(hurtmsg)}", inline=False)
            embed3.set_thumbnail(url=user2.avatar.url)

            await msg.edit(embed=embed3)
            await asyncio.sleep(2)

        if userHealth <= 0:
            
            if user2Health <= 0:
                embed = discord.Embed(
                    title = f"It's a tie! Both players are dead.",
                    colour = discord.Colour.from_rgb(75, 255, 75)
                )
                await ctx.send(embed=embed)

            else:
                embed = discord.Embed(
                    title = f"{user2.name} has won!",
                    colour = discord.Colour.from_rgb(75, 255, 75)
                )
                await ctx.send(embed=embed)

        elif user2Health <= 0:
            
            if userHealth <= 0:
                embed = discord.Embed(
                    title = f"It's a tie! Both players are dead.",
                    colour = discord.Colour.from_rgb(75, 255, 75)
                )
                await ctx.send(embed=embed)

            else:
                embed = discord.Embed(
                    title = f"{user.name} has won!",
                    colour = discord.Colour.from_rgb(75, 255, 75)
                )
                await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 10, BucketType.user)
    async def animal(self, ctx, *, animal):

        if animal == 'dog':
            animal = 'Dog'
        
        if animal == 'cat':
            animal = 'Cat'

        if animal == 'panda':
            animal = 'Panda'

        if animal == 'fox':
            animal = 'Fox'

        if animal == 'bird':
            animal = 'Bird'

        if animal == 'koala':
            animal = 'Koala'

        if animal == 'red panda':
            animal = 'red_panda'

        if animal == 'raccoon':
            animal = 'Raccoon'

        if animal == 'kangaroo':
            animal = 'Kangaroo'

        async with aiohttp.ClientSession() as cs:
            async with cs.get(f"https://some-random-api.ml/animal/{animal}") as r:
                data = await r.json()

                if animal == "red_panda":
                    animal = "Red Panda"

                embed = discord.Embed(
                    title = animal,
                    description = 'Random Fact: ' + data["fact"],
                    colour = discord.Colour.from_rgb(0, 208, 255)
                )
                embed.set_image(url=data["image"])
                embed.timestamp = datetime.datetime.utcnow()
                await ctx.send(embed=embed)

    @animal.error
    async def animal_error(self, ctx, error):

        if isinstance(commands.MissingRequiredArgument):
            embed = discord.Embed(
                description = "Invalid Search Query, please try one of the following: Dog, Cat, Panda, Fox, Red Panda, Koala, Bird, Raccoon, Kangaroo",
                colour = discord.Colour.from_rgb(255, 75, 75)
            )
            embed.timestamp = datetime.datetime.utcnow()
            embed.set_author(name="Search Error", icon_url=ctx.author.avatar.url)
            await ctx.send(embed=embed)

        if isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(
                description = f":stopwatch: Command is on cooldown, please try again in {round(error.retry_after, 1)} seconds.",
                colour = discord.Colour.from_rgb(255, 75, 75)
            )
            embed.set_author(name="Cooldown", icon_url=ctx.author.avatar.url)
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=embed, delete_after=5)

    @commands.command()
    @commands.cooldown(1, 10, BucketType.user)
    async def wink(self, ctx, user: discord.Member):
        embed = discord.Embed(
            title = f"{ctx.author.name} winked at {user.name}! :wink:",
            colour = discord.Colour.from_rgb(0, 208, 255)
        )
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://some-random-api.ml/animu/wink") as r:
                data = await r.json()
                embed.set_image(url=data["link"])
                await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 10, BucketType.user)
    async def hug(self, ctx, user: discord.Member):
        embed = discord.Embed(
            title = f"{ctx.author.name} hugged {user.name}!",
            colour = discord.Colour.from_rgb(0, 208, 255)
        )
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://some-random-api.ml/animu/hug") as r:
                data = await r.json()
                embed.set_image(url=data["link"])
                await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 10, BucketType.user)
    async def pat(self, ctx, user: discord.Member):
        embed = discord.Embed(
            title = f"{ctx.author.name} pat {user.name}!",
            colour = discord.Colour.from_rgb(0, 208, 255)
        )
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://some-random-api.ml/animu/pat") as r:
                data = await r.json()
                embed.set_image(url=data["link"])
                await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 10, BucketType.user)
    async def joke(self, ctx):

        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://some-random-api.ml/joke") as r:
                data = await r.json()
                await ctx.reply(data["joke"])

    @commands.command()
    @commands.cooldown(1, 10, BucketType.user)
    async def encode(self, ctx, *, message):

        async with aiohttp.ClientSession() as cs:
            async with cs.get(f"https://some-random-api.ml/binary?encode={message}") as r:
                data = await r.json()
                text = data["binary"]
                
                embed = discord.Embed(
                    description = f":white_check_mark: | Encoded Data: **{text}**",
                    colour = discord.Colour.from_rgb(0, 208, 255)
                )
                embed.set_author(name="Binary Encoder", icon_url=ctx.author.avatar.url)
                embed.timestamp = datetime.datetime.utcnow()
                await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 10, BucketType.user)
    async def decode(self, ctx, *, message):

        async with aiohttp.ClientSession() as cs:
            async with cs.get(f"https://some-random-api.ml/binary?decode={message}") as r:
                data = await r.json()
                text = data["text"]
                
                embed = discord.Embed(
                    description = f":white_check_mark: | Encoded Data: **{text}**",
                    colour = discord.Colour.from_rgb(0, 208, 255)
                )
                embed.set_author(name="Binary Decoder", icon_url=ctx.author.avatar.url)
                embed.timestamp = datetime.datetime.utcnow()
                await ctx.send(embed=embed)

    @commands.command(aliases = ['piss'])
    async def pisson(self, ctx, user: discord.Member=None):

        if user is None:
            user = ctx.author
            text = f"{user.mention} has pissed themselves!"

        else:
            user = user
            text = f"{ctx.author.mention} pissed on {user.mention}!"

        em = discord.Embed(
            description = text,
            colour = discord.Colour.from_rgb(0, 208, 255)
        )

        em.set_author(name="Pissing Machine", icon_url=ctx.author.avatar.url)
        em.timestamp = datetime.datetime.utcnow()
        await ctx.reply(embed=em)

    @commands.command(aliases = ['cum'])
    async def cumon(self, ctx, user: discord.Member=None):

        if user is None:
            user = ctx.author
            text = f"{user.mention} tried to cum on their own, fucking weirdo innit."

        else:
            user = user
            text = f"{ctx.author.mention} cummed on {user.mention}!"

        em = discord.Embed(
            description = text,
            colour = discord.Colour.from_rgb(0, 208, 255)
        )

        em.set_author(name="Cum Machine", icon_url=ctx.author.avatar.url)
        em.timestamp = datetime.datetime.utcnow()
        await ctx.reply(embed=em)

#---------------------CLIENT---------------------#

def setup(client):
    client.add_cog(FunCmds(client))