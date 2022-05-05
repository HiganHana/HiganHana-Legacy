import logging
import os
import sys


# add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bot.conf import bot_bridge, ArmandaMember
from bot.init import run_bot_and_flask
from zxutil.folderCacher import FolderCacher
from bot.funcs import download_img
from genshin import Client

if __name__ == "__main__":
    # IMPORT HONKAIDEX  
    import honkaiDex.profile.cached
    
    # setup genshin client
    cookies = {
        "ltuid" : bot_bridge.ltuid,
        "ltoken" : bot_bridge.ltoken,
    }

    bot_bridge._hoyoclient = Client(cookies=cookies)

    # establish cacher
    bot_bridge._pulled_cacher = FolderCacher.make_webimg_cache("cache/pulled_images/", extension="png")
    bot_bridge._merged_cacher = FolderCacher.make_webimg_cache("cache/merged_images/", extension="png")

    ArmandaMember.from_dict(bot_bridge.ARMANDA_JSON)

    run_bot_and_flask()

    while True:
        continue