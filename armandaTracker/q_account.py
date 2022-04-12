import discord
from discord import Interaction, Button
from discord.ext import commands
from discord.ui import View, InputText

async def ask_in_game_uid(ctx : commands.Context):
    """
    Ask for the in-game UID of the member.
    """
    async def on_callback(interaction : Interaction):  
        if interaction.result == Interaction.Result.cancelled:
            await ctx.author.send("Cancelled")
        if interaction.result == Interaction.Result.success:
            await ctx.author.send(f"{interaction.input_text}")

    # send dm with inputtext
    view = View()
    # set callback
    uid_input = InputText(label="uid", placeholder="Enter your in-game UID")
    view.add_item(uid_input)
    done_button = Button(text="Done", style=Button.Style.primary)
    done_button.callback = on_callback
    view.add_item(done_button)

    await ctx.author.send(view=view)
    