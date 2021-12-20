from keep_alive import keep_alive
import asyncio
import time
import nextcord as discord
import random
import datetime
import os
from nextcord.ext import commands, tasks
from nextcord.ext.commands import BucketType
import aiohttp

version = "v1.51"
latest_update = "> New Admin Commands\n> Bi & Les rate commands."
timeNow = datetime.datetime.utcnow()

# vortexRGB = (0, 155, 180)
# Emoji Format = <: name :     id           >
# Emoji Format = <:stonks:713292086954295296>

client = commands.Bot(command_prefix=['!', '>'], case_sensitive=False, intents=discord.Intents.all())
client.sniped = None
client.remove_command('help')

@client.event
async def on_message_delete(message: discord.Message):
    client.sniped = message
    
@client.command()
async def snipe(ctx: commands.Context):

    em = discord.Embed(
        description = f"{client.sniped.content}",
        colour = discord.Colour.from_rgb(0, 208, 255)
    )

    em.set_author(name=f"{client.sniped.author.name}", icon_url=client.sniped.author.display_avatar)
    em.timestamp = datetime.datetime.utcnow()
    await ctx.reply(embed=em)

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
@commands.cooldown(1, 3600, BucketType.user)
async def collecttest(ctx):

    await ctx.send("Collected!")

@client.command()
async def meme(ctx):
    async with aiohttp.ClientSession() as cs:
        async with cs.get("https://some-random-api.ml/meme") as r:
            memes = await r.json()
            embed = discord.Embed(
                title = memes["caption"],
                colour = discord.Colour.random()
            )
            embed.set_image(url=memes["image"])
            embed.set_footer(text=f'Random Meme Requested by {ctx.author}')
            await ctx.send(embed=embed)

#client.load_extension('jishaku')
keep_alive()
token = os.environ['token']

if __name__ == "__main__":
    client.run(token)
    async def startup():
        client.session = aiohttp.ClientSession()

    client.loop.create_task(startup())
    client.run(token)