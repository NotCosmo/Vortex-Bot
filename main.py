from keep_alive import keep_alive
import nextcord as discord
import datetime
import os
from nextcord.ext import commands
import aiohttp
import jishaku

from pymongo import MongoClient
cluster = MongoClient("mongodb+srv://Cosmo:1H1uqPGjo5CjtHQe@eco.5afje.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
database = cluster["Discord"]
db = database["Server_Utils"]

version = "v1.51"
latest_update = "> New Admin Commands\n> Bi & Les rate commands."
timeNow = datetime.datetime.utcnow()

# vortex
# Format = <:stonks:713292086954295296>

client = commands.Bot(command_prefix=['!', '>'], intents=discord.Intents.all())
client.sniped = None
client.roles_persistent_view = False
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
async def rpgleaks(ctx):

    await ctx.author.add_roles(discord.utils.get(ctx.guild.roles, name="RPG Leaks"))
    await ctx.reply("Done")
    
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

client.load_extension('jishaku')
os.environ["JISHAKU_EMBEDDED_JSK_COLOUR"] = "0x00d0ff"
os.environ.setdefault("JISHAKU_NO_UNDERSCORE", "1")
os.environ.setdefault("JISHAKU_HIDE", "0")

data = db.find_one({"tag":"token"})
token = data['bot_token']

keep_alive()
client.run(token)