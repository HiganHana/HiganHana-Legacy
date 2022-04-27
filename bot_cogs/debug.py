from contextlib import redirect_stdout
from pprint import pformat
import sys
from discord.ext import commands
from discord.ext.commands import Bot
from bot.conf import bot_bridge
import discord
from discord.interactions import InteractionResponse
from bot_ui.reg import uid_form
import honkaiDex
from honkaiDex import Battlesuit,BaseCharacter,StigamataSet
import io
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
    
    @commands.command(name="eval")
    @commands.has_any_role("Bot Dev")
    async def eval_code(self, ctx, *code):
        
        line = ""
        for c in code:
            line = line + c + " "
        
        code = str(line).strip()
        embed = discord.Embed(title="Eval Result", description=f"input:```{code}```")
        try:
            result = eval(code)

            output = None
            with io.StringIO() as buf, redirect_stdout(buf):
                if callable(result):
                    result = result()
                    output = buf.getvalue()
                    
                    if output is not None:
                        embed.add_field(name="stdout", value=f"```{output}```")
            embed.add_field(name="result", value=f"```{pformat(result)}```")
            
            
        except Exception as e:
            embed.add_field(name="error", value=f"```{pformat(e)}```")
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(cog_debug(bot))