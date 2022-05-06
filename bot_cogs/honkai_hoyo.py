import logging
from pprint import pformat
from typing import Sequence
from discord.ext import commands
from bot.conf import bot_bridge
import discord
from discord.utils import get
from genshin import Client
from genshin.models.honkai import FullBattlesuit
from fuzzywuzzy import process
from honkaiDex import Battlesuit
import logging
from zxutil.FUNCS.img import combine_linear_image

def get_combined_name(*args):
    if len(args) == 0:
        return None
   
    pend_name = ""
    for i, arg in enumerate(args):
        if arg is None:
            pend_name += "0."
            continue
        pend_name += str(arg) + "."
    
    return pend_name[:-1]

import bot.funcs as botfunc
import random
class honkai_hoyo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
        self.hoyoclient : Client = bot_bridge._hoyoclient

    async def get_battlesuits(self, ctx : discord.ApplicationContext, uid : int) -> Sequence[FullBattlesuit]:
        try:
            results = await self.hoyoclient.get_honkai_battlesuits(int(uid))
            return results
        except Exception as e:
            logging.error(e)

            embed = discord.Embed(title="Error", description="Failed to get honkai profile")
            embed.add_field(name="log", value=pformat(e))
            await ctx.respond(embed=embed)
            return None
    
    def create_owned_list(self, battlesuits : Sequence[FullBattlesuit]):
        owned_list = []
        random.shuffle(battlesuits)
        for i, battlesuit in enumerate(battlesuits):
            if i >= 8:
                break
            owned_list.append(battlesuit)
        return owned_list

    def create_owned_str_list(self, battlesuits: Sequence[FullBattlesuit]):
        battlesuits = self.create_owned_list(battlesuits)
        owned_str = ""
        for i, battlesuit in enumerate(battlesuits):
            owned_str += f"{battlesuit.id} `{battlesuit.name} ({battlesuit.rank})`\n"
        return owned_str
        
    def query_battlesuits_by_id(self, battlesuits : Sequence[FullBattlesuit], id : int) -> FullBattlesuit:
        for battlesuit in battlesuits:
            if battlesuit.id == id:
                return battlesuit
        return None

    def query_battlesuits_by_name(self, battlesuits : Sequence[FullBattlesuit], name : str) -> FullBattlesuit:
        name = name.lower().strip()
        battlesuits :dict = {k.name : k for k in battlesuits }

        # nickname check
        nickname_res = None
        if " " not in name and len(name) < 10:
            for x in Battlesuit.iterate():
                x : Battlesuit
                for ni in x.nickname:
                    if name == ni.lower():
                        nickname_res = x

        # fuzzy matching nickname
        if nickname_res is not None:
            result = process.extractOne(nickname_res.name, battlesuits.keys())
            if result[1] > 90:
                bs_name = result[0]
                return battlesuits[bs_name]

        # fuzzy matching
        result = process.extractOne(name, battlesuits.keys())
        if result[1] > 80:
            bs_name = result[0]
            return battlesuits[bs_name]

        return None

    @commands.slash_command(name="hoyo_valk", description="Get hoyolab character")
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.has_any_role(*bot_bridge.MOD_ROLES, *bot_bridge.BOOSTER_PLAN, *bot_bridge.IMPACT_MEMBER)
    async def hoyop(self, ctx : discord.ApplicationContext, user : discord.User, battlesuit_name : str =None):
        if battlesuit_name is not None and not isinstance(battlesuit_name, str):
            embed = discord.Embed(title="Error", description="UNKNOWN ERROR, battlesuit_name is not a string")
            await ctx.respond(embed=embed)
            return

        if  (member :=  await botfunc.check_author_registered(ctx)) is None: return
            
        if (user_member :=  await botfunc.check_user_registered(ctx, user)) is None: return
    
        battlesuits = await self.get_battlesuits(ctx, user_member.uid)

        # when there is no query for battlesuit name
        if battlesuit_name is None:
            owned_lists = self.create_owned_list(battlesuits)
            embed = discord.Embed(title="Honkai hoyo", description="Select a battlesuit by name/id")

            for owned in owned_lists:
                owned : FullBattlesuit
                embed.add_field(name=f"{owned.name} ({owned.character})", value=f"id `{owned.id}` rank `{owned.rank}`", inline=False)
            return await ctx.respond(embed=embed)
        
        
        # when there is a query for battlesuit name
        # and is int
        battlesuit = None
        if battlesuit_name.isdigit() and (battlesuit := self.query_battlesuits_by_id(battlesuits, int(battlesuit_name))) is None:
            embed = discord.Embed(title="Error", description="Battlesuit not found")
            embed.add_field(name="Owned", value=self.create_owned_str_list(battlesuits))
            return await ctx.respond(embed=embed)
        
        if battlesuit is None:
            battlesuit = self.query_battlesuits_by_name(battlesuits, battlesuit_name)
        
        if battlesuit is None:
            embed = discord.Embed(title="Error", description="Battlesuit not found")
            embed.add_field(name="Owned", value=self.create_owned_str_list(battlesuits))
            return await ctx.respond(embed=embed)

        # create profile
        embed = discord.Embed(
            title=f"{user.display_name}'s {battlesuit.name} {battlesuit.rank}",
            description=f"loading...{user.mention}"
        )
        await ctx.respond(embed=embed)

        # download image
        # weapon
        profile_embed = discord.Embed(
            title=f"{user.display_name}'s {battlesuit.name} {battlesuit.rank}",
            description=f"{user.mention}",
            color=0x00ff00
        )

        images = [(None, None), (None, None), (None, None), (None, None)]
        if battlesuit.weapon is not None:
            profile_embed.add_field(name="Weapon", value=battlesuit.weapon.name)

            bot_bridge._pulled_cacher.save(
                key=battlesuit.weapon.id,
                link=battlesuit.weapon.icon
            )
            images[0] = (bot_bridge._pulled_cacher.load(battlesuit.weapon.id), battlesuit.weapon.id)

        stig_pos =["T", "M", "B"]

        stigs = battlesuit.stigmata
        if stigs is not None:
            for i, stig in enumerate(battlesuit.stigmata):
                bot_bridge._pulled_cacher.save(
                    key=stig.id, link=stig.icon
                )        
                images[i+1] = (bot_bridge._pulled_cacher.load(stig.id), stig.id)

                # profile embed
                profile_embed.add_field(name=f"Stigmata {stig_pos[i]}", value=stig.name)
        else:
            stigs = []
        #
        # if only weapon
        if all(x is None for x in images[1:]):
            profile_embed.set_image(url=battlesuit.weapon.icon)
            profile_embed.add_field(name="Weapon", value=battlesuit.weapon.name)
            await ctx.channel.send(embed=profile_embed)

        img_names  = [x[1] for x in images]
        combined_name = get_combined_name(*img_names)

        if combined_name not in bot_bridge._merged_cacher:
            print("Recreating merged image")
            combined_img, combined_name = combine_linear_image("128x128", *images)
            bot_bridge._merged_cacher.save(
                obj=combined_img,
                key=combined_name
            )
    

        file = discord.File(bot_bridge._merged_cacher.get_path(combined_name), filename="image.png")
        profile_embed.set_image(url="attachment://image.png")
        await ctx.channel.send(embed=profile_embed, file=file)

def setup(bot):
    bot.add_cog(honkai_hoyo(bot))