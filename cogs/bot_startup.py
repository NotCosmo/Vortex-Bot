import nextcord as discord
import datetime, time
import os
import asyncio
from nextcord.ext import commands, tasks
from nextcord.utils import find
from nextcord import Interaction, SlashOption
from main import version
from pymongo import MongoClient

cluster = MongoClient("mongodb+srv://Cosmo:1H1uqPGjo5CjtHQe@eco.5afje.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
database = cluster["Discord"]
utils = database["Server_Utils"]


# from main import uptimeCounter, ts, tm, th, td

class RolesView(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="QOTD", style=discord.ButtonStyle.blurple, custom_id="roles_view:qotd"
    )
    async def qotd(self, button: discord.ui.Button, i: discord.Interaction):

        if find(lambda r: r.name == "QOTD", i.guild.roles) in i.user.roles:
            await i.user.remove_roles(find(lambda r: r.name == "QOTD", i.guild.roles))
            await i.response.send_message(":x: You have been removed from the QOTD role.", ephemeral=True)
        else:
            await i.user.add_roles(find(lambda r: r.name == "QOTD", i.guild.roles))
            await i.response.send_message(":white_check_mark: You have been added to the QOTD role.", ephemeral=True)

    @discord.ui.button(
        label="FOTD", style=discord.ButtonStyle.blurple, custom_id="roles_view:fotd"
    )
    async def fotd(self, button: discord.ui.Button, i: discord.Interaction):

        if find(lambda r: r.name == "FOTD", i.guild.roles) in i.user.roles:
            await i.user.remove_roles(find(lambda r: r.name == "FOTD", i.guild.roles))
            await i.response.send_message(":x: You have been removed from the FOTD role.", ephemeral=True)
        else:
            await i.user.add_roles(find(lambda r: r.name == "FOTD", i.guild.roles))
            await i.response.send_message(":white_check_mark: You have been added to the FOTD role.", ephemeral=True)

    @discord.ui.button(
        label="Economy", style=discord.ButtonStyle.blurple, custom_id="roles_view:eco"
    )
    async def eco(self, button: discord.ui.Button, i: discord.Interaction):

        if find(lambda r: r.name == "Economy", i.guild.roles) in i.user.roles:
            await i.user.remove_roles(find(lambda r: r.name == "Economy", i.guild.roles))
            await i.response.send_message(":x: You have been removed from the Economy role.", ephemeral=True)
        else:
            await i.user.add_roles(find(lambda r: r.name == "Economy", i.guild.roles))
            await i.response.send_message(":white_check_mark: You have been added to the Economy role.", ephemeral=True)

class StartUp(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):

        if not self.client.roles_persistent_view:
            self.client.add_view(RolesView())
            self.client.roles_persisent_view = True

        global startTime  # global variable to be used later in cog
        startTime = time.time()  # snapshot of time when listener sends on_ready

        global latency
        latency = round(self.client.latency * 1000)

        # await self.client.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name="Pornhub LIVE"))
        print('> Bot is now online')
        print(f'> {latency}ms')
        await self.client.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name="Pornhub LIVE | .gg/ZUTBBya"))
        utils.update_one({"tag": "Bot Info"}, {"$set": {"uptime_start": time.time()}})

    @commands.command(
        name="setuprules",
    )
    @commands.has_permissions(administrator=True)
    async def setuprules(self, ctx):
        welcome_embed = discord.Embed(
            title=":wave: Welcome!",
            description=f"Welcome to {ctx.guild.name}! We are a small community of people who enjoy talking to each other. One of our server highlights is the server's custom economy! (eco channel)! We hope you enjoy your stay.",
            colour=discord.Colour.blurple()
        )
        rules_embed = discord.Embed(
            title=":clipboard: Rules",
            description="While this is mostly a relaxed community, there are certain rules you must follow.\n\n",
            colour=discord.Colour.blurple()
        )
        rules_embed.description += "**Rule 1**: Do not spam the chat with large walls of text, advertisements or other forms of spam.\n\n"
        rules_embed.description += "**Rule 2**: Racism, homophobia and other forms of discrimination should be kept out of the server.\n\n"
        rules_embed.description += "**Rule 3**: There are no strict rules to NSFW, though any sorts of NSFW including lolis, children etc will be instantly removed.\n\n"
        rules_embed.description += "**Rule 4**: Gore is not allowed and we will yeet you the fuck out of here if we think what you send is fucked up.\n\n"
        rules_embed.description += "**Rule 5**: Harassment of any kind is not tolerated on this server.\n\n"
        rules_embed.description += "**Rule 6**: Follow Discord's [Community Guidelines](https://discord.com/guidelines) & [Terms of Service](https://discord.com/terms)\n\n"
        rules_embed.description += "**Extra Notes**:\n- The template of these rules was ~~stolen~~ borrowed from **Thank You Discord** and edited by the amazing staff.\n- Staff will have final say in most matters, if you believe they are abusing their permissions, please DM <@455971566199767040>."
        roles_embed = discord.Embed(
            title=":diamond_shape_with_a_dot_inside: Roles",
            description="Here are some of the roles you can get on this server.\n\n",
            colour=discord.Colour.blurple()
        )
        roles_embed.description += ":question: **QOTD**: Get pinged daily for a random Question of The Day.\n\n"
        roles_embed.description += ":thinking: **FOTD**: Get pinged daily for a random Fact of The Day.\n\n"
        roles_embed.description += ":moneybag: **Economy**: Gain access to the server's custom economy features..\n\n"
        await ctx.send(embed=welcome_embed)
        await ctx.send(embed=rules_embed)
        await ctx.send(embed=roles_embed, view=RolesView())

def setup(client):
    client.add_cog(StartUp(client))