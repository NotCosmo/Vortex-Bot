# Main Imports

import nextcord as discord
import random
import asyncio
import time

# Other

from nextcord.ext import commands
from nextcord.ext.commands import BucketType
from nextcord.utils import find
import datetime
from pymongo import MongoClient

# ------------------------------- #
''' Cluster '''
# ------------------------------- #

cluster = MongoClient("mongodb+srv://Cosmo:1H1uqPGjo5CjtHQe@eco.5afje.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
database = cluster["Discord"]
eco = database["Economy"]

class BJ(discord.ui.View):
    def __init__(self, bet, user_money, me, dealer):
        super().__init__()
        self.bet = bet
        self.user_money = user_money
        self.me = me
        self.dealer = dealer

    @discord.ui.button(label='Hit', style=discord.ButtonStyle.blurple)
    async def hit(self, button, interaction):

        await interaction.response.defer()

        import random

        rng = random.randint(3, 7)

        self.me += rng

        if self.me > 21:
            em = discord.Embed(description=f"Result: Lost :gem: {self.bet:,}.",colour=discord.Colour.from_rgb(255, 75, 75))
            em.set_author(name=interaction.author,icon_url=interaction.author.display_avatar)
            em.add_field(name="Your Hand",value=self.me,inline=True)
            em.add_field(name="Dealer Hand",value=self.dealer,inline=True)
            em.timestamp = datetime.datetime.utcnow()

            await interaction.edit_original_message(
                embed=em
                #content=f'You: {self.me}\nDealer: {self.dealer}\n\nYou lost!'
            )
            self.stand.disabled = True
            self.hit.disabled = True
            await interaction.edit_original_message(view=self)
            updateMoney = self.user_money - self.bet
            eco.update_one({"memberid":interaction.author.id},{"$set":{"bal": updateMoney}})
            return

        if self.me == 21:
            em = discord.Embed(description=f"Result: Won :gem: {self.bet:,}.",colour=discord.Colour.from_rgb(75, 255, 75))
            em.set_author(name=interaction.author,icon_url=interaction.author.display_avatar)
            em.add_field(name="Your Hand",value=self.me,inline=True)
            em.add_field(name="Dealer Hand",value=self.dealer,inline=True)
            em.timestamp = datetime.datetime.utcnow()

            await interaction.edit_original_message(
                embed=em
            )
            self.stand.disabled = True
            self.hit.disabled = True
            await interaction.edit_original_message(view=self)
            updateMoney = self.user_money + self.bet
            eco.update_one({"memberid":interaction.author.id},{"$set":{"bal": updateMoney}})
            return

        else:
            em = discord.Embed(description=f"Bet: :gem: {self.bet:,}.",colour=discord.Colour.from_rgb(0, 208, 255))
            em.set_author(name=interaction.author,icon_url=interaction.author.display_avatar)
            em.add_field(name="Your Hand",value=self.me,inline=True)
            em.add_field(name="Dealer Hand",value=self.dealer,inline=True)
            em.timestamp = datetime.datetime.utcnow()

            await interaction.edit_original_message(
                embed=em
            )
            return

    @discord.ui.button(label='Stand', style=discord.ButtonStyle.blurple)
    async def stand(self, button, interaction):

        await interaction.response.defer()
        rng = random.randint(3, 7)

        self.dealer += rng

        if self.dealer > 21:
            em = discord.Embed(description=f"Result: Won :gem: {self.bet:,}.",colour=discord.Colour.from_rgb(75, 255, 75))
            em.set_author(name=interaction.author,icon_url=interaction.author.display_avatar)
            em.add_field(name="Your Hand",value=self.me,inline=True)
            em.add_field(name="Dealer Hand",value=self.dealer,inline=True)
            em.timestamp = datetime.datetime.utcnow()

            await interaction.edit_original_message(
                embed=em
            )
            self.stand.disabled = True
            self.hit.disabled = True
            await interaction.edit_original_message(view=self)
            updateMoney = self.user_money + self.bet
            eco.update_one({"memberid":interaction.author.id},{"$set":{"bal": updateMoney}})
            return

        if self.dealer == 21:
            em = discord.Embed(description=f"Result: Lost :gem: {self.bet:,}",colour=discord.Colour.from_rgb(255, 75, 75))
            em.set_author(name=interaction.author,icon_url=interaction.author.display_avatar)
            em.add_field(name="Your Hand",value=self.me,inline=True)
            em.add_field(name="Dealer Hand",value=self.dealer,inline=True)
            em.timestamp = datetime.datetime.utcnow()

            await interaction.edit_original_message(
                embed=em
            )
            self.stand.disabled = True
            self.hit.disabled = True
            await interaction.edit_original_message(view=self)
            updateMoney = self.user_money - self.bet
            eco.update_one({"memberid":interaction.author.id},{"$set":{"bal": updateMoney}})
            return

        else:
            em = discord.Embed(description=f"Bet: :gem: {self.bet:,}.",colour=discord.Colour.from_rgb(0, 208, 255))
            em.set_author(name=interaction.author,icon_url=interaction.author.display_avatar)
            em.add_field(name="Your Hand",value=self.me,inline=True)
            em.add_field(name="Dealer Hand",value=self.dealer,inline=True)
            em.timestamp = datetime.datetime.utcnow()

            return await interaction.edit_original_message(
                embed=em
            )

# ------------------------------- #
''' Setup '''
# ------------------------------- #

class EcoGames(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def dice(self, ctx, bet=None):

        id = ctx.author.id

        if eco.count_documents({"memberid":id}) == 0:
            eco.insert_one({"memberid": id,"bal": 0})

        Economy = eco.find_one({"memberid":id})
        money = Economy["bal"]

        if bet == "all":
            bet = int(money)

        elif bet == "0":
            return

        elif bet == "half":
            bet = int(money/2)

        elif "e" in bet:

            string = bet.split("e")
            num = string[0]
            exponent = string[1]
            
            bet = int(num) * (10 ** int(exponent))

        elif "," in bet:

            string = bet.split(",")
            _string = ''
            for x in string:
                _string += x
                bet = int(_string)

        else:

            bet = int(bet)

        if bet < 0:
            em = discord.Embed(
                description = ":no_entry_sign: Please provide a positive number!",
                colour = discord.Colour.from_rgb(0, 208, 255)
            )

            em.set_author(name=ctx.author, icon_url=ctx.author.display_avatar)
            em.timestamp = datetime.datetime.utcnow()
            return await ctx.send(embed=em)

        bet = abs(bet)
        if bet == None:

            em = discord.Embed(
                description = ":x: Not enough arguments given!\n\nUsage:\n`dice <bet>`",
                colour = discord.Colour.from_rgb(0, 208, 255)
            )

            em.set_author(name=ctx.author, icon_url=ctx.author.display_avatar)
            em.timestamp = datetime.datetime.utcnow()
            return await ctx.send(embed=em)

        if bet == 0:
            return

        if bet <= money:

            userRoll = random.randint(1, 12)
            botRoll = random.randint(1, 12)

            em = discord.Embed(
                title = ":game_die: Dice Roll!",
                description = f"> **{ctx.author.name}** rolled a {userRoll}!",
                colour = discord.Colour.from_rgb(0, 208, 255)
            )
            em.timestamp = datetime.datetime.utcnow()
            msg = await ctx.reply(embed=em)

            em2 = discord.Embed(
                title = ":game_die: Dice Roll!",
                description = f"> **{ctx.author.name}** rolled a {userRoll}!\n> \n> **Bot** rolled a {botRoll}!",
                colour = discord.Colour.from_rgb(0, 208, 255)
            )
            em2.timestamp = datetime.datetime.utcnow()
            await asyncio.sleep(.5)
            await msg.edit(embed=em2)

            # User Wins
            if userRoll > botRoll:

                updateMoney = money + bet
                eco.update_one({"memberid":id},{"$set":{"bal": updateMoney}})

                em3 = discord.Embed(
                    title = ":game_die: Dice Roll!",
                    description = f"> **{ctx.author.name}** rolled a {userRoll}!\n> **Bot** rolled a {botRoll}!\n\n> :trophy: **{ctx.author.mention}**, won :gem: {bet:,}",
                    colour = discord.Colour.from_rgb(75, 255, 75)
                )
                em3.timestamp = datetime.datetime.utcnow()
                await msg.edit(embed=em3)

            # Tie
            elif botRoll == userRoll:

                em3 = discord.Embed(
                    title = ":game_die: Dice Roll!",
                    description = f"> **{ctx.author.name}** rolled a {userRoll}!\n> **Bot** rolled a {botRoll}!\n\n> :trophy: **Draw**, money back!",
                    colour = discord.Colour.from_rgb(0, 208, 255)
                )

                await msg.edit(embed=em3)

            # Bot wins
            else:
                
                updateMoney = money - bet
                eco.update_one({"memberid":id},{"$set":{"bal": updateMoney}})

                em3 = discord.Embed(
                    title = ":game_die: Dice Roll!",
                    description = f"> **{ctx.author.name}** rolled a {userRoll}!\n> **Bot** rolled a {botRoll}!\n> :trophy: **Bot** wins! Lost :gem: {bet:,}",
                    colour = discord.Colour.from_rgb(255, 75, 75)
                )

                await msg.edit(embed=em3)

        # User does not have enough money
        else:

            embed = discord.Embed(
                title = ":game_die: Dice Roll!",
                description = f"You do not have enough money for that!",
                colour = discord.Colour.red()
            )
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=embed)

    @commands.command(aliases = ["slotmachine", "slotsmachine"])
    async def slots(self, ctx, bet=None):
        
        id = ctx.author.id

        if eco.count_documents({"memberid":id}) == 0:
            eco.insert_one({"memberid": id,"bal": 0})

        Economy = eco.find_one({"memberid":id})
        money = Economy["bal"]

        if bet == "all":
            bet = int(money)

        elif bet == "0":
            return

        elif bet == "half":
            bet = int(money/2)

        elif "e" in bet:

            string = bet.split("e")
            num = string[0]
            exponent = string[1]
            
            bet = int(num) * (10 ** int(exponent))

        elif "," in bet:

            string = bet.split(",")
            _string = ''
            for x in string:
                _string += x
                bet = int(_string)

        else:

            bet = int(bet)

        if bet < 0:
            em = discord.Embed(
                description = ":x: Please provide a positive number!",
                colour = discord.Colour.from_rgb(0, 208, 255)
            )

            em.set_author(name=ctx.author, icon_url=ctx.author.display_avatar)
            em.timestamp = datetime.datetime.utcnow()
            return await ctx.send(embed=em)

        bet = abs(bet)
        if bet == None:

            em = discord.Embed(
                description = ":no_entry_sign: Not enough arguments given!\n\nUsage:\n`slots <bet>`",
                colour = discord.Colour.from_rgb(0, 208, 255)
            )

            em.set_author(name=ctx.author, icon_url=ctx.author.display_avatar)
            em.timestamp = datetime.datetime.utcnow()
            return await ctx.send(embed=em)


        if bet == 0:
            return

        # User has enough money
        if bet <= money:

            tiles = [":eggplant:", ":banana:", "<:nutsack:843602229658517524>"]

            T1 = random.choice(tiles)
            T2 = random.choice(tiles)
            T3 = random.choice(tiles)
            T4 = random.choice(tiles)
            T5 = random.choice(tiles)
            T6 = random.choice(tiles)
            T7 = random.choice(tiles)
            T8 = random.choice(tiles)
            T9 = random.choice(tiles)

            em = discord.Embed(
                title = ":slot_machine: Slot Machine",
                description = f"> {T1}{T2}{T3}\n" + f"> {T4}{T5}{T6}\n" + f"> {T7}{T8}{T9}",
                colour = discord.Colour.from_rgb(0, 208, 255)
            )

            msg = await ctx.send(embed=em)

            for i in range(5):

                T1 = random.choice(tiles)
                T2 = random.choice(tiles)
                T3 = random.choice(tiles)
                T4 = random.choice(tiles)
                T5 = random.choice(tiles)
                T6 = random.choice(tiles)
                T7 = random.choice(tiles)
                T8 = random.choice(tiles)
                T9 = random.choice(tiles)

                em2 = discord.Embed(
                    title = ":slot_machine: Slot Machine",
                    description = f"> {T1}{T2}{T3}\n" + f"> {T4}{T5}{T6}\n" + f"> {T7}{T8}{T9}",
                    colour = discord.Colour.from_rgb(0, 208, 255)
                )

                await msg.edit(embed=em2)
                await asyncio.sleep(0.75)

            T1 = random.choice(tiles)
            T2 = random.choice(tiles)
            T3 = random.choice(tiles)
            T4 = random.choice(tiles)
            T5 = random.choice(tiles)
            T6 = random.choice(tiles)
            T7 = random.choice(tiles)
            T8 = random.choice(tiles)
            T9 = random.choice(tiles)

            em2 = discord.Embed(
                title = ":slot_machine: Slot Machine",
                description = f"> {T1}{T2}{T3}\n" + f"> {T4}{T5}{T6}\n" + f"> {T7}{T8}{T9}",
                colour = discord.Colour.from_rgb(0, 208, 255)
            )

            await msg.edit(embed=em2)

            # User Wins
            if T4 == T5 and T5 == T6:

                _money = money + bet
                eco.update_one({"memberid":id},{"$set":{"bal": _money}})
                em2.description += f"\n\nYou won :gem: {bet} {T4}{T5}{T6}"
                await msg.edit(embed=em2)

            # User loses
            else:

                _money = money - bet
                eco.update_one({"memberid":id},{"$set":{"bal": _money}})
                em2.description += f"\n\nYou lost :gem: {bet} {T4}{T5}{T6}"
                await msg.edit(embed=em2)

        # User is too poor
        else:
            embed = discord.Embed(
                title = ":slot_machine: Slot Machine",
                description = f"You do not have enough money for that!",
                colour = discord.Colour.red()
            )
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=embed)

    @commands.command()
    async def cf(self, ctx, bet=None):

        id = ctx.author.id

        if eco.count_documents({"memberid":id}) == 0:
            eco.insert_one({"memberid": id,"bal": 0})

        Economy = eco.find_one({"memberid":id})
        money = Economy["bal"]
        ws = Economy["cfWinStreak"]


        if bet == "all":
            bet = int(money)

        elif bet == "0":
            return

        elif bet == "half":
            bet = int(money/2)

        elif "e" in bet:

            string = bet.split("e")
            num = string[0]
            exponent = string[1]
                
            bet = int(num) * (10 ** int(exponent))

        elif "," in bet:

            string = bet.split(",")
            _string = ''
            for x in string:
                _string += x
                bet = int(_string)

        else:

            bet = int(bet)

        if bet < 0:
            em = discord.Embed(
                description = ":x: Please provide a positive number!",
                colour = discord.Colour.from_rgb(0, 208, 255)
            )

            em.set_author(name=ctx.author, icon_url=ctx.author.display_avatar)
            em.timestamp = datetime.datetime.utcnow()
            return await ctx.send(embed=em)

        bet = abs(bet)
        if bet == None:

            em = discord.Embed(
                description = ":no_entry_sign: Not enough arguments given!\n\nUsage:\n`cf <bet>`",
                colour = discord.Colour.from_rgb(0, 208, 255)
            )

            em.set_author(name=ctx.author, icon_url=ctx.author.display_avatar)
            em.timestamp = datetime.datetime.utcnow()
            return await ctx.send(embed=em)

        if bet == 0:
            return
        
        _chance = random.randint(1, 100)
        percentChance = 50 + ws
        winChance = _chance in range(percentChance, 100)

        if bet <= money:
            
            if winChance == True:

                ws += 1

                updateMoney = money + bet
                percentChance = 50 + ws

                eco.update_one({"memberid":id},{"$set":{"bal": updateMoney}})
                eco.update_one({"memberid":id},{"$set":{"cfWinStreak": ws}})

                embed = discord.Embed(
                    description = f"You just made :gem: {int(bet):,}!",
                    colour = discord.Colour.green()
                )
                embed.set_author(name=f"Cockfight", icon_url=ctx.author.display_avatar)
                embed.set_footer(text=f"Win Chance: {percentChance}%")
                embed.timestamp = datetime.datetime.utcnow()
                await ctx.reply(embed=embed)

            else:
                newMoney = money - bet
                eco.update_one({"memberid":id},{"$set":{"bal": newMoney}})

                embed = discord.Embed(
                    description = f"You just lost :gem: {int(bet):,}!",
                    colour = discord.Colour.red()
                )

                embed.set_author(name=f"Cockfight", icon_url=ctx.author.display_avatar)
                embed.set_footer(text=f"Lost {ws} win streak!")
                embed.timestamp = datetime.datetime.utcnow()
                await ctx.reply(embed=embed)

                eco.update_one({"memberid":id},{"$set":{"cfWinStreak": 0}})

        # User does not have enough money
        else:

            embed = discord.Embed(
                description = f"You do not have enough money for that!",
                colour = discord.Colour.red()
            )

            embed.set_author(name=f"Cockfight", icon_url=ctx.author.display_avatar)
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.reply(embed=embed)


# ------------------------------- #
''' Client '''
# ------------------------------- #
def setup(client):
    client.add_cog(EcoGames(client))