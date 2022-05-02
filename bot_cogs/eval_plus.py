from contextlib import redirect_stdout
from discord.ext import commands
import discord
import io
import typing
########################################
#---------------IMPORT SEC-------------
from bot.conf import bot_bridge, ArmandaMember
from honkaiDex import BaseCharacter, Battlesuit, StigamataSet
import inspect
from pprint import pprint, pformat
from zxutil.cond import CondField, CondLex
#---------------misc--------------------
BANNED_PHRASES = [
    "sys.exit",
    "os",
    "abort",
    "exit",
    "sleep",
    "discord"
]
########################################
class XSTORE:
    max_limit = 20


    @staticmethod
    def get(key):
        return bot_bridge._x_store.get(key, None)

    @staticmethod
    def set(key, value):
        while len(bot_bridge._x_store) > XSTORE.max_limit:
            bot_bridge._x_store.popitem(last=False)
        bot_bridge._x_store[key] = value

    @staticmethod
    def dump(key, file="dump.txt"):
        if key not in bot_bridge._x_store:
            return
        with open(file, "w") as f:
            f.write(pformat(bot_bridge._x_store[key], indent=4))

def STORE(key):
    return XSTORE.get(key)

class cog_eval(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.EACH_FIELD_HARD_LIMIT = 700
        bot_bridge._x_store = {}

    def parse_to_single_line(self, *code)-> list:
        line = ""
        set_cache = None

        for i, c in enumerate(code):
            if c.startswith("<") and c.endswith(">") and i == 0:
                set_cache = c[1:-1]
                continue

            line = line + c + " "
        return line.strip(), set_cache

    def create_codeblock(self, value):
        value = pformat(value, indent=4)

        if value is None or value == "":
            return None

        if len(value) > self.EACH_FIELD_HARD_LIMIT:
            value = value[:self.EACH_FIELD_HARD_LIMIT] + "\n<TRIMMED>"
        return f"```{value}```"

    async def not_allowed_message(self, ctx, line : str):
        embed = discord.Embed(title="Error", description="You are not allowed to use this command.")
        embed.add_field
        return await ctx.send(embed=embed)

    async def error_code(self, ctx, code_line : str,e: Exception):
        # get stacktrace
        stack = inspect.trace()
        stack = stack[1:]

        # make embed
        embed = discord.Embed(title="Error", description="an error occured while executing your code.")
        embed.add_field(name="Code", value=self.create_codeblock(code_line))
        if (e_message := self.create_codeblock(e)) is not None:
            embed.add_field(name="Error", value=e_message, inline=False)
        if (stacktrace := self.create_codeblock(pformat(stack))) is not None:
            embed.add_field(name="Stacktrace", value=stacktrace, inline=False)
        return await ctx.send(embed=embed)


    @commands.command(name="eval")
    @commands.has_any_role("Bot Dev")
    async def eval_command(self, ctx, *code):
        single_line_code, cache_key = self.parse_to_single_line(*code)

        if any(banned in code for banned in BANNED_PHRASES):
            return await self.not_allowed_message(ctx, single_line_code)

        try:
            result = eval(single_line_code)
            output = None
            with io.StringIO() as buf, redirect_stdout(buf):
                result = await self.exec_eval(result)
                output = buf.getvalue()
                output = output.strip()
            if result is not None and cache_key is not None:
                XSTORE.set(cache_key, result)
            elif output is not None and len(output) > 0 and cache_key is not None:
                XSTORE.set(cache_key, output)

            embed = discord.Embed(title="Eval", description="Evaluation successful.")
            embed.add_field(name="Code", value=self.create_codeblock(single_line_code))
            if result is not None:
                embed.add_field(name="Result", value=self.create_codeblock(result), inline=False)
            if output is not None:
                embed.add_field(name="Output", value=self.create_codeblock(output), inline=False)
            return await ctx.send(embed=embed)

        except Exception as e:
            return await self.error_code(ctx, single_line_code, e)

    async def exec_eval(self, val):
        """
        if val is a callable, execute it, else return value
        """
        if inspect.isgeneratorfunction(val) or inspect.isfunction(val):
            return await self.exec_callable(val)

        if isinstance(val, (set, list, tuple)) and callable(val[0]) and len(val) == 1:
            val = val[0]
            return await self.exec_callable(val)

        if isinstance(val, (set, list, tuple)) and callable(val[0]) and len(val) > 1:
            val, *args = val

            return await self.exec_callable(val, *args)
        
        return val

    async def exec_callable(self, val, *args):
        if inspect.iscoroutinefunction(val):
            return await val(*args)

        val = val(*args)
        return val

def setup(bot):
    bot.add_cog(cog_eval(bot))