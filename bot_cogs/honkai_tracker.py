
from pprint import pprint
from discord.ext import commands
from discord.ext.commands import Bot
from bot.conf import ArmandaMember
from bot.conf import bot_bridge
import discord
from discord.utils import get
from bot.funcs import has_roles
from zxutil.umodel import U_ValidationError

class cog_tracker(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name="register", 
        guild_ids=bot_bridge.allowed_servers,
        description="Register your honkai profile",
        
    )
    async def register(self, ctx, uid : int, lv : int, genshin_id = None):
        #ires : InteractionResponse = ctx.interaction.response

        if ctx.author.id in ArmandaMember.yield_field("discord_id"):
            embed = discord.Embed(title="Error", description="You are already registered")
            
            return await ctx.respond(embed=embed)

        if not has_roles(ctx, "Impact Member"):
            embed = discord.Embed(title="Error", description="You are not Impact Member")
            return await ctx.respond(embed=embed)

        try:
            member = ArmandaMember(
                discord_id=ctx.author.id,
                uid=uid,
                lv=lv,
                genshin_id=genshin_id
            )
            member.export_this(bot_bridge.ARMANDA_JSON)
        except U_ValidationError as e:
            e : U_ValidationError
            embed = discord.Embed(title="Error", description=e)
            return await ctx.respond(embed=embed)

        #invoke lookup
        await ctx.invoke(self.lookup, uid=uid)
            

        """form = uid_form()

        await ires.send_modal(form)"""
        
    @commands.slash_command(
        name="unbind",
        guild_ids=bot_bridge.allowed_servers,
        description="Unbind honkai profile (admin, mod)"
    )
    @commands.has_any_role("Impact Vice Leader", "Impact Leader")
    async def unbind(self, ctx, user : discord.User):
        member : ArmandaMember = ArmandaMember.get(discord_id=user.id)
        if member is None:
            embed = discord.Embed(title="Error", description="You are not registered")
            return await ctx.respond(embed=embed)
        
        ArmandaMember.remove_this(member)
        
        ArmandaMember.export_all(bot_bridge.ARMANDA_JSON, replace=True)
        embed = discord.Embed(title="User Unbinded", description="Unbinded {}".format(user.mention))
        await ctx.respond(embed=embed)
        

    @commands.slash_command(
        name="lookup", 
        guild_ids=bot_bridge.allowed_servers,
        description="Lookup honkai profile"
    )
    async def lookup(self, ctx : discord.ApplicationContext, user : discord.User = None, uid : int = None):
        if user is None and uid is None:
            user = ctx.author
        
        if user is not None:
            member : ArmandaMember = ArmandaMember.get(discord_id=user.id)
        
            if member is None:
                embed = discord.Embed(title="Error", description="User not registered")
                return await ctx.respond(embed=embed)

            username = user.display_name
        else:
            member : ArmandaMember = ArmandaMember.get(uid=uid)

            if member is None:
                embed = discord.Embed(title="Error", description="User not found")
                return await ctx.respond(embed=embed)

            username = member.uid
            if get(ctx.guild.members, id=member.discord_id) is not None:
                username = get(ctx.guild.members, id=member.discord_id).display_name
            
        embed = discord.Embed(title=f"{username} Lookup", description=f"by {ctx.author.mention}")
        
        embed.add_field(name="uid", value=member.uid)
        embed.add_field(name="lv", value=member.lv)
        if member.genshin_id is not None:
            embed.add_field(name="Genshin ID", value=member.genshin_id)
        
        return await ctx.respond(embed=embed)
    
    def _update(self,member : ArmandaMember,  **kwargs):
        """
        this method drops all none values from kwargs and perform update ArmandaMember
        """
        if len(kwargs) == 0:
            return

        kwargs = {k:v for k,v in kwargs.items() if v is not None}
        
        member.update(**kwargs)

    @commands.slash_command(
        name="update", 
        guild_ids=bot_bridge.allowed_servers,
        description="Update honkai profile"
    )
    @commands.cooldown(5,60, commands.BucketType.guild)
    async def update(
        self, 
        ctx : discord.ApplicationContext, 
        lv : int = None, 
        genshin_id : int =None,
        other_user : discord.User = None

    ):
        if other_user is None:
            user = ctx.author
        else:
            user = other_user
        
        # check permissions
        if other_user and not has_roles(ctx, *bot_bridge.MOD_ROLES):
            embed = discord.Embed(title="Error", description="You don't have permission to update other users")
            return await ctx.respond(embed=embed)

        # check if user is registered
        member : ArmandaMember = ArmandaMember.get(discord_id=user.id)
        if member is None:
            embed = discord.Embed(title="Error", description="User not registered")
            return await ctx.respond(embed=embed)

        try:
            self._update(member, lv=lv, genshin_id=genshin_id)
        except U_ValidationError as e:
            e : U_ValidationError
            embed = discord.Embed(title="Error", description=f"{e}")
            return await ctx.respond(embed=embed)

        member.export(bot_bridge.ARMANDA_JSON, update_=True)

        await ctx.invoke(self.lookup, user=user)

    @update.error
    async def update_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(title="Error", description="Guild on cooldown")
            await ctx.respond(embed=embed)

def setup(bot):
    bot.add_cog(cog_tracker(bot))