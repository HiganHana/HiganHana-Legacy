from pprint import pformat
from discord.ext import commands
from discord.ext.commands import Bot
from bot.conf import bot_bridge
import discord
from discord.interactions import InteractionResponse
from bot_ui.reg import uid_form
class cog_debug(commands.Cog):
    def __init__(self, bot):
        self.bot : Bot = bot
        
    @commands.command(name="dump_tracker")
    @commands.has_any_role(*bot_bridge.MOD_ROLES)
    async def dump_tracker(self, ctx):
        await ctx.send(f"""```
{pformat(bot_bridge._honkai_tracker._data)}
```""")

    @commands.command(name="shutdown")
    @commands.has_any_role(*bot_bridge.MOD_ROLES)
    async def shutdown(self, ctx):
        await ctx.send("Shutting down...")
        await self.bot.close()
        exit(0)

    @commands.command(name="list_cogs")
    @commands.has_any_role(*bot_bridge.MOD_ROLES)
    async def list_cogs(self, ctx):
        await ctx.send(f"""```
{pformat(self.bot.cogs)}
```""")
    
def setup(bot):
    bot.add_cog(cog_debug(bot))