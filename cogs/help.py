import nextcord as discord
from nextcord.ext import commands
from nextcord.errors import Forbidden

bot_colour = discord.Colour.from_rgb(0, 208, 255)

async def get_emoji(cog):

    emoji = ''
    
    if cog == "Admin":
        emoji = ':shield:'
    if cog == "General":
        emoji = ":information_source:"
    if cog == "Images":
        emoji = ":camera:"
    if cog == "Economy":
        emoji = ":moneybag:"
        
    return emoji

async def send_embed(ctx, embed):
    """
    Function that handles the sending of embeds
    -> Takes context and embed to send
    - tries to send embed in channel
    - tries to send normal message when that fails
    - tries to send embed private with information abot missing permissions
    If this all fails: https://youtu.be/dQw4w9WgXcQ
    """
    try:
        await ctx.send(embed=embed)
    except Forbidden:
        try:
            await ctx.send("Hey, seems like I can't send embeds. Please check my permissions :)")
        except Forbidden:
            await ctx.author.send(
                f"Hey, seems like I can't send any message in {ctx.channel.name} on {ctx.guild.name}\n"
                f"May you inform the server team about this issue? :slight_smile: ", embed=embed)


class Help(commands.Cog):
    """
    Sends this help message
    """

    def __init__(self, client):
        self.client = client

    @commands.command()
    # @commands.bot_has_permissions(add_reactions=True,embed_links=True)
    async def help(self, ctx, *input):
        """Shows all modules of that bot"""

        prefix = '!' 
        version =  1.2
        emoji = ''

        # checks if cog parameter was given
        # if not: sending all modules and commands not associated with a cog
        if not input:

            # starting to build embed
            emb = discord.Embed(title='Vortex Help', colour=bot_colour,description=f'Use `{prefix}help <module>` to gain more information about that module\n\n')
            emb.description += f":information_source: **General**\n- !help General.\n\n"
            emb.description += f":camera: **Images**\n- !help Images.\n\n"
            emb.description += f":moneybag: **Economy**\n- !help Economy.\n\n"
            emb.description += f":shield: **Staff**\n- !help Staff."

            return await send_embed(ctx, emb)
                    
        elif len(input) == 1:

            # iterating trough cogs
            for cog in self.client.cogs:
                # check if cog is the matching one
                if cog.lower() == input[0].lower():

                    # making title - getting description from doc-string below class
                    emoji = await get_emoji(cog)
                    emb = discord.Embed(title=f'{emoji} {cog} Module', description=f"{self.client.cogs[cog].description}\n\n__**Commands**__\n",colour=bot_colour)

                    # getting commands from cog
                    for command in self.client.get_cog(cog).get_commands():
                        # if cog is not hidden
                        if not command.hidden:
                            emb.description += f"{command.name}, "
                    # found cog - breaking loop
                    break

            # if input not found
            # yes, for-loops have an else statement, it's called when no 'break' was issued
            else:
                emb = discord.Embed(title="What's that?!",description=f"I've never heard from a module called `{input[0]}` before :scream:",color=discord.Color.orange())

        # too many cogs requested - only one at a time allowed
        elif len(input) > 1:
            emb = discord.Embed(title="That's too much.",
            description="Please request only one module at once :sweat_smile:",
            color=discord.Color.orange())

        else:
            emb = discord.Embed(title="It's a magical place.",
            description="I don't know how you got here. But I didn't see this coming at all.\n"
                "Would you please be so kind to report that issue to me on github?\n"
                "https://github.com/nonchris/discord-fury/issues\n"
                "Thank you! ~Chris",
            color=discord.Color.red())

        # sending reply embed using our own function defined above
        await send_embed(ctx, emb)

def setup(client):
    client.add_cog(Help(client))