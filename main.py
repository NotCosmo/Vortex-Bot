import keep_alive
import discord
import random
import datetime
import os
from discord.ext import commands
from discordTogether import DiscordTogether
import aiohttp

version = "v1.41"
latest_update = "> AFK Command\n> Hack Command."
timeNow = datetime.datetime.utcnow()

# vortexRGB = (0, 155, 180)
# Emoji Format = <: name :     id           >
# Emoji Format = <:stonks:713292086954295296>

client = commands.Bot(command_prefix=["!", ">"], case_sensitive=True, intents=discord.Intents.all())
togetherControl = DiscordTogether(client)
client.remove_command('help')

@client.event
async def on_member_join(user):

    channel = client.get_channel(735765424108601386)
    embed = discord.Embed(
        description = f'Welcome to the server {user.mention}! We hope you enjoy your stay.',
        colour = discord.Colour.from_rgb(0, 208, 255)
    )

    embed.set_author(name="👋 New User", icon_url=user.avatar_url)
    embed.timestamp = datetime.datetime.utcnow()
    await channel.send(embed=embed)

    return 0;

@client.command()
@commands.is_owner()
async def reload(ctx, extension):
    client.reload_extension(f"cogs.{extension}")
    embed = discord.Embed(title='Reload', description=f'{extension} successfully reloaded', colour = discord.Colour.from_rgb(255, 75, 75))
    await ctx.send(embed=embed)

@client.command()
@commands.is_owner()
async def quit(ctx):
    await ctx.send("Shutting down the bot")
    return await client.close() # this just shuts down the bot.

##
@client.command()
async def load(ctx, extension):
  client.load_extension(f'cogs.{extension}')

@client.command()
async def unload(ctx, extension):
  client.unload_extension(f'cogs.{extension}')

for filename in os.listdir('./cogs'):
  if filename.endswith('.py'):
    client.load_extension(f'cogs.{filename[:-3]}')

