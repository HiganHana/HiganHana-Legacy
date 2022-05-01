from contextlib import redirect_stdout
from pprint import pformat
import typing
from discord.ext import commands
from discord.ext.commands import Bot
from bot.conf import bot_bridge
import discord
from discord.interactions import InteractionResponse
from bot_ui.reg import uid_form
import honkaiDex
from honkaiDex import Battlesuit,BaseCharacter,StigamataSet
import io
import inspect
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

        if "os.system" in code:
            embed.add_field(name="Error", value="os.system is not allowed")
            return await ctx.respond(embed=embed)

        try:
            result = eval(code)

            output = None
            with io.StringIO() as buf, redirect_stdout(buf):
                result = await self.exec_eval(result)
                output = buf.getvalue()
                    
                if output is not None:
                    embed.add_field(name="stdout", value=f"```{output}```")
            embed.add_field(name="result", value=f"```{pformat(result)}```")
            
            
        except Exception as e:
            embed.add_field(name="error", value=f"```{pformat(e)}```")
        await ctx.send(embed=embed)

    async def exec_callable(self, val, *args):
        if inspect.iscoroutinefunction(val):
            return await val(*args)

        val = val(*args)
        return val
        

    async def exec_eval(self, val):
        if callable(val):
            return await self.exec_callable(val)

        if isinstance(val, typing.Iterable) and len(val) == 1:
            val = val[0]
            return await self.exec_callable(val)

        if isinstance(val, typing.Iterable) and len(val) > 1:
            val, *args = val

            return await self.exec_callable(val, *args)
        
        return val

def setup(bot):
    bot.add_cog(cog_debug(bot))