
from random import choices
from discord.ext import commands
from discord.ext.commands import Bot
from bot.tracker import ArmandaMember
from bot.conf import bot_bridge
import discord
from discord.commands import Option
from honkaiDex import BaseCharacter, Battlesuit, StigamataSet

class NotRegisteredError(Exception):pass

class honkai_wiki_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # cog check
    def cog_check(self, ctx):
        member : ArmandaMember = bot_bridge._honkai_tracker.get_one(discord_id=ctx.author.id)
        if member is None:
            raise NotRegisteredError()

    async def cog_command_error(self, ctx, error):
        if isinstance(error, NotRegisteredError):
            embed = discord.Embed(title="Error", description="You are not registered")
            await ctx.respond(embed=embed)

    @commands.slash_command(
        name="wiki-character", 
        guild_ids=bot_bridge.allowed_servers,
        description="Lookup a character"
    )
    async def wiki_character(self, ctx : discord.ApplicationContext, query : str):
        character : BaseCharacter = BaseCharacter.get_from_name(query, partial=True, nick=True)
        if character is None:
            embed = discord.Embed(title="Error", description="Character not found")
            return await ctx.respond(embed=embed)
    
        embed = discord.Embed(title=f"{character.name} Lookup", description=f"by {ctx.author.mention}")
        embed.add_field(name="Nickname", value=character.nickname)
        
        return await ctx.respond(embed=embed)

    @commands.slash_command(
        name="wiki-battlesuit",
        guild_ids=bot_bridge.allowed_servers,
        description="Lookup a battlesuit"
    )
    async def wiki_battlesuit(self, ctx : discord.ApplicationContext, query : str):
        battlesuit : Battlesuit = Battlesuit.get_from_name(query, partial=True, nick=True)
        if battlesuit is None:
            embed = discord.Embed(title="Error", description="Battlesuit not found")
            return await ctx.respond(embed=embed)
    
        embed = discord.Embed(title=f"{battlesuit.name} Lookup", description=f"by {ctx.author.mention}")
        embed.add_field(name="Nickname", value=", ".join(battlesuit.nickname))
        embed.add_field(name="Rarity", value=battlesuit.rarity)
        embed.add_field(name="Version Released", value=battlesuit.version_released)
        tags = "" if battlesuit.tags is None else ", ".join(battlesuit.tags)
        embed.add_field(name="Tags", value=tags)

        if (battlesuit.img_link is not None):
            embed.set_thumbnail(url=battlesuit.img_link)
        
        return await ctx.respond(embed=embed)

    @commands.slash_command(
        name="wiki-stigamata",
        guild_ids=bot_bridge.allowed_servers,
        description="Lookup a stigamata"
    )
    async def wiki_stigamata(
        self, ctx : discord.ApplicationContext, 
        query : str, 
        pos:Option(str, choices=["T", "M", "B"])
    ):
        stigamata : StigamataSet = StigamataSet.get_from_name(query, partial=True, nick=True)
        if stigamata is None:
            embed = discord.Embed(title="Error", description="Stigamata not found")
            return await ctx.respond(embed=embed)
    
        embed = discord.Embed(title=f"{stigamata.name} ({pos}) Lookup", description=f"by {ctx.author.mention}")
        
        if pos == "T":
            stig = stigamata.top
        elif pos == "M":
            stig = stigamata.middle
        elif pos == "B":
            stig = stigamata.bottom

        if (stig.img is not None):
            embed.set_image(url=stig.img)

        embed.add_field(name="Effect", value=stig.effect)
        return await ctx.respond(embed=embed)
        
def setup(bot):
    bot.add_cog(honkai_wiki_cog(bot))