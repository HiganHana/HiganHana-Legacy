from pprint import pformat
from discord.ext import commands
import discord
from bot.conf import ArmandaMember, bot_bridge
from bot.funcs import has_roles

class mod_cog(commands.Cog):
    def __init__(self, bot):
        self.bot : discord.Bot = bot

    def cog_check(self, ctx: discord.ApplicationContext) -> bool:
        if not has_roles(ctx, *bot_bridge.MOD_ROLES):
            return False
        return True
        
    @commands.command(name="echo")
    async def echo_x(self, ctx, *input):
        line = ""
        for x in input:
            line += x + " "

        await ctx.send(line)
        await ctx.message.delete()

    @commands.command(name="bury")
    async def bury(self, ctx: discord.ApplicationContext, counter : int=None):
        await ctx.message.delete()

        if counter is None:
            counter = 1

        if len(str(counter)) > 15:
            msg = await ctx.fetch_message(counter)
            if msg is not None:
                return await msg.delete()
            return

        if counter >= 10:
            counter = 10
        if counter <= 0:
            return

        await ctx.channel.purge(limit=counter)
                
    
    @commands.command(name="cast")
    async def cast(self, ctx : discord.ApplicationContext, channel : discord.TextChannel):
        lines = []
        title = "Cast"
        description = f"by {ctx.author.mention}"
        fname = "Message"
        notify_msg = None
        img=None
        while True:
            if notify_msg is not None:
                await notify_msg.delete()
            notify_msg = await ctx.send(f"listening...")

            msg : discord.Message = await ctx.bot.wait_for("message", check=lambda m: m.author == ctx.author, timeout=30)
            if msg is None:
                continue
            if msg.content == "eof":
                await notify_msg.delete()
                await msg.delete()
                break
            if msg.content.startswith("title="):
                title = msg.content[6:]
            elif msg.content.startswith("des="):
                description = msg.content[4:]
            elif msg.content.startswith("fname="):
                fname = msg.content[6:]
            elif msg.content.startswith("http"):
                lines.append(f"[link]({msg.content})")
            elif msg.content.startswith("img="):
                img = msg.content[4:]
            else:
                lines.append(msg.content)
            
            await msg.delete()

        embed = discord.Embed(title=title, description=description)
        if len(lines) > 0:
            embed.add_field(name=fname, value="\n".join(lines))
        if img is not None:
            embed.set_image(url=img)
            
        await channel.send(embed=embed)

    

def setup(bot):
    bot.add_cog(mod_cog(bot))