@client.command()
@commands.has_any_role("Event Perms", "The Boys", "Admin")
async def game(ctx, vcgame):

    if vcgame in ["youtube", "fishing", "poker", "chess", "betrayal"]:
        link = await togetherControl.create_link(ctx.author.voice.channel.id, f'{vcgame}')
        await ctx.send(f"Click the blue link!\n{link}")

    else:
        embed = discord.Embed(
            description = "**Invalid Game!** Please choose between:\n\n- youtube, fishing, poker, chess, betrayal",
            colour = discord.Colour.from_rgb(0, 208, 255)
        )
        embed.timestamp = timeNow
        embed.set_author(name="Error", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

@game.error
async def game_error(ctx: commands.Context, error: commands.CommandError):

    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(
            description = "**Invalid Game!** Please choose between:\n\n- youtube, fishing, poker, chess, betrayal",
            colour = discord.Colour.from_rgb(0, 208, 255)
        )
        embed.timestamp = timeNow
        embed.set_author(name="Error", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

@client.command()
@commands.is_owner()
async def todo(ctx):

    await ctx.send("Mute + Unmute\n\nAdmin Cmds help page")

@client.command()
async def meme(ctx):
    async with aiohttp.ClientSession() as cs:
        async with cs.get("https://www.reddit.com/r/memes.json") as r:
            memes = await r.json()
            embed = discord.Embed(
                colour = discord.Colour.random()
            )
            embed.set_image(url=memes["data"]["children"][random.randint(0, 25)]["data"]["url"])
            embed.set_footer(text=f'Image from r/memes! Requested by {ctx.author}')
            await ctx.send(embed=embed)

@client.command()
async def search(ctx, subreddit):

    nsfw = ["porn", "r34", "nsfw", "nsfw2", "sex", "hentai", "hentai_gif", "tentai", "HENTAI_GIFS", "thighdeology", "waifusgonewild", "lanarhoades", "boobs", "tits", "ass", "pussy", "vagina", "AstolfoRidesYou", "flash"]
    blocked_users = []

    if subreddit in nsfw:

        embed = discord.Embed(
            description = 'No',
            colour = discord.Colour.from_rgb(255, 0, 0)
        )
        await ctx.send(embed=embed)

    elif ctx.author.id in blocked_users:

        embed = discord.Embed(
            description = 'You are blocked from this command!',
            colour = discord.Colour.from_rgb(255, 0, 0)
        )
        await ctx.send(embed=embed)

    else:
        async with aiohttp.ClientSession() as cs:
            try:
                async with cs.get(f"https://www.reddit.com/r/{subreddit}.json") as r:
                    image = await r.json()
                    embed = discord.Embed(
                        colour = discord.Colour.random()
                    )
                    embed.set_image(url=image["data"]["children"][random.randint(0, 25)]["data"]["url"])
                    embed.set_footer(text=f'Image from r/{subreddit}! Requested by {ctx.author}')
                    await ctx.send(embed=embed)
            except:
                embed = discord.Embed(
                    title = 'Error Occured',
                    description = "That subreddit is invalid or I could not find an image, please try a different subreddit.",
                    colour = discord.Colour.from_rgb(255, 95, 95)
                )
                await ctx.send(embed=embed)

@client.command()
async def info(ctx, reqINFO=None):

    if reqINFO is None:

        embed = discord.Embed(
            title = 'What are you searching for?',
            description = 'Try searching for a keyowrd, such as `!info Bosses`',
            colour = discord.Colour.from_rgb(0, 208, 255)
        )
        await ctx.send(embed=embed)

    elif reqINFO == 'Bosses':

        embed = discord.Embed(
            title = 'Bosses - Economy',
            description = 'You can fight bosses by obtaining a key from the shop and using the `!boss` command, though you need to meet certain requirements that will be showed upon purchasing the boss key. \n \nBosses can give great loot, such as items with % crystal boosts or luck boosts for other bosses!\n \nEvery once in a while, there will be a special boss that will only be out for a short period of time, these bosses will drop **Unqiue** items with even better items.',
            colour = discord.Colour.from_rgb(0, 208, 255)
        )
        await ctx.send(embed=embed)

    elif reqINFO == 'Trading':
        embed = discord.Embed(
            title = 'Trading - Economy',
            description = 'If you have an item in your inventory, you can use the `/sellitem` command to sell it to another user for crystals. This can be done back and forth where you are either trading items for items or items for money. \n \nWhatever happens is **your** responsibility, staff members will not interfere with trades unless there is some sort of exploit going around.',
            colour = discord.Colour.from_rgb(0, 208, 255)
        )
        await ctx.send(embed=embed)

@commands.has_permissions(administrator=True)
async def mail(ctx, user: discord.Member=None, *, message=None):
    
    if user is None:
        embed = discord.Embed(
            description = 'Who are you trying to send the message to? `!mail <user> <message>`',
            colour = discord.Colour.from_rgb(255, 95, 95)
        )
        embed.set_author(name='Confusion?', icon_url=ctx.author.icon_url)
        await ctx.send(embed=embed)

    elif user is not None:

        if message is None:
            embed = discord.Embed(
                description = 'What are you trying to send? `!mail <user> <message>`',
                colour = discord.Colour.from_rgb(255, 95, 95)
            )
            embed.set_author(name='Confusion', icon_url=ctx.author.icon_url)
            await ctx.send(embed=embed)
        elif message is not None:
            embed = discord.Embed(
                description = f'{message}',
                colour = discord.Colour.from_rgb(0, 155, 180)
            )
            embed.set_author(name=f'{ctx.author.mention} sent you a message!', icon_url=ctx.author.icon_url)
            await user.send(embed=embed)

client.load_extension("jishaku")
keep_alive.keep_alive()
token = os.environ['token']

if __name__ == "__main__":
    client.run(token)