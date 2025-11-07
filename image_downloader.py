import os
import random
import string
import gdown
from PIL import Image, ImageOps


def prepare_image(_input):
    random.seed(_input)
    name = "".join(random.choices(string.hexdigits, k=15)) + ".jpg" # encrypts the name of the file based on the filename
    for file in os.listdir("images"):
        if name == file: # if the filename already exists in the folder, skip it
            return "images/" + name
    image = gdown.download(_input, "images/" + name, fuzzy=True) # if it doesn't, download the file with the encrypted name
    with Image.open(image) as _img: # rescale the image and resave the rescaled image
        _img = ImageOps.exif_transpose(_img) # rotate image from exif tags
        ratio = 375 / _img.width
        _img = _img.resize((int(_img.width * ratio), int(_img.height * ratio)))
        _img = _img.convert("RGB")
        # Qt does resize images to fit the window, however it does not keep aspect ratio.
        # this will not fix the issue entirely but for most pictures it should be fine

        _img.save("images/" + name, format="jpeg", optimize=True, quality=35)

    return image
