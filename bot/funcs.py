from tkinter import Image
from discord import ApplicationContext
import requests
import discord
from bot.conf import ArmandaMember
import logging
import os
from pprint import pprint
from discord.ext import commands
import logging
import sys
from flask import Flask
from threading import Thread
import importlib


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


def download_image_from_url(url : str, filename : str):
    """
    Downloads an image from a url and saves it to a file.
    """
    # if filename already in cache, return
    if os.path.exists(os.path.join("cache", "base", filename)):
        return

    if not filename:
        return

    path = os.path.join("cache","base", filename)

    if os.path.exists(path):
        return
    
    response = requests.get(url, stream=True)
    with open(path, 'wb') as out_file:
        out_file.write(response.content)

def batch_download(**kwargs):
    """
    Downloads images from a list of urls.
    """
    for filename, url  in kwargs.items():
        download_image_from_url(url, filename)

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

