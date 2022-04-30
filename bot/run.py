import logging
import os
import sys


# add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bot.conf import bot_bridge, ArmandaMember
from bot.init import run_bot_and_flask
from zxutil.folderCacher import FolderCacher
from bot.funcs import download_img

def pulled_save_image(raw, file_path : str, link : str):
    img = download_img(link)
    logging.info(f"Saving image {link} to {file_path}")
    if img is None:
        logging.debug(f"Failed to download image {link}")
    img.save(file_path, "PNG")
    return img



if __name__ == "__main__":
    # IMPORT HONKAIDEX  
    import honkaiDex.profile.cached
    
    # establish cacher
    bot_bridge._pulled_cacher = FolderCacher.make_webimg_cache("cache/pulled_images/", extension="png")
    bot_bridge._merged_cacher = FolderCacher.make_webimg_cache("cache/merged_images/", extension="png")

    bot_bridge._pulled_cacher.file_save_method =pulled_save_image 

    ArmandaMember.from_dict(bot_bridge.ARMANDA_JSON)

    run_bot_and_flask()