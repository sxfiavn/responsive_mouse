import os
from PIL import Image, ImageTk

ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets")

# Colors
PRIMARY_BG = "#524A8F"
TEXT_COLOR = "white"

# Fonts (names only — actual font files must be system-installed)
TITLE_FONT = ("Quicksand", 18, "bold")
BODY_FONT = ("Quicksand", 14)
BUTTON_FONT = ("Quicksand", 16, "bold")

# Image cache to avoid reloading
_image_cache = {}

def load_image(path, size=None):
    """
    Load an image from the assets folder. Optionally resize.
    Returns a PhotoImage for use in Tkinter.
    """
    global _image_cache

    if (path, size) in _image_cache:
        return _image_cache[(path, size)]

    img = Image.open(path)

    if size:
        img = img.resize(size, Image.LANCZOS)

    photo = ImageTk.PhotoImage(img)
    _image_cache[(path, size)] = photo
    return photo
