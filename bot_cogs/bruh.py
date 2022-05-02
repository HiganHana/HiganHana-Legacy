from discord.ext import commands
import discord
import random

class cog_bruh(commands.Cog):
    def __init__(self, bot):
        self.bot : discord.Bot = bot
        self.last_message = None
        self.count = 0
        self.activate_instanta = ["lol", "lmao", "bruh", "hi"]
        self.temp_ban = []
        self.temp_ban_size = 3
        self.grace = 0
        
    @commands.Cog.listener("on_message")
    async def echoer(self, message : discord.Message):
        if message.author.bot or message.content.startswith("!") or len(message.content) > 50:
            return
        if self.grace > 0:
            self.grace -= 1
        
        # if matching any of the activate_instanta
        if any(x in message.content.lower() for x in self.activate_instanta) and message.author not in self.temp_ban and self.grace <= 0:
            await message.channel.send(message.content)
            self.count = 0
            self.last_message = None   
            self.temp_ban.append(message.author)
            if len(self.temp_ban) > self.temp_ban_size:
                self.temp_ban.pop(0)

            self.grace = random.randint(1, 5)
            return

        if self.last_message is None:
            self.last_message = message.content
            return

        if self.last_message == message.content:
            self.count += 1
        else:
            self.count = 0
            self.last_message = message.content
            return

        random_number = random.randint(self.count, 5)
        if random_number <= 2:
            return
            
        await message.channel.send(message.content)
        self.count = 0
        self.last_message = None
        
    
def setup(bot):
    bot.add_cog(cog_bruh(bot))