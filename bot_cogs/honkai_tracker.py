from discord.ext import commands
from discord.ext.commands import Bot
from bot_ui.reg import ask_in_game_uid
from bot.conf import bot_bridge
import discord

class tester(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.slash_command(name="register", guild_ids=bot_bridge.allowed_servers)
    async def register(self, ctx):
        await ask_in_game_uid(ctx)
    
    @commands.slash_command(name="unbind", guild_ids=bot_bridge.allowed_servers)
    async def unbind(self, ctx, user : discord.User):
        bot_bridge._honkai_tracker.remove_member_by_attr("discord_id", user.id)
        embed = discord.Embed(title="User Unbinded", description="Unbinded {}".format(user.mention))
        await ctx.send(embed=embed)
        bot_bridge._honkai_tracker.save()

def setup(bot):
    bot.add_cog(tester(bot))