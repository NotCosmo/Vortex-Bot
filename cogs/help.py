import nextcord as discord
from nextcord.ext import commands
from datetime import datetime

bot_colour = discord.Colour.from_rgb(0, 208, 255)


def get_emoji(cog):
    emoji = ''

    if cog == "Fun":
        emoji = ':tada:'
    if cog == "General":
        emoji = ":information_source:"
    if cog == "Economy":
        emoji = ":moneybag:"
    if cog == "Staff":
        emoji = ":shield:"

    return emoji



class Help(commands.Cog):
    """
    Sends this help message
    """

    def __init__(self, client):
        self.client = client

    @commands.command(name="help", aliases=["h"])
    async def help(self, ctx, *, input=None):

        count = 0
        total = 0
        embed = discord.Embed(title="Vortex Help", description="", colour=bot_colour)
        embed.set_thumbnail(url=self.client.user.avatar.url)
        #embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.display_avatar)

        for cog in self.client.cogs:
            _cog =  self.client.get_cog(cog)
            if len(_cog.get_commands()) > 0:
                for c in _cog.get_commands():
                    total += 1

        main_cogs = ["General", "Fun", "Economy"]

        if ctx.channel.id in [814787632776609812, 842812145791402004]:
            main_cogs = ["General", "Fun", "Economy", "Staff"]
        
        for cog in main_cogs:
            cmds = ""
            for command in self.client.get_cog(cog).get_commands():
                if not command.hidden:
                    #cmds += f"{command.name}, "
                    cmds += f"`{command.name}` "
                    count += 1

            embed.add_field(name=f"{get_emoji(cog)} {cog}", value=f"{cmds}\n<:transparent:911319446918955089>", inline=False)
            embed.description = f"**Prefix**: `!` ┃ `>`\n\nHey there! I'm a general purpose bot developed by <@455971566199767040>\nShowing a total of **{count}** out of **{total}** commands.\n<:transparent:911319446918955089>"
            embed.timestamp = datetime.utcnow()
        return await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Help(client))