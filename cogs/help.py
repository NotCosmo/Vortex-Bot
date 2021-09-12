import discord
from discord.ext import commands
from main import version, latest_update, timeNow

#version = "v0.4"
#latest_update = "> Test"

class HelpCommand(commands.MinimalHelpCommand):
    async def send_pages(self):

        destination = self.get_destination()
        for page in self.paginator.pages:
            embed = discord.Embed(
                title = "Help Menu",
                description = f"- Prefixes for the bot are `!` and `>`.\n- Arguments shown with `<>` are **required**.\n- Arguments shown with `()` are **optional** and do not need to be passed in.\n\n**━━━━━ Modules ━━━━━━**\n\n> **💥 Rate**\n> - !help rate\n> \n> **🥳 Fun**\n> - !help fun\n> \n> **📷 Images**\n> - !help images\n> \n> ⭐ **Anime**\n> - !help animecmds\n> \n> **🎵 Music**\n> - !help music\n> \n> **️ ⚙️ Other**\n> - !help other\n> \n> 🔒 **Admin**\n> - !help admin\n\n**━━━ Latest Update - {version} ━━━**\n\n{latest_update}\n\n**━━━━━━━━━━━━━━━**\n\n> Thanks <@656073353215344650> for helping with the Music module.",
                colour = discord.Colour.random()
            )
            embed.timestamp = timeNow
            #embed.set_thumbnail(url=guild.icon_url)
            await destination.send(embed=embed)

    async def send_command_help(self, command):

        desc = command.help
        if command.name == "rate":
            embedName = "💥 Rate Module"
            embedColour = discord.Colour.from_rgb(47, 49, 54)

        elif command.name == "fun":
            embedName = "🥳 Fun Module"
            embedColour = discord.Colour.from_rgb(47, 49, 54)

        elif command.name == "other":
            embedName = "⚙️ Other Module"
            embedColour = discord.Colour.from_rgb(47, 49, 54)
        
        elif command.name == "images":
            embedName = "📷 Images Module"
            embedColour = discord.Colour.from_rgb(47, 49, 54)

        elif command.name == "admin":
            embedName = "🔒 Admin Module"
            embedColour = discord.Colour.from_rgb(47, 49, 54)

        elif command.name == "animecmds":
            embedName = f"⭐ Anime Module"
            embedColour = discord.Colour.from_rgb(47, 49, 54)

        elif command.name == "music":
            embedName = "🎵 Music Module"
            embedColour = discord.Colour.from_rgb(47, 49, 54)

        else:
            embedName = self.get_command_signature(command)
            embedColour = discord.Colour.from_rgb(0, 208, 255)

        #else:
            #embedName = self.get_command_signature(command)

        embed = discord.Embed(colour=embedColour)
        embed.add_field(name=embedName, value=desc)
        #alias = command.aliases
        #if alias:
            #embed.add_field(name="Aliases", value=", ".join(alias), inline=False)

        channel = self.get_destination()
        embed.timestamp = timeNow
        await channel.send(embed=embed)

    async def send_error_message(self, error):
        embed = discord.Embed(title="Error", description=error)
        channel = self.get_destination()
        await channel.send(embed=embed)


class HelpCog(commands.Cog):

    def __init__(self, client):
       self.client = client
        
       # Focus here
       # Setting the cog for the help
       help_command = HelpCommand()
       help_command.cog = self # Instance of YourCog class
       client.help_command = help_command

    @commands.command(help="> `drip`: Rates your drip.\n> `gay`: Shows how gay you are.\n> `halal`: Shows how halal you are.\n> `pedo`: Rates how much of a pedo you are.\n> `pog`: Rates how pog you are.\n> `pp`: Shows how big your penis is.\n> `retard`: Shows how retarded you are.\n> `simp`: Shows how much of a simp you are.\n> `sus`: Shows how sus you are.\n> `horny`: Shows how horny you are.\n> `weeb`: Rates how much of a weeb you are.\n> `poop`: Rates your poop size.")
    async def rate(self, ctx):
        pass

    @commands.command(help = "> `8ball`: Ask the magic 8ball a question.\n> `meme`: Get a random meme!\n> `coinflip`: Flip a coin!\n> `luck`: Find out the luck of something happening!\n> `randomnumber`: Pick a random number from `<min>` to `<max>`.\n> `rps:` Play Rock Paper Scissors!\n> `say`: Make the bot say something.\n> `tyod`: Use Thousand Years of Death on someone!\n> `slap`: Slap someone!\n> `cookie`: Give someone a cookie!\n> `shoot`: Shoot someone!\n> `hack`: Hack somebody!")
    async def fun(self, ctx):
        pass

    @commands.command(help = "> `av`: Shows users avatar.\n> `poll`: Create a poll.\n> `userinfo`: Shows info on a user.\n> `stats`: Shows current bot stats.\n> `search`: Search for an image in a subreddit.\n> `bug`: Report a bot/server bug.\n> `updates`: Toggle Vortex Update Pings.\n> `economy`: Toggle Economy Update Pings.\n> `afk`: Set your AFK status.")
    async def other(self, ctx):
        pass

    @commands.command(help = "> `wanted`: Shows user in a wanted poster.\n> `rip`: Shows user in a RIP gravestone.\n> `ship`: Ship yourself with another member!")
    async def images(self, ctx):
        pass

    @commands.command(help = "> `aninews`: Get the latest news on Anime.\n> `char`: Search for an anime character.\n> `anime`: Search for info about an anime.")
    async def animecmds(self, ctx):
        pass

    @commands.command(help = "> `join`: Joins a voice channel.\n> `leave`: Leaves a voice channel.\n> `play`: Play a song.\n> `pause`: Pauses a song.\n> `resume`: Resumes a song.\n> `stop`: Stop playing a song.\n> `resume`: Resume playing a command.\n> `loop`: Toggle loop for a song.\n> `queue`: Show the current song queue.\n> `np`: Show the current song playing.\n> `skip`: Skips the current song.\n> `volume`: Change the volume of a song.\n> `remove`: Remove a song from the queue.")
    async def music(self, ctx):
        pass

    @commands.command(help = "> `ban`: Bans a member.\n> `kick`: Kicks a member.\n> `purge`: Clears specified amount of messages.\n> `role`: Gives user specified role.\n> `getrewards`: Get rewards for a boss in case it froze.")
    async def admin(self, ctx):
        pass


def setup(client):
    client.add_cog(HelpCog(client))