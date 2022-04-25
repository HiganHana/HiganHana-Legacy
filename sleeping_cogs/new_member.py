from turtle import title
import discord
from discord.ext import commands
from discord.bot import Bot
from bot.conf import bot_bridge
help = discord.SlashCommandGroup(name="help", description="Help you get familiar with this server")
class new_member(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
       
        
    #Fresh people join this discord TODO add embed and infomation,
    @commands.slash_command(name="yahallo")
    async def new_member(self, ctx):
        #Create embed
        embed = discord.Embed(
            title = "Welcome to HiganHana",
            description = f"Welcome to the server @{ctx.author.name}! Check out #chill-chat to give yourself a role!",
            color = discord.colour.red(),
        )
        
        #Honkai Impact field
        embed.add_field(
            title = "Honkai Impact Players",
            value = "If you're applying or already in the armada, **Please use the command /register to get started**"
        )
        
        #Honkai Star Rail
        embed.add_field(
            title = "Honkai Star Rail Players",
            value = "The game is currently in a closed contracted beta test, please avoid leaking anything here cuz last thing I need is a lawsuit on my ass"
        )
        
        #Hebban field
        embed.add_field(
            title = "Heaven Burns Red Players",
            value = "Kiyan can answer some questions so don't hesitate to ask him"
        )
        await ctx.respond(embed = embed)
        
        
    #create a help command to guide people
    
    
    #Overall
    @help.command
    async def overall(ctx):
        embed = discord.embed(
            title = "Help - Hanabusa Cafe",
            value = "As long as you\'r following the #rules, you're free to do whatever"
        )
        embed.add_field(
            title = "Go get your roles",
            value = "If you haven\'t done that, then please do that so you unlock more chats",
            )
        embed.add_field(
            title = "Create a ticket",
            value = "If you wanna complains or something, create a ticket at #ticket-countertop, most information will be in there",
            )
        embed.add_field(
            title = "Annoucements/Events",
            value = "I rarely do annoucement unless it\'t related to server change or cyber-security stuff",
            )
        embed.add_field(
            title = "Limited time stuff",
            value = "Sometime there will be a limited time stuff that we do in this server, so be sure to look out for that",
            )
        embed.add_field(
            title = "Youtube/Twitch",
            value = "You make video or stream? Then you can post your content in the **Content Creator** catergory",
            )
        embed.add_field(
            title = "Content Creator",
            value = "Hand-picked content creator will get to post in #cc-uploaded-video and/or #cc-going-live, otherwise bot will do the posting",
            inline = True
            )
        embed.add_field(
            title = "Small Creator",
            value = "#youtube-video and #twitch-strem will be available for anyone to post",
            inline = True
            )
        await ctx.respond(embed = embed)
    
    #Hanabusa Cafe
    @help.command
    async def hanabusachat(ctx):
        embed = discord.embed(
            title = "Help - Hanabusa Cafe",
            value = "Please attempt to keep the topic in there, if you're talking about one unrelated stuff please move to another channel"
        )
        embed.add_field(
            title = "#chill-chat",
            value = "Basically talks about whatever, as long as it\'s SFW",
            inline = True
            )
        embed.add_field(
            title = "#bot-spam",
            value = "Use bot\'s commands here",
            inline = True
            )
        embed.add_field(
            title = "#horni-jail",
            value = "Very NSFW, join if you\'re willing to",
            inline = True
            )
        embed.add_field(
            title = "#shitpost-cave",
            value = "Post your shitpost, memes or laughable stuff here",
            inline = True
            )
        embed.add_field(
            title = "#art-channel",
            value = "Fan arts, drawing, etc. goes here, can be a slight ecchi but no hentai, that\'s for #horni-jail",
            inline = True
            )
        embed.set_footer(text = "If there\'s many request for a channel, I\' make one")
        await ctx.respond(embed = embed)
        
    #Honkai
    async def honkaiimpact(ctx):
        embed = discord.embed(
            title = "Help - Honkai Impact",
            value = "Don\'t hesitate to ask any questions and ping the helpers"
        )
        embed.add_field(
            title = "#impact-chat",
            value = "Honkai Impact related goes here, any questions will most likely be answered here",
            inline = True
            )
        embed.add_field(
            title = "#impact-annoucement",
            value = "Most of the annoucement related to Honkai or the armada will go here",
            inline = True
            )
        embed.add_field(
            title = "#impact-code",
            value = "If this chat glow white, there's a new code",
            inline = True
            )
        embed.add_field(
            title = "#impact-faq",
            value = "Honkai players\' bestfriend, be sure to check this first before asking any question",
            inline = True
            )
        embed.add_field(
            title = "#impact-lore",
            value = "All lore stuff will be discuss here to avoid spoilers in other chats",
            inline = True
            )
        embed.add_field(
            title = "#impact-leak-discussion",
            value = "Leaks, lots of leaks here",
            inline = True
            )
        embed.add_field(
            title = "#impact-coop",
            value = "Ask for a coop partner here",
            inline = True
            )
        embed.add_field(
            title = "#looking-for-sensei",
            value = "If you need a sensei or cadet, tell us here",
            inline = True
            )
        await ctx.respond(embed = embed)

def setup(bot):
    bot.add_cog(new_member(bot))

