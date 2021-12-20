# Main Imports

import nextcord as discord
import random
import asyncio
import time

# Other

from nextcord.ext import commands
from nextcord.ext.commands import BucketType
from nextcord.utils import find
from datetime import datetime
from pymongo import MongoClient

# ------------------------------- #
''' Cluster '''
# ------------------------------- #

cluster = MongoClient("mongodb+srv://Cosmo:1H1uqPGjo5CjtHQe@eco.5afje.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
database = cluster["Discord"]
eco = database["Economy"]

# ------------------------------- #
''' Setup '''
# ------------------------------- #

class NPCS(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.group(invoke_without_command=True)
    async def quest(self, ctx):

        em = discord.Embed(
            colour = discord.Colour.from_rgb(0, 208, 255)
        )

        em.add_field(name="Merlin", value="- The Main Npc for anything related to bosses!", inline=False)
        em.add_field(name="Amethyst", value="- The Main Npc for anything related to amulets and magic items!", inline=False)

        await ctx.send(embed=em)

    @quest.command(aliases = ["Merlin"])
    async def merlin(self, ctx):

        Economy = eco.find_one({"memberid":ctx.author.id})
        quest = Economy["currentQuest"]

        # Quest One
        if quest == "Merlin1":

            em = discord.Embed(
                title = f"✨ Enchanted Tower",
                description = '',
                colour = discord.Colour.from_rgb(0, 208, 255)
            )
            em.timestamp = datetime.utcnow()
            cd = 5

            em.description += ":crystal_ball: **Merlin**: Hello young one. It appears fate has brought us together once again."
            msg = await ctx.send(embed=em)
            await msg.edit(embed=em)

            await asyncio.sleep(cd)
            em.description += f"\n\n**{ctx.author.name}**: Fate is quite mischevious, I learned that from a wise man."
            await msg.edit(embed=em)

            await asyncio.sleep(cd)
            em.description += f"\n\n:crystal_ball: **Merlin**: It quite is.. *cough* I am in need of your help {ctx.author.name}.. my apprentice, who I thought to be long dead, has risen."
            await msg.edit(embed=em)

            await asyncio.sleep(cd)
            em.description += f"\n\n**{ctx.author.name}**: Normally, I would assume that's a good thing, though seeing as you called me here, I would say it's bad news."
            await msg.edit(embed=em)
            
            await asyncio.sleep(cd)
            em.description += f"\n\n:crystal_ball: **Merlin**: It was years ago, when I was still a young man learning about the wonders of magic. In one of my many travels, I came across a boy, seemingly abandoned in the middle of the forest."
            await msg.edit(embed=em)

            await asyncio.sleep(cd)
            em.description += f" He was young, not even 11 at the time, and quite understandably scared. He looked simple enough, probably from a village in the area, with raven-black hair and a peasant's attire."
            await msg.edit(embed=em)

            await asyncio.sleep(cd)
            await msg.edit(embed=em)
            em.description += f" I'd assumed he was lost, not uncommon for children to wander where they should not, but when he looked up at me and I met those emerald-green eyes of his, I knew this was not a simple boy."

            await asyncio.sleep(cd)
            em.description += f"**{ctx.author.name}**: Sound like a nice boy, what happened after?"
            await msg.edit(embed=em)

            await asyncio.sleep(cd)
            em.description += f"\n\n:crystal_ball: **Merlin**: It is true what they say, the eyes are the windows to the soul, and magic is something that is entwined very closely with your soul. This boy, his magic, was powerful. Perhaps even on-par with my own. Such potential was rare to come by. I had only come across it once before...but I digress."
            await msg.edit(embed=em)

            await asyncio.sleep(cd)
            em.description += f"\n\n**{ctx.author.name}**: Hold up a second. On-par with your own? Merlin, you didn't tell me it was this serious."
            await msg.edit(embed=em)

            await asyncio.sleep(cd)
            em.description += f"\n\n:crystal_ball: **Merlin**: Certainly. I will not bore you with the details of the boy's life, but our conversation came to a close with him accepting an Apprentinceship under me.."
            await msg.edit(embed=em)

            await asyncio.sleep(cd)
            em.description += f" Wait...I sense a dark presence near us. It is one I recognise...I believe one of **Raven**'s minions are near us. I can not fight them alone, I am too weak in my old age. Please, {ctx.author.name} take this staff and help me defeat them."
            await msg.edit(embed=em)

            await asyncio.sleep(cd)
            em.description += f"\n\n**{ctx.author.name}**: It would be an honour to fight with you, Merlin."
            await msg.edit(embed=em)

            await asyncio.sleep(cd)
            em.description += f"\n\n**QUEST OBJECTIVE**: Defeat one of **Raven**'s minions.\n-> `0/1` minions defeated.\n-> Use `>boss minion` to start."
            await msg.edit(embed=em)

        # Quest Two
        elif quest == "Merlin2":

            em = discord.Embed(
                title = f"✨ Enchanted Tower",
                description = '',
                colour = discord.Colour.from_rgb(0, 208, 255)
            )
            em.timestamp = datetime.utcnow()
            cd = 5

            em.description += f":crystal_ball: **Merlin**: Ah, the wonders of youth...how I wish to be able to wield my magic as such again...alas my days of prosperity are gone. What is it you have there {ctx.author.name}?"
            msg = await ctx.send(embed=em)
            await msg.edit(embed=em)

            await asyncio.sleep(cd)
            em.description += f"\n\n**{ctx.author.name}**: It's the minions weapon, seems to be a sword of some kind? It's seeped in this disgusting magic though..."
            await msg.edit(embed=em)

            await asyncio.sleep(cd)
            em.description += f"\n\n:crystal_ball: **Merlin**: Ah...chaos magic. A truly foul and wretched thing it is. However...this weapon may be useful to you on your journey...perhaps I should introduce you to ***Amethyst***, a truly talented Spellcrafter. Go young one, speak to Amethyst, she will know what to do with the weapon. "
            await msg.edit(embed=em)

            await asyncio.sleep(cd)
            em.description += f"\n\n**QUEST OBJECTIVE**: Speak to Amethyst.\n-> Use `>quest Amethyst` to continue."
            await msg.edit(embed=em)

            eco.update_one({"memberid":ctx.author.id},{"$set":{"currentQuest": "Amethyst1"}})

        # Quest 3
        elif quest == "Merlin3":

            em = discord.Embed(
                title = f"✨ Enchanted Tower",
                description = '',
                colour = discord.Colour.from_rgb(0, 208, 255)
            )
            em.timestamp = datetime.utcnow()
            cd = 5

            msg = await ctx.send(embed=em)

            em.description += f"\n\n:crystal_ball: **Merlin**: Young one! I'm so glad to see you."
            await msg.edit(embed=em)

            await asyncio.sleep(cd)
            em.description += f"\n\n**{ctx.author.name}**: What's going on? Amethyst sensed your magic in distress- what is this dark presence?"
            await msg.edit(embed=em)

            await asyncio.sleep(cd)
            em.description += f"\n\n:crystal_ball: **Merlin**: I see that staff of yours is allowing you to see things more clearly. It's Raven's presence. He's here, watching us from the shadows."
            await msg.edit(embed=em)

            await asyncio.sleep(cd)
            em.description += f"\n\n**{ctx.author.name}**: Explain that later. For now, what do you mean it's **Raven**'s presence? Do we need to fight him? I don't think we can take him on at this stage."
            await msg.edit(embed=em)

            em.description += f"\n\n:crystal_ball: **Merlin**: Thankfully not. It appears Raven has sent one of his upper minions, or a Follower to hunt us down."
            await msg.edit(embed=em)

            await asyncio.sleep(cd)
            em.description += f"\n\n**{ctx.author.name}**: Well that sounds like a much better challenge for me. Time to test out this new staff."
            await msg.edit(embed=em)

            await asyncio.sleep(cd)
            em.description += f"\n\n**QUEST OBJECTIVE**: Defeat Raven's Follower 10 times.\n-> Use `>boss Follower` to continue."
            await msg.edit(embed=em)

        # Quest 3
        elif quest == "Merlin4":

            em = discord.Embed(
                title = f"✨ Enchanted Tower",
                description = '',
                colour = discord.Colour.from_rgb(0, 208, 255)
            )
            em.timestamp = datetime.utcnow()
            cd = 5

            msg = await ctx.send(embed=em)

            em.description += f"\n\n:crystal_ball: **Merlin**: Thank you for taking care of that for me young one."
            await msg.edit(embed=em)

            await asyncio.sleep(cd)
            em.description += f"\n\n**{ctx.author.name}**: No need. This new staff is quite handy if I do say so myself. Though I did get some odd loot from that follower, do you think you could examine it?"
            await msg.edit(embed=em)

            await asyncio.sleep(cd)
            em.description += f"\n\n:crystal_ball: **Merlin**: This is definitely Raven's Magic. I can feel the chaos magic radiating from it. Amethyst should be able to help you, as you might have already figured out, she's good with stuff like this, and I heard she's looking for you actually."
            await msg.edit(embed=em)

            await asyncio.sleep(cd)
            em.description += f"\n\n**{ctx.author.name}**: Lovely coincidence, I'll go see what she needs, you should take a rest. Thanks Merlin."
            await msg.edit(embed=em)

            await asyncio.sleep(cd)
            em.description += f"\n\n**QUEST OBJECTIVE**: Go talk to Amethyst.\n-> Use `>quest Amethyst` to continue."
            await msg.edit(embed=em)
            eco.update_one({"memberid":ctx.author.id},{"$set":{"currentQuest":"Amethyst3"}})

    @quest.command(aliases = ["Amethyst"])
    async def amethyst(self, ctx):

        Economy = eco.find_one({"memberid":ctx.author.id})
        quest = Economy["currentQuest"]

        feather = find(lambda r: r.name == "🕊️ Gryphon's Feather", ctx.message.guild.roles)
        claw = find(lambda r: r.name == "🐉 Gryphon's Claw", ctx.message.guild.roles)
        heart = find(lambda r: r.name == "❤️ Gryphon's Heart", ctx.message.guild.roles)

        if quest == "Amethyst1":

            em = discord.Embed(
                title = f"⚗️ Spellcrafter Hut",
                description = '',
                colour = discord.Colour.from_rgb(0, 208, 255)
            )
            em.timestamp = datetime.utcnow()
            cd = 5

            em.description += f":crossed_swords: **Amethyst**: So, you're {ctx.author.name}? Merlin's new protege?"
            msg = await ctx.send(embed=em)
            await msg.edit(embed=em)

            await asyncio.sleep(cd)
            em.description += f"\n\n**{ctx.author.name}**: Yeah...he told me to bring you this? Said you'd know what to do with it..."
            await msg.edit(embed=em)

            await asyncio.sleep(cd)
            em.description += f"\n\n:crossed_swords: **Amethyst**: Oh, fancy staff dude. Where'd you get it?"
            await msg.edit(embed=em)

            await asyncio.sleep(cd)
            em.description += f"\n\n**{ctx.author.name}**: I got it of some guy that was spying on Merlin, called him one of 'Raven's minions'...not sure what it means but that dude was serious bad news."
            await msg.edit(embed=em)

            await asyncio.sleep(cd)
            em.description += f"\n\n:crossed_swords: **Amethyst**: Oh...you don't know who Raven is? Actually nevermind, that's not my business. Anyways hand over the staff, if it's from one of Raven's guys I know what Merlin wants."
            await msg.edit(embed=em)

            await asyncio.sleep(cd)
            em.description += f" Hey, since you're in the area, you should go visit the Shopkeeper. He sells some pretty cool shit, heard he's been making some potion that can increase your spell damage, go buy one for me while I work on this staff."
            await msg.edit(embed=em)

            await asyncio.sleep(cd)
            em.description += f"\n\n**QUEST OBJECTIVE**: Buy a potion for Amethyst.\n-> `0/1` potions bought.\n-> Use `>shop` to start."
            await msg.edit(embed=em)

        elif quest == "Amethyst2":
            
            em = discord.Embed(
                title = f"⚗️ Spellcrafter Hut",
                description = '',
                colour = discord.Colour.from_rgb(0, 208, 255)
            )
            cd = 5
            em.timestamp = datetime.utcnow()

            em.description += f":crossed_swords: **Amethyst**: Thanks for the potion, I can now finalise your staff, but before that, I need to explain some things."
            msg = await ctx.send(embed=em)
            await msg.edit(embed=em)

            await asyncio.sleep(cd)
            em.description += f"\n\n**{ctx.author.name}**: Oh no, more confusing magic stuff? Merlin has already given me enough of that."
            await msg.edit(embed=em)

            await asyncio.sleep(cd)
            em.description += f"\n\n:crossed_swords: **Amethyst**: Magical weapons can be reforged, if brought to the right Spellcrafter. They can empower your weapon with different magical abilities, which can aid you in your adventures and everyday life."
            await msg.edit(embed=em)

            await asyncio.sleep(cd)
            em.description += f"\n\n**{ctx.author.name}**: That's a little less confusing than I thought. Where can I find a Spellcrafter that can reforge magical weapons?"
            await msg.edit(embed=em)

            await asyncio.sleep(cd)
            em.description += f"\n\n:crossed_swords: **Amethyst**: You're pretty slow kid, you're looking at one right now."
            await msg.edit(embed=em)

            await asyncio.sleep(cd)
            em.description += f"\n\n**{ctx.author.name}**: Oh. Right. Merlin did mention you were a talented Spellcrafter, that makes a little more sense now."
            await msg.edit(embed=em)

            await asyncio.sleep(cd)
            em.description += f"\n\n:crossed_swords: **Amethyst**: Right, anyway. Magical weapons can be rated on how powerful they are, for example that staff would currently be a Tier 1 or **Common** staff. More powerful weapons will give you increased strength, durability (health) and stamina."
            await msg.edit(embed=em)

            await asyncio.sleep(cd)
            em.description += f"\n\n**{ctx.author.name}**: Weapons boosting my stamina? I've never heard of that before."
            await msg.edit(embed=em)

            await asyncio.sleep(cd)
            em.description += f"\n\n:crossed_swords: **Amethyst**: Did Merlin really not teach you anything? Your stamina is your attack speed or general speed during a boss fight. Higher stamina will allow you to have a higher chance to evade boss attacks and instead hit the boss yourself."
            await msg.edit(embed=em)

            await asyncio.sleep(cd)
            em.description += f"\n\n**{ctx.author.name}**: Simple enough. Do I need to get you anything else for the reforge to work?"
            await msg.edit(embed=em)

            await asyncio.sleep(cd)
            em.description += f"\n\n:crossed_swords: **Amethyst**: No. I'll be able to use my enchanting magic to reforge this weapon into something more powerful that will assist you in battles."
            await msg.edit(embed=em)

            await asyncio.sleep(cd)
            em.description += f"\n\n**{ctx.author.name}**: Okay, sounds good."
            await msg.edit(embed=em)

            await asyncio.sleep(cd)
            em.description += f"\n\n:crossed_swords: **Amethyst**: With my enchants on the staff, you should be able to sense things more clearly, you'll find it useful in upcoming battles."
            await msg.edit(embed=em)

            await asyncio.sleep(cd)
            em.description += f"\n\n**{ctx.author.name}**: Before I leave, I have to ask you something-"
            await msg.edit(embed=em)

            await asyncio.sleep(cd)
            em.description += f"\n\n:crossed_swords: **Amethyst**: Unfortunately our time has been cut short, I see potential in you kid.. I sense Merlin's magic in distress, I can't go there myself for- well that's a story for another day. You should hurry up and go to Merlin."
            await msg.edit(embed=em)

            await asyncio.sleep(cd)
            em.description += f"\n\n**QUEST OBJECTIVE**: Help Merlin.\n-> ???\n-> Use `>quest Merlin` to start."
            await msg.edit(embed=em)
            await ctx.author.add_roles(find(lambda r: r.name == "✧ Cursed Staff", ctx.message.guild.roles))
            eco.update_one({"memberid":ctx.author.id},{"$set":{"currentQuest":"Merlin3"}})

        elif quest == "Amethyst3":
            
            em = discord.Embed(
                title = f"⚗️ Spellcrafter Hut",
                description = '',
                colour = discord.Colour.from_rgb(0, 208, 255)
            )
            cd = 5
            em.timestamp = datetime.utcnow()
            msg = await ctx.send(embed=em)

            em.description += f"\n\n:crossed_swords: **Amethyst**: Hey {ctx.author.name}, just in time, I was actually looking for you."
            await msg.edit(embed=em)

            await asyncio.sleep(cd)
            em.description += f"\n\n**{ctx.author.name}**: Hey Amethyst, Merlin told me you were looking for me so I came here, I also wanted to ask you some stuff."
            await msg.edit(embed=em)

            await asyncio.sleep(cd)
            em.description += f"\n\n:crossed_swords: **Amethyst**: Well my quest for you can wait, what's up?"
            await msg.edit(embed=em)

            await asyncio.sleep(cd)
            em.description += f"\n\n**{ctx.author.name}**: I've got some loot from a follower of Raven's, Merlin said you would know what to do with it."
            await msg.edit(embed=em)

            await asyncio.sleep(cd)
            em.description += f"\n\n:crossed_swords: **Amethyst**: This is definitely chaos magic {ctx.author.name}. I could try and take away some of the chaos magic to allow you to use it in battle, I think it would be useful."
            await msg.edit(embed=em)

            await asyncio.sleep(cd)
            em.description += f"\n\n**{ctx.author.name}**: Thanks, I also got this amulet-"
            await msg.edit(embed=em)

            await asyncio.sleep(cd)
            em.description += f"\n\n:crossed_swords: **Amethyst**: That amulet.. I've seen it before. If I remember correctly it was used to forge a weapon called the **Azure Splitter**, translating to Sky Splitter."
            await msg.edit(embed=em)

            await asyncio.sleep(cd)
            em.description += f"\n\n**{ctx.author.name}**: That seems like it would be useful against Raven, could you find a book to show me how to forge it?"
            await msg.edit(embed=em)

            await asyncio.sleep(cd)
            em.description += f"\n\n:crossed_swords: **Amethyst**: Yes, though it would take some time. I need you to go out and slay a Gryphon for me though, you'll need to get 3 specific drops from it, you'll know what they are when you see them."
            await msg.edit(embed=em)

            await asyncio.sleep(cd)
            em.description += f"\n\n**{ctx.author.name}**: Thanks for the vagueness I guess. I'll be back once I have what you need."
            await msg.edit(embed=em)

            await asyncio.sleep(cd)
            em.description += f"\n\n**QUEST OBJECTIVE**: Defeat a Gryphon and get all 3 drops.\n-> ???\n-> Use `>boss Gryphon` to start."
            await msg.edit(embed=em)
            eco.update_one({"memberid":ctx.author.id},{"$set":{"currentQuest":"Amethyst4"}})

        elif quest == "Amethyst4" and feather in ctx.author.roles and claw in ctx.author.roles and heart in ctx.author.roles:
            
            em = discord.Embed(
                title = f"⚗️ Spellcrafter Hut",
                description = '',
                colour = discord.Colour.from_rgb(0, 208, 255)
            )
            cd = 5
            em.timestamp = datetime.utcnow()
            msg = await ctx.send(embed=em)

            em.description += f":crossed_swords: **Amethyst**: I see you've gotten the materials that you need."
            await msg.edit(embed=em)

            await asyncio.sleep(cd)
            em.description += f"\n\n**{ctx.author.name}**: Yeah, that was rough honestly."
            await msg.edit(embed=em)

            await asyncio.sleep(cd)
            em.description += f"\n\n:crossed_swords: **Amethyst**: Just in time actually, I found the book that shows what you need to craft the Azure Splitter.. and something else as well."
            await msg.edit(embed=em)

            await asyncio.sleep(cd)
            em.description += f"\n\n**{ctx.author.name}**: Oh great, I've got everything I need already, what's the other thing you found though?"
            await msg.edit(embed=em)

            await asyncio.sleep(cd)
            em.description += f"\n\n:crossed_swords: **Amethyst**: I shall let you find out on your own.."
            await msg.edit(embed=em)

            await asyncio.sleep(cd)
            em.description += f"\n\n**QUEST OBJECTIVE**: Craft the **Azure Splitter**.\n-> ???\n-> Use `>craft` to start."
            await msg.edit(embed=em)
            eco.update_one({"memberid":ctx.author.id},{"$set":{"currentQuest":"Amethyst5"}})

    @commands.command()
    async def craft(self, ctx, *, item=None):

        feather = find(lambda r: r.name == "🕊️ Gryphon's Feather", ctx.message.guild.roles)
        claw = find(lambda r: r.name == "🐉 Gryphon's Claw", ctx.message.guild.roles)
        heart = find(lambda r: r.name == "❤️ Gryphon's Heart", ctx.message.guild.roles)
        azure_splitter = find(lambda r: r.name == "⚜️ Azure Splitter", ctx.message.guild.roles)
        amulet = find(lambda r: r.name == "⚜️ Gryphon's Delirium", ctx.message.guild.roles)
        raven_dagger = find(lambda r: r.name == "✪ Raven's Dagger", ctx.message.guild.roles)
        darkness_amulet = find(lambda r: r.name == "✪ Darkness Amulet", ctx.message.guild.roles)

        if item is None:

            em = discord.Embed(
                title = "Crafting Guide",
                description = "This is a guide to show all recipes that have been unlocked and what each crafted item does.\n<:transparent:911319446918955089>",
                colour = discord.Colour.from_rgb(0, 208, 255)
            )

            em.add_field(name="⚜️ Azure Splitter (Weapon)", value="> **Required**: Gryphon Feather, Gryphon Claw and Raven's Dagger\n> **Cost**: :gem: 1.5M\n> **Ability**: Gain +10% More Damage in boss fights, along with more base health and base damage.\n<:transparent:911319446918955089>", inline=False)
            em.add_field(name="⚜️ Gryphon's Delirium (Amulet)", value="> **Required**: Darkness Amulet and Gryphon Heart\n> **Cost**: :gem: 1.5M\n> **Ability**: Gain a passive 1.5x multiplier for income commands as well as a passive 1.5x income for rank collects.", inline=False)
            em.timestamp = datetime.utcnow()
            await ctx.send(embed=em)

        elif item in ["Azure Splitter", "azure splitter", "Azure splitter"]:
            
            bal = eco.find_one({"memberid":ctx.author.id})["bal"]

            if bal >= 1500000 and feather in ctx.author.roles and claw in ctx.author.roles and raven_dagger in ctx.author.roles:
                em = discord.Embed(
                    description = "Successfully crafted the **Azure Splitter**.",
                    colour = discord.Colour.from_rgb(0, 208, 255)
                )
                em.set_author(name=ctx.author,icon_url=ctx.author.display_avatar)
                em.timestamp = datetime.utcnow()
                await ctx.send(embed=em)
                await ctx.author.remove_roles(feather)
                await ctx.author.remove_roles(claw)
                await ctx.author.remove_roles(raven_dagger)
                await ctx.author.add_roles(azure_splitter)
                eco.update_one({"memberid":ctx.author.id},{"$set":{"bal":bal-1500000}})

            else:
                em = discord.Embed(
                    description = "You do not meet the requirements to craft this weapon.",
                    colour = discord.Colour.from_rgb(0, 208, 255)
                )
                em.set_author(name=ctx.author,icon_url=ctx.author.display_avatar)
                em.timestamp = datetime.utcnow()
                await ctx.send(embed=em)

        elif item in ["Gryphon Delirium", "Gryphon delirium", "gryphon delirium"]:
            
            bal = eco.find_one({"memberid":ctx.author.id})["bal"]

            if bal >= 1500000 and heart in ctx.author.roles and darkness_amulet in ctx.author.roles:
                em = discord.Embed(
                    description = "Successfully crafted the **Gryphon Delirium**.",
                    colour = discord.Colour.from_rgb(0, 208, 255)
                )
                em.set_author(name=ctx.author,icon_url=ctx.author.display_avatar)
                em.timestamp = datetime.utcnow()
                await ctx.send(embed=em)
                await ctx.author.remove_roles(heart)
                await ctx.author.remove_roles(darkness_amulet)
                await ctx.author.add_roles(amulet)
                eco.update_one({"memberid":ctx.author.id},{"$set":{"bal":bal-1500000}})

            else:
                em = discord.Embed(
                    description = "You do not meet the requirements to craft this amulet.",
                    colour = discord.Colour.from_rgb(0, 208, 255)
                )
                em.set_author(name=ctx.author,icon_url=ctx.author.display_avatar)
                em.timestamp = datetime.utcnow()
                await ctx.send(embed=em)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def resetquest(self, ctx):

        Economy = eco.find_one({"memberid":ctx.author.id})
        quest = Economy["currentQuest"]

        print(quest)
        eco.update_one({"memberid":ctx.author.id},{"$set":{"currentQuest": "Merlin1"}})

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setquest(self, ctx, *, _quest):

        Economy = eco.find_one({"memberid":ctx.author.id})
        quest = Economy["currentQuest"]

        eco.update_one({"memberid":ctx.author.id},{"$set":{"currentQuest": _quest}})
        quest = Economy["currentQuest"]
        await ctx.send(quest)

    @commands.command(aliases = ["cq"])
    async def checkquest(self, ctx):

        Economy = eco.find_one({"memberid":ctx.author.id})
        quest = Economy["currentQuest"]
        obj = Economy["questObjectiveCounter"]

        em = discord.Embed(
            description = f"**Current Quest:** {quest}\n**Objective Counter**: {obj}\n\n*Note: Not all quests require the objective counter, though some quests such as Merlin3 do require it.*",
            colour = discord.Colour.from_rgb(0, 208, 255)
        )
        em.set_author(name=ctx.author,icon_url=ctx.author.display_avatar)
        em.timestamp = datetime.utcnow()
        await ctx.send(embed=em)

def setup(client):
    client.add_cog(NPCS(client))