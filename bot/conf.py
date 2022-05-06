"""
this file contains the global configurations

BotBridge will load the specified json file with dict.update(), overwriting existing keys
"""

from dataclasses import dataclass
import typing
import logging
from zxutil.bridge import Bridge
from zxutil.umodel import UItem, UniqueKey, UPrimaryKey
from zxutil.folderCacher import FolderCacher
from honkaiDex.game import valid_lv, valid_na_uid
import genshin
import discord


class BotBridge(Bridge):
    prefix = "!"
    case_insensitive = True
    cogs = []
    cog_folder = "bot_cogs"
    cog_building = "building_cogs"
    allowed_servers : typing.List[int]
    token : str
    no_bot : bool = False

    # flask
    host = "0.0.0.0"
    port = 8000
    blueprints_folder = "flask_cogs"

    # logging
    log_level = logging.WARNING
    log_format = "%(asctime)s:%(levelname)s:%(name)s:%(message)s"
    
    log_ignore_discord = True
    log_lv_discord = logging.WARNING
    log_to_file = True
    log_file = "bot.log"

    # permissions
    MOD_ROLES = ["Impact Vice Leader", "Impact Leader","Jasione","Bot Dev"]
    BOOSTER_PLAN = ["Server Booster"]
    IMPACT_MEMBER = ["Impact Member"]
    BOT_DEV = "Bot Dev"
    # hoyo
    ltuid : int
    ltoken : str

    # armanda member base
    ARMANDA_JSON  = "appdata/armanda_members.json"

    # image saving
    _pulled_cacher : FolderCacher
    _merged_cacher : FolderCacher

    #
    _bot : discord.Bot
    _hoyoclient : genshin.Client

def valid_genshin_id(value):
    str_val = str(value)

    if len(str_val) != 9:
        return False

    if not str_val.isdigit():
        return False
    
    return int(str_val)

@dataclass
class ArmandaMember(UItem):
    discord_id : typing.Union[int, UPrimaryKey]
    uid : typing.Union[int, UniqueKey, valid_na_uid]
    lv : typing.Union[int, valid_lv]
    genshin_id : typing.Union[int, UniqueKey, valid_genshin_id] = None

bot_bridge : BotBridge = BotBridge(file="appdata/config.json")