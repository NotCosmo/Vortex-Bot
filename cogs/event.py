import discord
from discord.ext import commands
import asyncio
from discord.utils import *

class Event(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def eventstart(self, ctx):
        s = 3

        role = discord.utils.find(lambda r: r.name == '[✦] Mage', ctx.message.guild.roles)

        embed = discord.Embed(
            description = f'**{ctx.author.name}**: Where am I..?',
            colour = discord.Colour.from_rgb(0, 208, 255)
        )
        msg = await ctx.send(embed=embed)

        embed2 = discord.Embed(
            description = f'**{ctx.author.name}**: Where am I..?\n**???**: You are now in my realm, you mortal fiend.',
            colour = discord.Colour.from_rgb(255, 20, 20)
        )
        await asyncio.sleep(s)
        await msg.edit(embed=embed2)
        embed3 = discord.Embed(
            description = f'**{ctx.author.name}**: Where am I..?\n**???**: You are now in my realm, you mortal fiend.\n**{ctx.author.name}**: Who- what are you?',
            colour = discord.Colour.from_rgb(0, 208, 255)
        )
        await asyncio.sleep(s)
        await msg.edit(embed=embed3)
        embed4 = discord.Embed(
            description = f'**{ctx.author.name}**: Where am I..?\n**???**: You are now in my realm, you mortal fiend.\n**{ctx.author.name}**: Who- what are you?\n**???**: You have killed hundreds of my children yet YOU, a MORTAL does not know who I am?! I AM THE GOD OF DEATH!',
            colour = discord.Colour.from_rgb(255, 20, 20)
        )
        await asyncio.sleep(s)
        await msg.edit(embed=embed4)
        embed5 = discord.Embed(
            description = f'**{ctx.author.name}**: Where am I..?\n**???**: You are now in my realm, you mortal fiend.\n**{ctx.author.name}**: Who- what are you?\n**???**: You have killed hundreds of my children yet YOU, a MORTAL does not know who I am?! I AM THE GOD OF DEATH!\n**{ctx.author.name}**: Ah, I see. You must be **Thanatos**.',
            colour = discord.Colour.from_rgb(0, 208, 255)
        )
        await asyncio.sleep(s)
        await msg.edit(embed=embed5)
        embed6 = discord.Embed(
            description = f'**{ctx.author.name}**: Where am I..?\n**???**: You are now in my realm, you mortal fiend.\n**{ctx.author.name}**: Who- what are you?\n**???**: You have killed hundreds of my children yet YOU, a MORTAL does not know who I am?! I AM THE GOD OF DEATH!\n**{ctx.author.name}**: Ah, I see. You must be **Thanatos**.\n**Thanatos**: That is right. I am now going to dispose of you filthy scum.',
            colour = discord.Colour.from_rgb(255, 20, 20)
        )
        await asyncio.sleep(s)
        await msg.edit(embed=embed6)
        embed7 = discord.Embed(
            description = f'\n\nYou start feeling numb and dizzy, the world going blank around you, "This is the end." you think.\n\nAnd then you suddenly wake up.',
            colour = discord.Colour.from_rgb(0, 208, 255)
        )
        await asyncio.sleep(s)
        await msg.edit(embed=embed7)
        embed8 = discord.Embed(
            description = f'**{ctx.author.name}**: What. The. Fuck. Just. Happened.',
            colour = discord.Colour.from_rgb(0, 208, 255)
        )
        await asyncio.sleep(s)
        await msg.edit(embed=embed8)
        embed9 = discord.Embed(
            description = f'**{ctx.author.name}**: What. The. Fuck. Just. Happened.\n**???**: Be calm young one, there is no danger here.',
            colour = discord.Colour.from_rgb(204, 0, 204)
        )
        await asyncio.sleep(s)
        await msg.edit(embed=embed9)
        embed10 = discord.Embed(
            description = f'**{ctx.author.name}**: What. The. Fuck. Just. Happened.\n**???**: Be calm young one, there is no danger here.\n**{ctx.author.name}**: Who are you? What am I doing here? What is this place?',
            colour = discord.Colour.from_rgb(0, 208, 255)
        )
        await asyncio.sleep(s)
        await msg.edit(embed=embed10)
        embed11 = discord.Embed(
            description = f'**{ctx.author.name}**: What. The. Fuck. Just. Happened.\n**???**: Be calm young one, there is no danger here.\n**{ctx.author.name}**: Who are you? What am I doing here? What is this place?\n**???**: You are at my home, in the **Enchanted Fortress**. As for who I am, young one, I am sure you have heard many a tale of me and this place, I am **Merlin**.',
            colour = discord.Colour.from_rgb(204, 0, 204)
        )
        await asyncio.sleep(s)
        await msg.edit(embed=embed11)
        embed12 = discord.Embed(
            description = f'**{ctx.author.name}**: What. The. Fuck. Just. Happened.\n**???**: Be calm young one, there is no danger here.\n**{ctx.author.name}**: Who are you? What am I doing here? What is this place?\n**???**: You are at my home, in the **Enchanted Fortress**. As for who I am, young one, I am sure you have heard many a tale of me and this place, I am **Merlin**.\n**{ctx.author.name}**: So this place truly exists.. I never thought I would get to see this.',
            colour = discord.Colour.from_rgb(0, 208, 255)
        )
        await asyncio.sleep(s)
        await msg.edit(embed=embed12)
        embed13 = discord.Embed(
            description = f'**{ctx.author.name}**: What. The. Fuck. Just. Happened.\n**???**: Be calm young one, there is no danger here.\n**{ctx.author.name}**: Who are you? What am I doing here? What is this place?\n**???**: You are at my home, in the **Enchanted Fortress**. As for who I am, young one, I am sure you have heard many a tale of me and this place, I am **Merlin**.\n**{ctx.author.name}**: So this place truly exists.. I never thought I would get to see this.\n**Merlin:** Indeed it does young one, now I believe you have many questions, and I many answers.',
            colour = discord.Colour.from_rgb(204, 0, 204)
        )
        await asyncio.sleep(s)
        await msg.edit(embed=embed13)
        embed14 = discord.Embed(
            description = f'**{ctx.author.name}**: What. The. Fuck. Just. Happened.\n**???**: Be calm young one, there is no danger here.\n**{ctx.author.name}**: Who are you? What am I doing here? What is this place?\n**???**: You are at my home, in the **Enchanted Fortress**. As for who I am, young one, I am sure you have heard many a tale of me and this place, I am **Merlin**.\n**{ctx.author.name}**: So this place truly exists.. I never thought I would get to see this.\n**Merlin:** Indeed it does young one, now I believe you have many questions, and I many answers.',
            colour = discord.Colour.from_rgb(0, 208, 255)
        )
        await asyncio.sleep(s)
        await msg.edit(embed=embed14)
        embed15 = discord.Embed(
            description = f'**{ctx.author.name}**: What. The. Fuck. Just. Happened.\n**???**: Be calm young one, there is no danger here.\n**{ctx.author.name}**: Who are you? What am I doing here? What is this place?\n**???**: You are at my home, in the **Enchanted Fortress**. As for who I am, young one, I am sure you have heard many a tale of me and this place, I am **Merlin**.\n**{ctx.author.name}**: So this place truly exists.. I never thought I would get to see this.\n**Merlin:** Indeed it does young one, now I believe you have many questions, and I many answers.\n**{ctx.author.name}**: I like your funny words magic man.',
            colour = discord.Colour.from_rgb(0, 208, 255)
        )
        await asyncio.sleep(s)
        await msg.edit(embed=embed15)
        embed16 = discord.Embed(
            description = f'**{ctx.author.name}**: What. The. Fuck. Just. Happened.\n**???**: Be calm young one, there is no danger here.\n**{ctx.author.name}**: Who are you? What am I doing here? What is this place?\n**???**: You are at my home, in the **Enchanted Fortress**. As for who I am, young one, I am sure you have heard many a tale of me and this place, I am **Merlin**.\n**{ctx.author.name}**: So this place truly exists.. I never thought I would get to see this.\n**Merlin:** Indeed it does young one, now I believe you have many questions, and I many answers.\n**{ctx.author.name}**: I like your funny words magic man.\n\n **Congratulations, you have ascended to <@&875471775914405999>**',
            colour = discord.Colour.from_rgb(0, 208, 255)
        )
        await asyncio.sleep(s)
        await msg.edit(embed=embed16)
        embed17 = discord.Embed(
            description = f'**{ctx.author.name}**: What. The. Fuck. Just. Happened.\n**???**: Be calm young one, there is no danger here.\n**{ctx.author.name}**: Who are you? What am I doing here? What is this place?\n**???**: You are at my home, in the **Enchanted Fortress**. As for who I am, young one, I am sure you have heard many a tale of me and this place, I am **Merlin**.\n**{ctx.author.name}**: So this place truly exists.. I never thought I would get to see this.\n**Merlin:** Indeed it does young one, now I believe you have many questions, and I many answers.\n**{ctx.author.name}**: I like your funny words magic man.\n\n **Congratulations, you have ascended to <@&875471775914405999>**' +
            '\n\n__**Unlocked:**__',
            colour = discord.Colour.from_rgb(0, 208, 255)
        )
        await asyncio.sleep(1.5)
        await msg.edit(embed=embed17)
        embed17 = discord.Embed(
            description = f'**{ctx.author.name}**: What. The. Fuck. Just. Happened.\n**???**: Be calm young one, there is no danger here.\n**{ctx.author.name}**: Who are you? What am I doing here? What is this place?\n**???**: You are at my home, in the **Enchanted Fortress**. As for who I am, young one, I am sure you have heard many a tale of me and this place, I am **Merlin**.\n**{ctx.author.name}**: So this place truly exists.. I never thought I would get to see this.\n**Merlin:** Indeed it does young one, now I believe you have many questions, and I many answers.\n**{ctx.author.name}**: I like your funny words magic man.\n\n **Congratulations, you have ascended to <@&875471775914405999>**' +
            '\n\n__**Unlocked:**__\n- Magic Weapon Crafting',
            colour = discord.Colour.from_rgb(0, 208, 255)
        )
        await asyncio.sleep(1.5)
        await msg.edit(embed=embed17)
        embed18 = discord.Embed(
            description = f'**{ctx.author.name}**: What. The. Fuck. Just. Happened.\n**???**: Be calm young one, there is no danger here.\n**{ctx.author.name}**: Who are you? What am I doing here? What is this place?\n**???**: You are at my home, in the **Enchanted Fortress**. As for who I am, young one, I am sure you have heard many a tale of me and this place, I am **Merlin**.\n**{ctx.author.name}**: So this place truly exists.. I never thought I would get to see this.\n**Merlin:** Indeed it does young one, now I believe you have many questions, and I many answers.\n**{ctx.author.name}**: I like your funny words magic man.\n\n **Congratulations, you have ascended to <@&875471775914405999>**' +
            '\n\n__**Unlocked:**__\n- Magic Weapon Crafting\n- Key of the Sea',
            colour = discord.Colour.from_rgb(0, 208, 255)
        )
        await asyncio.sleep(1.5)
        await msg.edit(embed=embed18)
        embed19 = discord.Embed(
            description = f'**{ctx.author.name}**: What. The. Fuck. Just. Happened.\n**???**: Be calm young one, there is no danger here.\n**{ctx.author.name}**: Who are you? What am I doing here? What is this place?\n**???**: You are at my home, in the **Enchanted Fortress**. As for who I am, young one, I am sure you have heard many a tale of me and this place, I am **Merlin**.\n**{ctx.author.name}**: So this place truly exists.. I never thought I would get to see this.\n**Merlin:** Indeed it does young one, now I believe you have many questions, and I many answers.\n**{ctx.author.name}**: I like your funny words magic man.\n\n **Congratulations, you have ascended to <@&875471775914405999>**' +
            '\n\n__**Unlocked:**__\n- Magic Weapon Crafting\n- Key of the Sea\n- Ranks XI - XX',
            colour = discord.Colour.from_rgb(0, 208, 255)
        )
        await asyncio.sleep(1.5)
        await msg.edit(embed=embed19)
        embed20 = discord.Embed(
            description = f'**{ctx.author.name}**: What. The. Fuck. Just. Happened.\n**???**: Be calm young one, there is no danger here.\n**{ctx.author.name}**: Who are you? What am I doing here? What is this place?\n**???**: You are at my home, in the **Enchanted Fortress**. As for who I am, young one, I am sure you have heard many a tale of me and this place, I am **Merlin**.\n**{ctx.author.name}**: So this place truly exists.. I never thought I would get to see this.\n**Merlin:** Indeed it does young one, now I believe you have many questions, and I many answers.\n**{ctx.author.name}**: I like your funny words magic man.\n\n **Congratulations, you have ascended to <@&875471775914405999>**' +
            '\n\n__**Unlocked:**__\n- Magic Weapon Crafting\n- Key of the Sea\n- Ranks XI - XX\n- The **Enchanted Fortress**.',
            colour = discord.Colour.from_rgb(0, 208, 255)
        )
        await asyncio.sleep(1.5)
        await ctx.author.add_roles(role)
        await msg.edit(embed=embed20)



def setup(client):
    client.add_cog(Event(client))