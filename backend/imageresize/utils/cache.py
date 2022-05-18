from glob import glob 
from PIL import Image
from io import BytesIO

def get_image_res(img_name):
    """Given an image name, returns a tuple of its size in pixels
    """
    return tuple(Image.open(img_name).size)

def get_image_size_bytes(img):
    """Saves image to buffer and returns its size in bytes
        int: n.o bytes in image
    """
    buffered = BytesIO()
    img.save(buffered, format="JPEG")
    return buffered.tell()


class Cache:
    def __init__(self, all_files, max_size:int=70000000) -> None:
        """
        Args:
            max_size (int, optional): (roughly) n.o bits in image. Defaults to 64000000.
            all_files (list[str]): All image names in static folder
        """
        self.images = {
                f"{fname}_{get_image_res(fname)}":Image.open(fname)
                    for fname in all_files
            }
        self.historic_frequencies = {name:0 for name in self.images.keys()}
        self.sizes = {fname:get_image_size_bytes(img) for fname, img in self.images.items()}
        self.current_size = sum(val for val in self.sizes.values())
        self.max_size = max_size
        if self.current_size >= self.max_size:
            raise Exception("Victor's cache is not big enough !!! ( less than needed for one resolution per static file )")

    def __len__(self):
        """Returns length of cache
        """
        return len(self.images)
    
    def __getitem__(self, key):
        """Sets historic frequency and returns element
        """
        if key in self.historic_frequencies:
            self.historic_frequencies[key] += 1
        else: 
            self.historic_frequencies[key] = 1
        return self.images[key]
    
    def __setitem__(self, key:str, value):
        """Adds item in cache. Handles freeing up space if needed

        Args:
            key (str): filename_size
            value (Image): Image to add
        """
        new_image_size = get_image_size_bytes(value)
        while self.current_size + new_image_size >= self.max_size and len(self.historic_frequencies) != 0:
            # get the key of the least frequent requested item
            least_wanted = min(
                    list(filter(lambda y: y[0] in self.images.keys(), self.historic_frequencies.items())), key=lambda x: x[1]
                )[0]
            
            self.current_size -= self.sizes[least_wanted]
            del self.images[least_wanted]
            del self.sizes[least_wanted] # optional ?
            del self.historic_frequencies[least_wanted]
            # print(f"Cache full! Deleting least wanted: {least_wanted}")
        self.images[key] = value
        self.sizes[key] = new_image_size
        self.current_size += new_image_size
        self.historic_frequencies[key] = 1

    def __str__(self):
        return f"\n ==CACHED ITEMS==\n{self.images}\n===\nFilled: {self.current_size}/{self.max_size}\n"
