import discord
import random
import asyncio
import datetime
from loot_table import boss1_lootTable, boss2_lootTable, boss3_lootTable, boss4_lootTable, boss5_lootTable
from discord.ext import commands
from discord.ext.commands import BucketType


class Boss(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.cooldown(1, 2, BucketType.user)
    async def boss(self, ctx, *, bossName=None):

        if bossName == 'Kraken' or bossName == 'kraken':

            rankReq = discord.utils.find(lambda r: r.name == '[✦] Mage', ctx.message.guild.roles)
            keyReq = discord.utils.find(lambda r: r.name == '[🌊] Key of the Sea', ctx.message.guild.roles)
            krakenWeapon = discord.utils.find(lambda r: r.name == "[✦] Kraken's Eye", ctx.message.guild.roles)
            # gaiaTitle = discord.utils.find(lambda r: r.name == "[⚔️] Slayer of the Earth", ctx.message.guild.roles)
            logChannel = self.client.get_channel(873941431570546770)

            if rankReq in ctx.author.roles and keyReq in ctx.author.roles:

                bossHP = 50000
                playerHP = 1500

                if krakenWeapon in ctx.author.roles:
                    dpsMin = 4000
                    dpsMax = 5000
                    playerHP = 2500

                else:
                    dpsMin = 2000
                    dpsMax = 2500
                    playerHP = 1500

                embed = discord.Embed(
                    title='🦑 The Kraken',
                    description=f'__**Boss Health**__\n:heart: {bossHP}\n\n__**Player Health**__\n:heart: {playerHP}\n\n__**Difficulty**__\n:star: :star:',
                    colour=discord.Colour.red()
                )

                msg = await ctx.send(embed=embed)
                while bossHP > 0 and playerHP > 0:
                    await asyncio.sleep(1)
                    DPS = random.randint(dpsMin, dpsMax)
                    playerDamage = random.randint(55, 75)
                    bossHP = bossHP - DPS
                    await asyncio.sleep(0.1)
                    playerHP = playerHP - playerDamage

                    embed2 = discord.Embed(
                        title='🦑 The Kraken',
                        description=f'\n\n__**Boss Health**__\n:heart: {bossHP} *[-{DPS}]*\n\n__**Player Health**__\n:heart: {playerHP} *[-{playerDamage}]*\n\n__**Difficulty**__\n:star: :star:',
                        colour=discord.Colour.red()
                    )
                    await msg.edit(embed=embed2)

                if bossHP <= 0:

                    if playerHP <= 0:
                        embed = discord.Embed(
                            title='You have died.',
                            description='The boss killed you before you killed it.',
                            colour=discord.Colour.from_rgb(255, 95, 95)
                        )
                        await ctx.send(f'{ctx.author.mention}')
                        await ctx.send(embed=embed)
                        await ctx.author.remove_roles(keyReq)

                    else:
                        l1 = random.choice(boss1_lootTable)
                        l2 = random.choice(boss1_lootTable)
                        l3 = random.choice(boss1_lootTable)
                        embed = discord.Embed(
                            title='The Kraken has been defeated',
                            description=f'__**Loot**__\n\n- {l1}\n- {l2}\n- {l3}',
                            colour=discord.Colour.from_rgb(0, 208, 255)
                        )
                        embed2 = discord.Embed(
                            title='Boss Defeated',
                            description=f'{ctx.author.mention} has defeated the Kraken.\n \n __**Loot**__\n- {l1}\n- {l2}\n- {l3}',
                            colour=discord.Colour.from_rgb(0, 208, 255)
                        )
                        if l1 == '[ITEM] Krakens Eye' or l2 == '[ITEM] Krakens Eye' or l3 == '[ITEM] Krakens Eye':
                            await ctx.author.add_roles(krakenWeapon)

                        await ctx.send(f'{ctx.author.mention}')
                        await ctx.author.remove_roles(keyReq)
                        await logChannel.send(embed=embed2)
                        await ctx.send(embed=embed)

                elif playerHP <= 0:

                    embed = discord.Embed(
                        title='You have died.',
                        description='The boss killed you before you killed it.',
                        colour=discord.Colour.from_rgb(255, 95, 95)
                    )
                    await ctx.send(f'{ctx.author.mention}')
                    await ctx.send(embed=embed)

        if bossName == 'Gorgon' or bossName == 'gorgon':

            rankReq = discord.utils.find(lambda r: r.name == '[✦ XII] Divine Mage', ctx.message.guild.roles)
            keyReq = discord.utils.find(lambda r: r.name == '[✦] Shadow Key', ctx.message.guild.roles)
            krakenWeapon = discord.utils.find(lambda r: r.name == "[✦] Kraken's Eye", ctx.message.guild.roles)
            weaponDrop = discord.utils.find(lambda r: r.name == "[✦] Gorgons Shadow", ctx.message.guild.roles)
            # gaiaTitle = discord.utils.find(lambda r: r.name == "[⚔️] Slayer of the Earth", ctx.message.guild.roles)
            logChannel = self.client.get_channel(873941431570546770)

            if rankReq in ctx.author.roles and keyReq in ctx.author.roles:

                bossHP = 100000
                if krakenWeapon in ctx.author.roles:
                    dpsMin = 4000
                    dpsMax = 5000
                    playerHP = 2500

                else:
                    dpsMin = 2000
                    dpsMax = 2500
                    playerHP = 1500

                embed = discord.Embed(
                    title='Gorgon',
                    description=f'__**Boss Health**__\n:heart: {bossHP}\n\n__**Player Health**__\n:heart: {playerHP}\n\n__**Difficulty**__\n:star: :star: :star:',
                    colour=discord.Colour.red()
                )

                msg = await ctx.send(embed=embed)
                while bossHP > 0 and playerHP > 0:
                    await asyncio.sleep(1)
                    DPS = random.randint(dpsMin, dpsMax)
                    playerDamage = random.randint(90, 115)
                    bossHP = bossHP - DPS
                    await asyncio.sleep(0.1)
                    playerHP = playerHP - playerDamage

                    embed2 = discord.Embed(
                        title='Gorgon',
                        description=f'\n\n__**Boss Health**__\n:heart: {bossHP} *[-{DPS}]*\n\n__**Player Health**__\n:heart: {playerHP} *[-{playerDamage}]*\n\n__**Difficulty**__\n:star: :star: :star:',
                        colour=discord.Colour.red()
                    )
                    await msg.edit(embed=embed2)

                if bossHP <= 0:

                    if playerHP <= 0:
                        if bossHP <= 0:
                            bossHP = 0

                        embed = discord.Embed(
                            title='You have died.',
                            description='The boss killed you before you killed it.',
                            colour=discord.Colour.from_rgb(255, 95, 95)
                        )
                        embed2 = discord.Embed(
                            title='Gorgon',
                            description=f'\n\n__**Boss Health**__\n:heart: {bossHP} *[-{DPS}]*\n\n__**Player Health**__\n:heart: 0 *[-{playerDamage}]*\n\n__**Difficulty**__\n:star: :star:',
                            colour=discord.Colour.red()
                        )
                        await ctx.send(f'{ctx.author.mention}')
                        await ctx.send(embed=embed)
                        await ctx.author.remove_roles(keyReq)
                        await msg.edit(embed=embed2)

                    else:
                        l1 = random.choice(boss2_lootTable)
                        l2 = random.choice(boss2_lootTable)
                        l3 = random.choice(boss2_lootTable)
                        embed = discord.Embed(
                            title='The Gorgon has been defeated',
                            description=f'__**Loot**__\n\n- {l1}\n- {l2}\n- {l3}',
                            colour=discord.Colour.from_rgb(0, 208, 255)
                        )
                        embed2 = discord.Embed(
                            title='Boss Defeated',
                            description=f'{ctx.author.mention} has defeated the Gorgon.\n \n __**Loot**__\n- {l1}\n- {l2}\n- {l3}',
                            colour=discord.Colour.from_rgb(0, 208, 255)
                        )
                        embed3 = discord.Embed(
                            title='Gorgon',
                            description=f'\n\n__**Boss Health**__\n:heart: 0 *[-{DPS}]*\n\n__**Player Health**__\n:heart: {playerHP} *[-{playerDamage}]*\n\n__**Difficulty**__\n:star: :star:',
                            colour=discord.Colour.red()
                        )
                        if l1 == '[ITEM] Gorgons Shadow' or l2 == '[ITEM] Gorgons Shadow' or l3 == '[ITEM] Gorgons Shadow':
                            await ctx.author.add_roles(weaponDrop)

                        await ctx.send(f'{ctx.author.mention}')
                        await ctx.author.remove_roles(keyReq)
                        await logChannel.send(embed=embed2)
                        await ctx.send(embed=embed)
                        await msg.edit(embed=embed3)

                elif playerHP <= 0:

                    embed = discord.Embed(
                        title='You have died.',
                        description='The boss killed you before you killed it.',
                        colour=discord.Colour.from_rgb(255, 95, 95)
                    )
                    embed2 = discord.Embed(
                        title='Gorgon',
                        description=f'\n\n__**Boss Health**__\n:heart: {bossHP} *[-{DPS}]*\n\n__**Player Health**__\n:heart: 0 *[-{playerDamage}]*\n\n__**Difficulty**__\n:star: :star:',
                        colour=discord.Colour.red()
                    )
                    await ctx.send(f'{ctx.author.mention}')
                    await ctx.send(embed=embed)
                    await ctx.author.remove_roles(keyReq)
                    await msg.edit(embed=embed2)

        if bossName == 'Hera' or bossName == 'hera':

            rankReq = discord.utils.find(lambda r: r.name == '[✦ XIII] Celestial', ctx.message.guild.roles)
            keyReq = discord.utils.find(lambda r: r.name == '[✨] Celestial Key', ctx.message.guild.roles)
            gorgonWeapon = discord.utils.find(lambda r: r.name == "[✦] Gorgons Shadow", ctx.message.guild.roles)
            weaponDrop = discord.utils.find(lambda r: r.name == "[✨] Godly Scepter", ctx.message.guild.roles)
            # gaiaTitle = discord.utils.find(lambda r: r.name == "[⚔️] Slayer of the Earth", ctx.message.guild.roles)
            logChannel = self.client.get_channel(873941431570546770)

            if rankReq in ctx.author.roles and keyReq in ctx.author.roles:

                bossHP = 175000
                if gorgonWeapon in ctx.author.roles:
                    dpsMin = 8000
                    dpsMax = 10000
                    playerHP = 3850

                elif weaponDrop in ctx.author.roles:
                    dpsMin = 16000
                    dpsMax = 20000
                    playerHP = 4250

                else:
                    dpsMin = 2000
                    dpsMax = 2500
                    playerHP = 1500

                embed = discord.Embed(
                    title='Hera',
                    description=f'__**Boss Health**__\n:heart: {bossHP}\n\n__**Player Health**__\n:heart: {playerHP}\n\n__**Difficulty**__\n:star: :star: :star: :star:',
                    colour=discord.Colour.red()
                )

                msg = await ctx.send(embed=embed)
                while bossHP > 0 and playerHP > 0:
                    await asyncio.sleep(1)
                    DPS = random.randint(dpsMin, dpsMax)
                    playerDamage = random.randint(170, 210)
                    bossHP = bossHP - DPS
                    await asyncio.sleep(0.1)
                    playerHP = playerHP - playerDamage

                    embed2 = discord.Embed(
                        title='Hera',
                        description=f'\n\n__**Boss Health**__\n:heart: {bossHP} *[-{DPS}]*\n\n__**Player Health**__\n:heart: {playerHP} *[-{playerDamage}]*\n\n__**Difficulty**__\n:star: :star: :star: :star:',
                        colour=discord.Colour.red()
                    )
                    await msg.edit(embed=embed2)

                if bossHP <= 0:

                    if playerHP <= 0:
                        if bossHP <= 0:
                            bossHP = 0

                        embed = discord.Embed(
                            title='You have died.',
                            description='The boss killed you before you killed it.',
                            colour=discord.Colour.from_rgb(255, 95, 95)
                        )
                        embed2 = discord.Embed(
                            title='Hera',
                            description=f'\n\n__**Boss Health**__\n:heart: {bossHP} *[-{DPS}]*\n\n__**Player Health**__\n:heart: 0 *[-{playerDamage}]*\n\n__**Difficulty**__\n:star: :star: :star: :star:',
                            colour=discord.Colour.red()
                        )
                        await ctx.send(f'{ctx.author.mention}')
                        await ctx.send(embed=embed)
                        await ctx.author.remove_roles(keyReq)
                        await msg.edit(embed=embed2)

                    else:
                        l1 = random.choice(boss3_lootTable)
                        l2 = random.choice(boss3_lootTable)
                        l3 = random.choice(boss3_lootTable)
                        embed = discord.Embed(
                            title='Hera has been defeated',
                            description=f'__**Loot**__\n\n- {l1}\n- {l2}\n- {l3}',
                            colour=discord.Colour.from_rgb(0, 208, 255)
                        )
                        embed2 = discord.Embed(
                            title='Boss Defeated',
                            description=f'{ctx.author.mention} has defeated Hera.\n \n __**Loot**__\n- {l1}\n- {l2}\n- {l3}',
                            colour=discord.Colour.from_rgb(0, 208, 255)
                        )
                        embed3 = discord.Embed(
                            title='Hera',
                            description=f'\n\n__**Boss Health**__\n:heart: 0 *[-{DPS}]*\n\n__**Player Health**__\n:heart: {playerHP} *[-{playerDamage}]*\n\n__**Difficulty**__\n:star: :star:',
                            colour=discord.Colour.red()
                        )
                        if l1 == '[ITEM] Godly Scepter' or l2 == '[ITEM] Godly Scepter' or l3 == '[ITEM] Godly Scepter':
                            await ctx.author.add_roles(weaponDrop)

                        await ctx.send(f'{ctx.author.mention}')
                        await ctx.author.remove_roles(keyReq)
                        await logChannel.send(embed=embed2)
                        await ctx.send(embed=embed)
                        await msg.edit(embed=embed3)

                elif playerHP <= 0:

                    embed = discord.Embed(
                        title='You have died.',
                        description='The boss killed you before you killed it.',
                        colour=discord.Colour.from_rgb(255, 95, 95)
                    )
                    embed2 = discord.Embed(
                        title='Hera',
                        description=f'\n\n__**Boss Health**__\n:heart: {bossHP} *[-{DPS}]*\n\n__**Player Health**__\n:heart: 0 *[-{playerDamage}]*\n\n__**Difficulty**__\n:star: :star: :star: :star:',
                        colour=discord.Colour.red()
                    )
                    await ctx.send(f'{ctx.author.mention}')
                    await ctx.send(embed=embed)
                    await ctx.author.remove_roles(keyReq)
                    await msg.edit(embed=embed2)

        if bossName == 'Serpent' or bossName == 'serpent':

            rankReq = discord.utils.find(lambda r: r.name == '[✦ XV] Worldkeeper', ctx.message.guild.roles)
            keyReq = discord.utils.find(lambda r: r.name == '[🌏] World Key', ctx.message.guild.roles)
            heraWeapon = discord.utils.find(lambda r: r.name == "[✨] Godly Scepter", ctx.message.guild.roles)
            weaponDrop = discord.utils.find(lambda r: r.name == "[🌏] Eternal Hamarr", ctx.message.guild.roles)
            # gaiaTitle = discord.utils.find(lambda r: r.name == "[⚔️] Slayer of the Earth", ctx.message.guild.roles)
            logChannel = self.client.get_channel(873941431570546770)

            if rankReq in ctx.author.roles and keyReq in ctx.author.roles:

                bossHP = 225000
                if heraWeapon in ctx.author.roles:
                    dpsMin = 8000  # 16000
                    dpsMax = 10000  # 20000
                    playerHP = 6250  # 5000

                elif weaponDrop in ctx.author.roles:
                    dpsMin = 32000
                    dpsMax = 40000
                    playerHP = 6500

                else:
                    dpsMin = 2000
                    dpsMax = 2500
                    playerHP = 1500

                embed = discord.Embed(
                    title='Jörmungandr',
                    description=f'__**Boss Health**__\n:heart: {bossHP}\n\n__**Player Health**__\n:heart: {playerHP}\n\n__**Difficulty**__\n:star: :star: :star: :star:',
                    colour=discord.Colour.red()
                )

                msg = await ctx.send(embed=embed)
                while bossHP > 0 and playerHP > 0:
                    await asyncio.sleep(1)
                    DPS = random.randint(dpsMin, dpsMax)
                    playerDamage = random.randint(220, 280)
                    bossHP = bossHP - DPS
                    await asyncio.sleep(0.1)
                    playerHP = playerHP - playerDamage

                    embed2 = discord.Embed(
                        title='Jörmungandr',
                        description=f'\n\n__**Boss Health**__\n:heart: {bossHP} *[-{DPS}]*\n\n__**Player Health**__\n:heart: {playerHP} *[-{playerDamage}]*\n\n__**Difficulty**__\n:star: :star: :star: :star:',
                        colour=discord.Colour.red()
                    )
                    await msg.edit(embed=embed2)

                if bossHP <= 0:

                    if playerHP <= 0:
                        if bossHP <= 0:
                            bossHP = 0

                        embed = discord.Embed(
                            title='You have died.',
                            description='The boss killed you before you killed it.',
                            colour=discord.Colour.from_rgb(255, 95, 95)
                        )
                        embed2 = discord.Embed(
                            title='Jörmungandr',
                            description=f'\n\n__**Boss Health**__\n:heart: {bossHP} *[-{DPS}]*\n\n__**Player Health**__\n:heart: 0 *[-{playerDamage}]*\n\n__**Difficulty**__\n:star: :star: :star: :star: :star:',
                            colour=discord.Colour.red()
                        )
                        await ctx.send(f'{ctx.author.mention}')
                        await ctx.send(embed=embed)
                        await ctx.author.remove_roles(keyReq)
                        await msg.edit(embed=embed2)

                    else:
                        l1 = random.choice(boss4_lootTable)
                        l2 = random.choice(boss4_lootTable)
                        l3 = random.choice(boss4_lootTable)
                        embed = discord.Embed(
                            title='Jörmungandr has been defeated',
                            description=f'__**Loot**__\n\n- {l1}\n- {l2}\n- {l3}',
                            colour=discord.Colour.from_rgb(0, 208, 255)
                        )
                        embed2 = discord.Embed(
                            title='Boss Defeated',
                            description=f'{ctx.author.mention} has defeated Jörmungandr.\n \n __**Loot**__\n- {l1}\n- {l2}\n- {l3}',
                            colour=discord.Colour.from_rgb(0, 208, 255)
                        )
                        embed3 = discord.Embed(
                            title='Jörmungandr',
                            description=f'\n\n__**Boss Health**__\n:heart: 0 *[-{DPS}]*\n\n__**Player Health**__\n:heart: {playerHP} *[-{playerDamage}]*\n\n__**Difficulty**__\n:star: :star: :star: :star: :star:',
                            colour=discord.Colour.red()
                        )
                        if l1 == '[ITEM] Eternal Hamarr' or l2 == '[ITEM] Eternal Hamarr' or l3 == '[ITEM] Eternal Hamarr':
                            await ctx.author.add_roles(weaponDrop)

                        await ctx.send(f'{ctx.author.mention}')
                        await ctx.author.remove_roles(keyReq)
                        await logChannel.send(embed=embed2)
                        await ctx.send(embed=embed)
                        await msg.edit(embed=embed3)

                elif playerHP <= 0:

                    embed = discord.Embed(
                        title='You have died.',
                        description='The boss killed you before you killed it.',
                        colour=discord.Colour.from_rgb(255, 95, 95)
                    )
                    embed2 = discord.Embed(
                        title='Jörmungandr',
                        description=f'\n\n__**Boss Health**__\n:heart: {bossHP} *[-{DPS}]*\n\n__**Player Health**__\n:heart: 0 *[-{playerDamage}]*\n\n__**Difficulty**__\n:star: :star: :star: :star: :star:',
                        colour=discord.Colour.red()
                    )
                    await ctx.send(f'{ctx.author.mention}')
                    await ctx.send(embed=embed)
                    await ctx.author.remove_roles(keyReq)
                    await msg.edit(embed=embed2)

        # LIMITED TIME BOSS
        if bossName == 'Asteria' or bossName == 'asteria':

            bossName = "Asteria"
            rankReq = discord.utils.find(lambda r: r.name == '[✦ XV] Worldkeeper', ctx.message.guild.roles)
            keyReq = discord.utils.find(lambda r: r.name == '[✨] Stellar Key', ctx.message.guild.roles)
            heraWeapon = discord.utils.find(lambda r: r.name == "[✨] Godly Scepter", ctx.message.guild.roles)
            jorgWeapon = discord.utils.find(lambda r: r.name == "[🌏] Eternal Hamarr", ctx.message.guild.roles)
            titleDrop = discord.utils.find(lambda r: r.name == "[✨] S11 Celestial Slayer", ctx.message.guild.roles)
            logChannel = self.client.get_channel(873941431570546770)

            if rankReq in ctx.author.roles:  # and keyReq in ctx.author.roles:

                bossHP = 175000
                if heraWeapon in ctx.author.roles:
                    dpsMin = 8000  # 16000
                    dpsMax = 10000  # 20000
                    playerHP = 6250  # 5000

                elif jorgWeapon in ctx.author.roles:
                    dpsMin = 32000
                    dpsMax = 40000
                    playerHP = 6500

                else:
                    dpsMin = 2000
                    dpsMax = 2500
                    playerHP = 1500

                embed = discord.Embed(
                    title='Asteria',
                    #description=f'__**Boss Health**__\n:heart: {bossHP}\n\n__**Player Health**__\n:heart: {playerHP}\n\n__**Difficulty**__\n:star: :star: :star: :star:',
                    colour=discord.Colour.gold()
                )
                embed.add_field(name="Boss Health", value = f":heart: {bossHP}", inline=True)
                embed.add_field(name="Player Health", value = f":heart: {playerHP}", inline=True)
                embed.add_field(name="Last Action", value="`Boss initiated.", inline=False)
                embed.add_field(name="Difficulty", value="star: :star: :star: :star: :star:", inline=False)

                s = 0;
                msg = await ctx.send(embed=embed)
                while bossHP > 0 and playerHP > 0:

                    await asyncio.sleep(1.5)
                    # Setting up Damage
                    DPS = random.randint(dpsMin, dpsMax)
                    playerDamage = random.randint(250, 320)

                    bossHP = bossHP - DPS
                    embed2 = discord.Embed(
                        title='Asteria',
                        #description=f'\n\n__**Boss Health**__\n:heart: {bossHP}\n__**Player Health**__\n:heart: {playerHP}\n\n`- {ctx.author.name} dealt {DPS} damage to the boss!`\n\n__**Difficulty**__\n:star: :star: :star: :star:',
                        colour=discord.Colour.gold()
                    )
                    embed2.add_field(name="Boss Health", value = f":heart: **{bossHP:,}**", inline=True)
                    embed2.add_field(name="Player Health", value = f":heart: **{playerHP:,}**", inline=True)
                    embed2.add_field(name="Last Action", value=f"`- {ctx.author.name} dealt {DPS:,} damage to the boss!`", inline=False)
                    embed2.add_field(name="Difficulty", value=":star: :star: :star: :star: :star:", inline=False)
                    await msg.edit(embed=embed2)

                    await asyncio.sleep(1.5)
                    playerHP = playerHP - playerDamage

                    embed3 = discord.Embed(
                        title='Asteria',
                        #description=f'\n\n__**Boss Health**__\n:heart: {bossHP}\n__**Player Health**__\n:heart: {playerHP}\n\n`- {bossName} dealt {playerDamage} damaged to the player.`\n\n__**Difficulty**__\n:star: :star: :star: :star:',
                        colour=discord.Colour.gold()
                    )
                    embed3.add_field(name="Boss Health", value = f":heart: **{bossHP:,}**", inline=True)
                    embed3.add_field(name="Player Health", value = f":heart: **{playerHP:,}**", inline=True)
                    embed3.add_field(name="Last Action", value=f"`- {bossName} dealt {playerDamage:,} damaged to the player.`", inline=False)
                    embed3.add_field(name="Difficulty", value=":star: :star: :star: :star: :star:", inline=False)
                    await msg.edit(embed=embed3)

                if bossHP <= 0:

                    if playerHP <= 0:
                        if bossHP <= 0:
                            bossHP = 0

                        embed = discord.Embed(
                            title='You have died.',
                            description='The boss killed you before you killed it.',
                            colour=discord.Colour.from_rgb(255, 95, 95)
                        )
                        embed2 = discord.Embed(
                            title='Asteria',
                            description=f'\n\n__**Boss Health**__\n:heart: {bossHP} *[-{DPS}]*\n\n__**Player Health**__\n:heart: 0 *[-{playerDamage}]*\n\n__**Difficulty**__\n:star: :star: :star: :star: :star:',
                            colour=discord.Colour.gold()
                        )
                        await ctx.send(f'{ctx.author.mention}')
                        await ctx.send(embed=embed)
                        await ctx.author.remove_roles(keyReq)
                        await msg.edit(embed=embed2)

                    else:
                        l1 = random.choice(boss5_lootTable)
                        l2 = random.choice(boss5_lootTable)
                        l3 = random.choice(boss5_lootTable)
                        embed = discord.Embed(
                            title='Asteria has been defeated',
                            description=f'__**Loot**__\n\n- {l1}\n- {l2}\n- {l3}',
                            colour=discord.Colour.from_rgb(0, 208, 255)
                        )
                        embed2 = discord.Embed(
                            title='Boss Defeated',
                            description=f'{ctx.author.mention} has defeated Asteria.\n \n __**Loot**__\n- {l1}\n- {l2}\n- {l3}',
                            colour=discord.Colour.from_rgb(0, 208, 255)
                        )
                        embed3 = discord.Embed(
                            title='Asteria',
                            description=f'\n\n__**Boss Health**__\n:heart: 0 *[-{DPS}]*\n\n__**Player Health**__\n:heart: {playerHP} *[-{playerDamage}]*\n\n__**Difficulty**__\n:star: :star: :star: :star: :star:',
                            colour=discord.Colour.red()
                        )
                        if l1 == '[Title] Celestial Slayer' or l2 == '[Title] Celestial Slayer' or l3 == '[Title] Celestial Slayer':
                            await ctx.author.add_roles(titleDrop)

                        await ctx.send(f'{ctx.author.mention}')
                        await ctx.author.remove_roles(keyReq)
                        await logChannel.send(embed=embed2)
                        await ctx.send(embed=embed)
                        await msg.edit(embed=embed3)

                elif playerHP <= 0:

                    embed = discord.Embed(
                        title='You have died.',
                        description='The boss killed you before you killed it.',
                        colour=discord.Colour.from_rgb(255, 95, 95)
                    )
                    embed2 = discord.Embed(
                        title='Jörmungandr',
                        description=f'\n\n__**Boss Health**__\n:heart: {bossHP} *[-{DPS}]*\n\n__**Player Health**__\n:heart: 0 *[-{playerDamage}]*\n\n__**Difficulty**__\n:star: :star: :star: :star: :star:',
                        colour=discord.Colour.red()
                    )
                    await ctx.send(f'{ctx.author.mention}')
                    await ctx.send(embed=embed)
                    await ctx.author.remove_roles(keyReq)
                    await msg.edit(embed=embed2)
    @boss.error
    async def boss_error(self, ctx: commands.Context, error: commands.CommandError):

        if isinstance(error, commands.CommandOnCooldown):
            remaining_time = str(datetime.timedelta(seconds=int(error.retry_after)))
            embed = discord.Embed(
                title='Boss Cooldown',
                description=f'Woah, slow down! You can only attempt to fight this boss every **10 minutes**. Try again in **{remaining_time}** minutes!',
                colour=discord.Colour.from_rgb(0, 208, 255)
            )
            await ctx.send(embed=embed)

    @commands.command()
    async def bosstest(self, ctx):

        x = 5
        if x == 5:
            bossHP = 1200000
            playerHP = 5000
            embed = discord.Embed(
                title='Hera',
                description=f'__**Boss Health**__\n:heart: {bossHP}\n\n__**Player Health**__\n:heart: {playerHP}\n\n__**Difficulty**__\n:star: :star: :star: :star: :star:',
                colour=discord.Colour.red()
            )

            msg = await ctx.send(embed=embed)
            while bossHP > 0 and playerHP > 0:
                await asyncio.sleep(1)
                DPS = random.randint(1000, 15000)
                playerDamage = random.randint(800, 1500)
                bossHP = bossHP - DPS

                await asyncio.sleep(0.1)
                playerHP = playerHP - playerDamage

                embed2 = discord.Embed(
                    title='Testing Boss',
                    description=f'\n\n__**Boss Health**__\n:heart: {bossHP} *[-{DPS}]*\n\n__**Player Health**__\n:heart: {playerHP} *[-{playerDamage}]*\n\n__**Difficulty**__\n:star: :star: :star: :star: :star: :star:',
                    colour=discord.Colour.red()
                )

                await msg.edit(embed=embed2)

            if playerHP <= 0:
                embed = discord.Embed(
                    title='You have died.',
                    description='The boss killed you before you killed it.',
                    colour=discord.Colour.from_rgb(255, 95, 95)
                )
                await ctx.send(f'{ctx.author.mention}')
                await ctx.send(embed=embed)

    @commands.command(aliases=['bosses'])
    async def bosslist(self, ctx):

        embed = discord.Embed(
            title='Boss List - Season 11',
            description='Bosses can only be fought every 10 minutes, considering you have the right requirements.\n\n__**Gaia**__\n\n - <@&867386940403875851>\n- <@&867386933931016243>\n\n__**Aithusa**__\n\n - <@&873806680008310847>\n - <@&870554289762877500>\n - <@&873806689655214140>',
            colour=discord.Colour.from_rgb(0, 208, 255)
        )

        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def getrewards(self, ctx, boss):

        if boss == "Kraken" or boss == "kraken":
            l1 = random.choice(boss1_lootTable)
            l2 = random.choice(boss1_lootTable)
            l3 = random.choice(boss1_lootTable)
            embed = discord.Embed(
                title='Kraken Loot',
                description=f'__**Loot**__\n\n- {l1}\n- {l2}\n- {l3}',
                colour=discord.Colour.from_rgb(0, 208, 255)
            )
            await ctx.send(embed=embed)

        if boss == 'gorgon' or boss == 'Gorgon':
            l1 = random.choice(boss2_lootTable)
            l2 = random.choice(boss2_lootTable)
            l3 = random.choice(boss2_lootTable)
            embed = discord.Embed(
                title='Gorgon Loot',
                description=f'__**Loot**__\n\n- {l1}\n- {l2}\n- {l3}',
                colour=discord.Colour.from_rgb(0, 208, 255)
            )
            await ctx.send(embed=embed)

        if boss == "Hera" or boss == "hera":
            l1 = random.choice(boss3_lootTable)
            l2 = random.choice(boss3_lootTable)
            l3 = random.choice(boss3_lootTable)
            embed = discord.Embed(
                title='Hera Loot',
                description=f'__**Loot**__\n\n- {l1}\n- {l2}\n- {l3}',
                colour=discord.Colour.from_rgb(0, 208, 255)
            )
            await ctx.send(embed=embed)

        if boss == "Serpent" or boss == "serpent":
            l1 = random.choice(boss4_lootTable)
            l2 = random.choice(boss4_lootTable)
            l3 = random.choice(boss4_lootTable)
            embed = discord.Embed(
                title='Serpent Loot',
                description=f'__**Loot**__\n\n- {l1}\n- {l2}\n- {l3}',
                colour=discord.Colour.from_rgb(0, 208, 255)
            )
            await ctx.send(embed=embed)

        if boss == "Asteria" or boss == "asteria":
            l1 = random.choice(boss5_lootTable)
            l2 = random.choice(boss5_lootTable)
            l3 = random.choice(boss5_lootTable)
            embed = discord.Embed(
                description = f"__**Loot**__\n\n- {l1}\n- {l2}\n- {l3}",
                colour = discord.Colour.from_rgb(0, 208, 255)
            )
            await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Boss(client))