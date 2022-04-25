from discord import ApplicationContext

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


from PIL import Image
import os
import requests

__DOWNLOADED__ = []

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

    global __DOWNLOADED__
    __DOWNLOADED__.append(filename)

def batch_download(**kwargs):
    """
    Downloads images from a list of urls.
    """
    for filename, url  in kwargs.items():
        download_image_from_url(url, filename)

__INCREMENTED__ = 0

def combine_image(*args):
    """
    Combines multiple images into one.
    """
    global __INCREMENTED__
    # 
    if __INCREMENTED__ > 10:
        __INCREMENTED__ =0

    if len(args) == 0:
        return
    
    if len(args) > 4:
        return
    
    images = [None, None, None, None]
    for i, arg in enumerate(args):
        arg = os.path.join("cache", "base", arg)
        if os.path.exists(arg):
            images[i] = Image.open(arg)
            # renormalize to 128x128
            images[i] = images[i].resize((128, 128))

    
    # combine
    height = 128
    width = 128*4
    combined = Image.new('RGBA', (width, height))
    for i, image in enumerate(images):
        if image is None:
            continue
        combined.paste(image, (128*i, 0))

    save_path = os.path.join("cache", "combined", f"test_{__INCREMENTED__}.png")
    combined.save(save_path)
    
    __INCREMENTED__ += 1
    
    return combined, save_path