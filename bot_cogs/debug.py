from pprint import pformat
from discord.ext import commands
import discord
from bot.conf import ArmandaMember, bot_bridge

class cog_debug(commands.Cog):
    def __init__(self, bot):
        self.bot : discord.Bot = bot

    async def build_and_send_embed(self, ctx,title:str, data):
        embed = discord.Embed(title=title, description=f"by {ctx.author.mention}")
        if data is not None:
            data =pformat(data, indent=4)
            data = "```" + data + "```"
            embed.add_field(name="data", value=data)
        return await ctx.send(embed=embed)

    @commands.command(name="dump_tracker")
    @commands.has_any_role(bot_bridge.BOT_DEV)
    async def dump_tracker(self, ctx):
        ret = []
        for member in ArmandaMember.yield_instance():
            member : ArmandaMember
            ret.append(member.uid)

        return await self.build_and_send_embed(ctx, "Dump tracker", ret)

    @commands.command(name="shutdown")
    @commands.has_any_role(bot_bridge.BOT_DEV)
    async def shutdown(self, ctx):
        await self.build_and_send_embed(ctx, "Shutdown", "Shutting down...")
        await self.bot.close()
        exit(0)

    @commands.command(name="list_cogs")
    @commands.has_any_role(bot_bridge.BOT_DEV)
    async def list_cogs(self, ctx):
        return await self.build_and_send_embed(ctx, "Cogs", self.bot.cogs)

    @commands.command(name="unload_cog")
    @commands.has_any_role(bot_bridge.BOT_DEV)
    async def unload_cog(self, ctx, cog_name):
        try:
            self.bot.unload_extension(cog_name)
            return await self.build_and_send_embed(ctx, "Unload cog", f"Cog {cog_name} unloaded.")
        except Exception as e:
            return await self.build_and_send_embed(ctx, "Unload cog", f"Error: {e}")

    @commands.command(name="load_cog")
    @commands.has_any_role(bot_bridge.BOT_DEV)
    async def load_cog(self, ctx, cog_name):
        try:
            self.bot.load_extension(bot_bridge.cog_folder+"."+cog_name)
            return await self.build_and_send_embed(ctx, "Load cog", f"Cog {cog_name} loaded.")
        except Exception as e:
            return await self.build_and_send_embed(ctx, "Load cog", f"Error: {e}")

    @commands.command(name="reload_cog")
    @commands.has_any_role(bot_bridge.BOT_DEV)
    async def reload_cog(self, ctx, cog_name):
        cog_name =bot_bridge.cog_folder+"."+cog_name
        try:
            self.bot.unload_extension(cog_name)
            self.bot.load_extension(cog_name)
            return await self.build_and_send_embed(ctx, "Reload cog", f"Cog {cog_name} reloaded.")
        except Exception as e:
            return await self.build_and_send_embed(ctx, "Reload cog", f"Error: {e}")

def setup(bot):
    bot.add_cog(cog_debug(bot))