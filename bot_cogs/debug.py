from pprint import pformat
from discord.ext import commands
import discord
from bot.conf import ArmandaMember, bot_bridge
from bot.funcs import has_roles
import asyncio

class cog_debug(commands.Cog):
    def __init__(self, bot):
        self.bot : discord.Bot = bot

    def cog_check(self, ctx: discord.ApplicationContext) -> bool:
        if not has_roles(ctx, bot_bridge.BOT_DEV):
            return False
        return True

    async def build_and_send_embed(self, ctx,title:str, data):
        embed = discord.Embed(title=title, description=f"by {ctx.author.mention}")
        if data is not None:
            data =pformat(data, indent=4)
            data = "```" + data + "```"
            embed.add_field(name="data", value=data)
        return await ctx.send(embed=embed)

    @commands.command(name="dump_tracker")
    async def dump_tracker(self, ctx):
        ret = []
        for uid in ArmandaMember.yield_field("uid"):
            ret.append(uid)

        return await self.build_and_send_embed(ctx, "Dump tracker", ret)

    @commands.command(name="shutdown")
    async def shutdown(self, ctx):
        await self.build_and_send_embed(ctx, "Shutdown", "Shutting down...")
        await self.bot.close()
        exit(0)

    @commands.command(name="list_cogs")
    async def list_cogs(self, ctx):
        return await self.build_and_send_embed(ctx, "Cogs", [cog for cog in self.bot.cogs.values()])

    @commands.command(name="unload_cog")
    async def unload_cog(self, ctx, cog_name):
        try:
            self.bot.unload_extension(cog_name)
            return await self.build_and_send_embed(ctx, "Unload cog", f"Cog {cog_name} unloaded.")
        except Exception as e:
            return await self.build_and_send_embed(ctx, "Unload cog", f"Error: {e}")

    @commands.command(name="load_cog")
    async def load_cog(self, ctx, cog_name):
        try:
            self.bot.load_extension(bot_bridge.cog_folder+"."+cog_name)
            return await self.build_and_send_embed(ctx, "Load cog", f"Cog {cog_name} loaded.")
        except Exception as e:
            return await self.build_and_send_embed(ctx, "Load cog", f"Error: {e}")

    @commands.command(name="reload_cog")
    async def reload_cog(self, ctx, cog_name):
        cog_name =bot_bridge.cog_folder+"."+cog_name
        try:
            self.bot.unload_extension(cog_name)
            self.bot.load_extension(cog_name)
            return await self.build_and_send_embed(ctx, "Reload cog", f"Cog {cog_name} reloaded.")
        except Exception as e:
            return await self.build_and_send_embed(ctx, "Reload cog", f"Error: {e}")

    @commands.command(name="wthreads")
    async def wake_threads(self, ctx : discord.ApplicationContext):
        channel = ctx.channel
        archived_threads_iter = channel.archived_threads()

        # walk through the archived threads iterator
        thread : discord.Thread = await archived_threads_iter.get()

        while True:
            try:
                await thread.unarchive()
                thread = await archived_threads_iter.next()
            except asyncio.QueueEmpty:
                break
                
    
    @commands.command(name="ithreads", help="Index all threads in the channel")
    async def index(self, ctx : discord.ApplicationContext, channel:discord.TextChannel = None, add_des = False):
        await ctx.message.delete()
        if channel is None:
            channel = ctx.channel

        threads = channel.threads
        if len(threads) == 0:
            
            return
        lines = []
        if not add_des:
            for thread in threads:
                thread : discord.Thread
                await thread.unarchive()
                lines.append(f"{thread.mention}")

            embed = discord.Embed(title=f"{ctx.channel.name} Threads", description="\n".join(lines)) 
            return await ctx.send(embed=embed)
        
        embed = discord.Embed(title=f"{ctx.channel.name} Threads")
        for thread in threads:
            
            thread : discord.Thread
            await thread.unarchive()
            # get thread first message
            message = thread.last_message

            embed.add_field(name=thread.name, value=f"{thread.mention}\n{message.content}")

        await ctx.send(embed=embed)

    @commands.command(name="xbury")
    async def xbury(self, ctx : discord.ApplicationContext, counter : int = 1):
        await ctx.message.delete()
        await ctx.channel.purge(limit=counter)

def setup(bot):
    bot.add_cog(cog_debug(bot))