from glob import glob
import base64
from io import BytesIO
from PIL import Image
from .cache import Cache


def get_image_and_resize(img_name, size):
    return Image.open(f"./static/{img_name}").resize(size)

def convert_base64(img):
    """Converts PIL Image into base64 string
    Returns:
        str: base64 string of image
    """
    buffered = BytesIO()
    img.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue())
    return img_str.decode('utf-8')

class ImageGrabber():
    """Handles high level loading of images
    """
    def __init__(self) -> None:
        self.all_files = glob("./static/*.jpeg")
        self.cache = Cache(self.all_files)
    
    def load_image(self, filename:str, size:tuple):
        """Decides weather to load image from static file or cache

        Returns:
            Image: resized image
        """
        cache_name = f"{filename}_{size}"
        if cache_name in self.cache.images.keys():
            # print(f"{cache_name} was in cache, counting and returning it")
            return self.cache[cache_name]
        else:
            # print(f"{cache_name} was not in cache, caching, counting and returning it")
            img = get_image_and_resize(filename, size)
            self.cache[cache_name] = img
            return img

    