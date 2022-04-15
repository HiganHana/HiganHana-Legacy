
from discord.ext import commands
from discord.ext.commands import Bot
from alib.tracker import HonkaiMember
from bot.conf import bot_bridge
import discord
from discord.interactions import InteractionResponse
from bot_ui.reg import uid_form
from discord.utils import get
from alib.dbot import has_roles
from honkai import valid_lv

class cog_tracker(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.slash_command(
        name="register", 
        guild_ids=bot_bridge.allowed_servers,
        description="Register your honkai profile",
        
    )
    async def register(self, ctx):
        ires : InteractionResponse = ctx.interaction.response

        if ctx.author.id in bot_bridge._honkai_tracker.get_field_generator("discord_id"):
            embed = discord.Embed(title="Error", description="You are already registered")
            
            return await ires.send_message(embed=embed)

        form = uid_form()

        await ires.send_modal(form)
        
    @commands.slash_command(
        name="unbind",
        guild_ids=bot_bridge.allowed_servers,
        description="Unbind honkai profile (admin, mod)"
    )
    @commands.has_any_role("Impact Vice Leader", "Impact Leader")
    async def unbind(self, ctx, user : discord.User):
        if bot_bridge._honkai_tracker.remove_member_by_attr("discord_id", user.id):
            bot_bridge._honkai_tracker.save()
        embed = discord.Embed(title="User Unbinded", description="Unbinded {}".format(user.mention))
        ires : InteractionResponse = ctx.interaction.response
        await ires.send_message(embed=embed)
        

    @commands.slash_command(
        name="lookup", 
        guild_ids=bot_bridge.allowed_servers,
        description="Lookup honkai profile"
    )
    async def lookup(self, ctx : discord.ApplicationContext, user : discord.User = None, uid : int = None):
        ires : InteractionResponse = ctx.interaction.response
        if user is None and uid is None:
            user = ctx.author
        
        if user is not None:
            member : HonkaiMember = bot_bridge._honkai_tracker.get_member(discord_id=user.id)
        
            if member is None:
                embed = discord.Embed(title="Error", description="User not registered")
                return await ires.send_message(embed=embed)

            username = user.name
        else:
            member : HonkaiMember = bot_bridge._honkai_tracker.get_member(uid=uid)

            if member is None:
                embed = discord.Embed(title="Error", description="User not found")
                return await ires.send_message(embed=embed)

            username = member.uid
            if get(ctx.guild.members, id=member.discord_id) is not None:
                username = get(ctx.guild.members, id=member.discord_id).name
            
        embed = discord.Embed(title=f"{username} Lookup", description=f"by {ctx.author.mention}")
        
        embed.add_field(name="uid", value=member.uid)
        embed.add_field(name="lv", value=member.lv)
        
        return await ires.send_message(embed=embed)
    
    @commands.slash_command(
        name="update", 
        guild_ids=bot_bridge.allowed_servers,
        description="Update honkai profile"
    )
    @commands.cooldown(1, 120, commands.BucketType.user)

    async def updateinfo(self, ctx : discord.ApplicationContext, lv : int = None, other_user : discord.User = None, **kwargs):

        print(kwargs)

        ires : InteractionResponse = ctx.interaction.response
        if other_user is None:
            user = ctx.author
        else:
            user = other_user
        
        # check permissions
        if other_user and not has_roles(ctx, *bot_bridge.MOD_ROLES):
            embed = discord.Embed(title="Error", description="You don't have permission to update other users")
            return await ires.send_message(embed=embed)

        # check if user is registered
        member : HonkaiMember = bot_bridge._honkai_tracker.get_member(discord_id=user.id)
        if member is None:
            embed = discord.Embed(title="Error", description="User not registered")
            return await ires.send_message(embed=embed)

        member_dict = member.to_dict()

        member.update(
            lv=(valid_lv, lv),
        )

        if not bot_bridge._honkai_tracker.is_changed():
            embed = discord.Embed(title="User Update", description="No changes made to {}".format(user.mention))
            return await ires.send_message(embed=embed)


        bot_bridge._honkai_tracker.save()
        embed = discord.Embed(title="User Update", description="Updated {}".format(user.mention))
        
        for var in member.generate_keywords_var():
            if(member_dict[var[0]] != var[1]):
                embed.add_field(name=var[0], value=f"{member_dict[var[0]]} -> {var[1]}", inline=False)

        return await ires.send_message(embed=embed)
    
    @updateinfo.error
    async def update_error(self, ctx, error):
        #
        if isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(title="Error", description="You are on cooldown", color=0xFF0000)
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(cog_tracker(bot))