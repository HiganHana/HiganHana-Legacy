import discord
from discord import Interaction
from discord.ui import InputText,Modal
from honkaiDex.game import valid_lv, valid_na_uid
from bot.conf import ArmandaMember, bot_bridge
from zxutil.umodel import U_ValidationError
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
            member = ArmandaMember(
                discord_id=user_id,
                uid=uid,
                lv=lv
            )
            member.export_this(bot_bridge.ARMANDA_JSON)
        except U_ValidationError as e:
            e : U_ValidationError
            embed.add_field(name="Error", value=e.message)
            return await interaction.response.send_message(embed=embed)
        
        embed.add_field(name="uid", value=uid)
        embed.add_field(name="lv", value=lv)
        embed.add_field(name="user", value=interaction.user.mention)
        await interaction.response.send_message(embed=embed)

