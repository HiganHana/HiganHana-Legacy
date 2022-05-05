from tkinter import Image
from discord import ApplicationContext
import requests
import discord
from bot.conf import ArmandaMember
import os
from pprint import pprint
import logging


def has_roles(ctx : ApplicationContext, *rolenames):
    """
    Checks if the author of a message has any of the roles specified.
    """
    author = ctx.author
    roles_obj = author.roles
    for role in roles_obj:
        if role.name in rolenames:
            return True
    return False


# misc
from PIL import Image
import io
def download_img(link : str) -> Image.Image:
    response = requests.get(link, stream=True)
    img = Image.open(io.BytesIO(response.content))
    return img

# ANCHOR COG universal

async def check_author_registered(ctx : ApplicationContext):
    member : ArmandaMember = ArmandaMember.get(discord_id=ctx.author.id)
    if member is None:
        embed = discord.Embed(title="Error", description="You are not registered")
        await ctx.respond(embed=embed)

    return member

async def check_user_registered(ctx : ApplicationContext, user : discord.User):
    member : ArmandaMember = ArmandaMember.get(discord_id=user.id)
    if member is None:
        embed = discord.Embed(title="Error", description=f"The user ({user.mention}) you are looking for is not registered")
        await ctx.respond(embed=embed)

    return member

# for loading python files in folders
def load_python_file(path : str):
    """
    Loads a list of python files from a path.
    """
    if not os.path.isdir(path) and not os.path.exists(path):
        raise FileNotFoundError(f"{path} does not exist")
    files = os.listdir(path)
    files = [file for file in files if file.endswith(".py") and not file.startswith("_")]
    files = [file[:-3] for file in files]
    return files
    
