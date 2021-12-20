import animec
import datetime
import nextcord as discord
from nextcord.ext import commands

#---------------------COG SETUP---------------------#

class Anime(commands.Cog):
    
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def anime(self, ctx, *, query):

        try:
            anime = animec.Anime(query)
        except:
            embed = discord.Embed(
                description = "Could not find any anime matching your search query.",
                colour = discord.Colour.from_rgb(255, 75, 75)
            )
            embed.set_author(name = "Anime Command", url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
            return
            
        embed = discord.Embed(
            title = anime.title_english,
            url = anime.url,
            description = f"{anime.description[:200]}...",
            colour = discord.Colour.from_rgb(0, 208, 255)
        )

        embed.add_field(name="Episodes", value=str(anime.episodes))
        embed.add_field(name="Rating", value=str(anime.rating))
        embed.add_field(name="Broadcast", value=str(anime.broadcast))
        embed.add_field(name="Status", value=str(anime.status))
        embed.add_field(name="Type", value=str(anime.type))
        embed.add_field(name="NSFW Status", value=str(anime.is_nsfw()))
        embed.set_thumbnail(url = anime.poster)
        await ctx.send(embed=embed)

    @commands.command(aliases = ["char", "animecharacter", "animechar"])
    async def character(self, ctx, *, query):

        try:
            char = animec.Charsearch(query)
        except:
            embed = discord.Embed(
                description = "Could not find an anime character matching your search",
                colour = discord.Colour.from_rgb(0, 208, 255)
            )
            await ctx.send(embed=embed)

        embed = discord.Embed(
            title = char.title,
            url = char.url,
            colour = discord.Colour.random()
        )
        embed.set_image(url = char.image_url)
        embed.set_footer(text = ", ".join(list(char.references.keys())[:2]))
        await ctx.send(embed=embed)

    @commands.command()
    async def aninews(self, ctx, amount: int=3):
        news = animec.Aninews(amount)
        links = news.links
        titles = news.titles
        descriptions = news.description

        embed = discord.Embed(
            title = "Latest Anime News",
            colour = discord.Colour.random(),
            timestamp = datetime.datetime.utcnow()
        )
        embed.set_thumbnail(url=news.images[0])

        for i in range(amount):
            embed.add_field(name = f"{i+1}) {titles[i]}", value = f"{descriptions[i][:200]}...\n[Read More]({links[i]})", inline=False)

        await ctx.send(embed=embed)

#---------------------CLIENT---------------------#

def setup(client):
    client.add_cog(Anime(client))