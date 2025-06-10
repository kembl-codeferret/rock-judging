import os
import shutil
import os.path as path
import random
import string
import gdown
from PIL import Image


def prepare_image(_input):
    random.seed(_input)
    name = "".join(random.choices(string.hexdigits, k=20)) + ".jpg" # encrypts the name of the file based on the filename
    for file in os.listdir("images"):
        if name == file: # if the filename already exists in the folder, skip it
            return "images/" + name
    image = gdown.download(_input, "images/" + name, fuzzy=True) # if it doesn't, download the file with the encrypted name
    with Image.open(image) as _img:
        ratio = 500 / _img.width
        _img = _img.resize((int(_img.width * ratio), int(_img.height * ratio)))
        _img = _img.convert("RGB")
        _img.save("images/" + name, format="jpeg", optimize=True, quality=35)

    return image
