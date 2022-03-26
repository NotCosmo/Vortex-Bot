from keep_alive import keep_alive
import nextcord as discord
import datetime
import os
from nextcord.ext import commands
import aiohttp
import jishaku

GUILD_ID = 581139467381768192

version = "v1.51"
latest_update = "> New Admin Commands\n> Bi & Les rate commands."
timeNow = datetime.datetime.utcnow()

# vortex
# Format = <:stonks:713292086954295296>

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

keep_alive()
token = os.environ['token']

if __name__ == "__main__":
    async def startup():
        client.session = aiohttp.ClientSession()

    client.loop.create_task(startup())
    client.run(token)