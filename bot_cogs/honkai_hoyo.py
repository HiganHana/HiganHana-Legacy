import json
import logging
from pprint import pformat, pprint
from unittest import result
from discord.ext import commands
from discord.ext.commands import Bot
from bot.tracker import ArmandaMember
from bot.conf import bot_bridge
import discord
from discord.interactions import InteractionResponse
from bot_ui.reg import uid_form
from discord.utils import get
from bot import batch_download, has_roles, download_image_from_url, combine_image
from honkaiDex.game import valid_lv
from genshin import Client
from genshin.models.honkai import FullBattlesuit, Stigma
from honkaiDex import Battlesuit
import logging
import os
logging.getLogger().setLevel(logging.INFO)

class honkai_hoyo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        cookies = {
            "ltuid" : bot_bridge.ltuid,
            "ltoken" : bot_bridge.ltoken,
        }
        self.hoyoclient = Client(cookies=cookies)

    @commands.slash_command(name="hoyo_valk", description="Get hoyolab character")
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.has_any_role(*bot_bridge.MOD_ROLES)
    async def hoyop(self, ctx : discord.ApplicationContext, user : discord.User, battlesuit_name : str):
        battlesuit_name = battlesuit_name.lower().strip()
        # check valid battlesuit
        bs : Battlesuit = Battlesuit.get_from_name(battlesuit_name, nick=True)
        if bs is None:
            bs : Battlesuit = Battlesuit.get_from_name(battlesuit_name,partial=True, nick=True)

        if bs is None:
            embed = discord.Embed(title="Error", description="battlesuit name not found")
            return await ctx.respond(embed=embed)

        logging.info(bs)

        # * check if user is registered
        member : ArmandaMember = bot_bridge._honkai_tracker.get_one(discord_id=ctx.author.id)
        if member is None:
            embed = discord.Embed(title="Error", description="You are not registered")
            return await ctx.respond(embed=embed)
        
        # * check if user is registered
        user_member : ArmandaMember = bot_bridge._honkai_tracker.get_one(discord_id=user.id)
        if user_member is None:
            embed = discord.Embed(title="Error", description="The target you are looking for is not registered")
            return await ctx.respond(embed=embed)
    
        try:
            results = await self.hoyoclient.get_honkai_battlesuits(user_member.uid)
        except Exception as e:
            logging.error(e.message)

            embed = discord.Embed(title="Error", description="Failed to get honkai profile")
            embed.add_field(name="log", value=pformat(e))
            return await ctx.respond(embed=embed)
        
        lbs = None

        for res in results:
            if battlesuit_name == res.name.lower().strip():
                lbs = res
                res : FullBattlesuit
                break
            if res.name in bs.all_names:
                lbs = res
                res : FullBattlesuit
                break
        
        if lbs is None:
            for res in results:
                if res.name in bs.name.lower().strip():
                    lbs = res
                    res : FullBattlesuit
                    break
                if battlesuit_name in res.name.lower().strip():
                    lbs = res
                    res : FullBattlesuit
                    break

        if lbs is None:
            embed = discord.Embed(title="Info", description="User does not have this battlesuit")
            return await ctx.respond(embed=embed)

        embed = discord.Embed(
            title=f"{user.display_name}'s {lbs.name} {lbs.rank}",
            description=f"{user.mention}"
        )
        embed.add_field(name="Weapon", value=lbs.weapon.name)
        POS = ["T", "M", "B"]
        for i, stig in enumerate(lbs.stigmata):
            embed.add_field(name=f"Stigma {POS[i]}", value=stig.name)

        embed.set_thumbnail(url=lbs.icon)
        download_image_from_url(lbs.weapon.icon, f"{lbs.weapon.name}_{lbs.weapon.id}")
        stig_file_names = {f"{k.name}_{k.id}" : k.icon for k in lbs.stigmata if k is not None}

        batch_download(**stig_file_names)

        combined, save_path = combine_image(f"{lbs.weapon.name}_{lbs.weapon.id}", *stig_file_names.keys())
        if save_path is None:
            embed.add_field(name="Error", value="Failed to load images")

        file = discord.File(save_path, filename="image.png")
        embed.set_image(url="attachment://image.png")
        await ctx.respond(embed=embed, file=file)

        #send

        

        

def setup(bot):
    bot.add_cog(honkai_hoyo(bot))