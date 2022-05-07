
import logging
from pprint import pprint
from random import choices
from discord.ext import commands
from discord.ext.commands import Bot
from discord import Option

from bot.conf import ArmandaMember
from bot.conf import bot_bridge
import discord
from honkaiDex import BaseCharacter, Battlesuit, StigamataSet

class NotRegisteredError(Exception):pass

class honkai_wiki_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # cog check
    def cog_check(self, ctx):
        member : ArmandaMember = ArmandaMember.get(discord_id=ctx.author.id)
        if member is None:
            raise NotRegisteredError()

    async def cog_command_error(self, ctx, error):
        if isinstance(error, NotRegisteredError):
            embed = discord.Embed(title="Error", description="You are not registered")
            await ctx.respond(embed=embed)
        else:
            pprint(error)

    async def send_character_embed(self, ctx, character : BaseCharacter):
        embed = discord.Embed(title=f"{character.name} Lookup", description=f"by {ctx.author.mention}")
        embed.add_field(name="Nickname", value=character.nickname)
        return await ctx.respond(embed=embed)

    @commands.slash_command(
        name="wiki-character", 
        guild_ids=bot_bridge.allowed_servers,
        description="Lookup a character"
    )
    async def wiki_character(self, ctx : discord.ApplicationContext, query : str):
        result : set = BaseCharacter.fuzzy_match_nicknames(query)[0]
        val = result[1]
        character : BaseCharacter = result[0]
        if val >= 98:
            return await self.send_character_embed(ctx, character)

        result : set = BaseCharacter.fuzzy_match_names(query)[0]
        val = result[1]
        character : BaseCharacter = result[0]
        if val > 80:
            return await self.send_character_embed(ctx, character)


        embed = discord.Embed(title="Error", description="Character not found")
        return await ctx.respond(embed=embed)
    
    async def send_battlesuit_embed(self, ctx, battlesuit : Battlesuit):
        embed = discord.Embed(title=f"{battlesuit.name} Lookup", description=f"by {ctx.author.mention}")
        embed.add_field(name="Nickname", value=", ".join(battlesuit.nickname))
        embed.add_field(name="Rarity", value=battlesuit.rarity)
        embed.add_field(name="Version Released", value=battlesuit.version_released)
        tags = "" if battlesuit.tags is None else ", ".join(battlesuit.tags)
        embed.add_field(name="Tags", value=tags)
        embed.add_field(name="Character", value=battlesuit.base_character.name)
        if (battlesuit.img_link is not None):
            embed.set_thumbnail(url=battlesuit.img_link)
        
        return await ctx.respond(embed=embed)

    @commands.slash_command(
        name="wiki-battlesuit",
        guild_ids=bot_bridge.allowed_servers,
        description="Lookup a battlesuit"
    )
    async def wiki_battlesuit(self, ctx : discord.ApplicationContext, query : str):
        res : set = Battlesuit.fuzzy_match_nicknames(query)[0]
        val = res[1]
        battlesuit : Battlesuit = res[0]
        if val >= 90:
            return await self.send_battlesuit_embed(ctx, battlesuit)

        res : set = Battlesuit.fuzzy_match_names(query)[0]
        battlesuit : Battlesuit = res[0]
        pprint(battlesuit)
        if res[1] > 80:
            return await self.send_battlesuit_embed(ctx, battlesuit)

        
        embed = discord.Embed(title="Error", description="Battlesuit not found")
        return await ctx.respond(embed=embed)


    async def send_stigamata_embed(self, ctx, stigamata : StigamataSet, pos : str):
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
        res : set =  StigamataSet.fuzzy_match_names(query)[0]
        stigamata : StigamataSet = res[0]
        if res[1] >= 90:
            return await self.send_stigamata_embed(ctx, stigamata, pos)

        embed = discord.Embed(title="Error", description="Stigamata not found")
        return await ctx.respond(embed=embed)


def setup(bot):
    bot.add_cog(honkai_wiki_cog(bot))