import logging
import discord
from discord import Interaction, Button
from discord.ext import commands
from discord.ui import View, InputText,Modal
from honkaiDex.game import valid_lv, valid_na_uid
from discord.interactions import InteractionResponse
from bot.conf import bot_bridge
from zxutil.collections.uitem import ValidationFail
class uid_form(Modal):
    def __init__(self):
        super().__init__("UID FORM")
        self.description = "Enter your in-game UID"
        self.uid_field = InputText(label="uid", placeholder="Enter your in-game UID")
        self.lv_field = InputText(label="lv", placeholder="Enter your in-game LV")
        self.add_item(self.uid_field)
        self.add_item(self.lv_field)

    async def callback(self, interaction : Interaction):
        user_id = interaction.user.id

        lv = self.lv_field.value
        uid = self.uid_field.value

        embed = discord.Embed(title="Register Form Feedback")

        if not valid_lv(lv):
            embed.add_field(name="Error", value="Please enter a valid LV")
            return await interaction.response.send_message(embed=embed)
        if not valid_na_uid(uid):
            embed.add_field(name="Error", value="Please enter a valid UID")
            return await interaction.response.send_message(embed=embed)

        try:
            bot_bridge._honkai_tracker.create_item(
                discord_id=user_id,
                uid=uid,
                lv=int(lv)
            )
        except ValidationFail as e:
            e : ValidationFail
            embed.add_field(name="Error", value=f"{e.problematic_key} is invalid ({e.validation_func.__name__})")
            return await interaction.response.send_message(embed=embed)

        bot_bridge._honkai_tracker.save()
        
        embed.add_field(name="uid", value=uid)
        embed.add_field(name="lv", value=lv)
        embed.add_field(name="user", value=interaction.user.mention)
        await interaction.response.send_message(embed=embed)

