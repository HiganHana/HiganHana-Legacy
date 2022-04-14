from pprint import pformat
from discord.ext import commands
from discord.ext.commands import Bot
from bot.conf import bot_bridge
import discord
from discord.interactions import InteractionResponse
from bot_ui.reg import uid_form

class cog_debug(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name="dump_tracker")
    @commands.has_guild_permissions(administrator=True)
    async def dump_tracker(self, ctx):
        await ctx.send(f"""```
{pformat(bot_bridge._honkai_tracker.__real_data__)}
```""")

def setup(bot):
    bot.add_cog(cog_debug(bot))