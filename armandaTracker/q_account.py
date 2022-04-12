import discord
from discord import Interaction, Button
from discord.ext import commands
from discord.ui import View, InputText,Modal

class uid_form(Modal):
    def __init__(self):
        super().__init__("uid form")
        self.description = "Enter your in-game UID"
        self.input_text = InputText(label="uid", placeholder="Enter your in-game UID")
        self.add_item(self.input_text)

    async def callback(self, interaction : Interaction):
        embed = discord.Embed(title="uid", description=self.input_text.value)
        embed.add_field(name="uid", value=self.input_text.value)
        await interaction.response.send_message(embed=embed)


async def ask_in_game_uid(ctx : commands.Context):
    """
    Ask for the in-game UID of the member.
    """
    form = uid_form()

    await ctx.interaction.response.send_modal(form)
    