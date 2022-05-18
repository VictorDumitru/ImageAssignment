import requests
from io import BytesIO
import base64
from bs4 import BeautifulSoup
from PIL import Image
import random
from time import time

def img_from_base64(b64):
    return Image.open(BytesIO(base64.b64decode(b64)))

def get_image_from_html(res):
    soup = BeautifulSoup(res.text, 'lxml')
    img = soup.find('img')['src']
    return img_from_base64(img[img.find(',')+1:])

def get_error_from_html(res):
    soup = BeautifulSoup(res.text, 'lxml')
    return soup.find('h1').decode_contents()

def run_test(filename, shape):
    res = requests.get(f"http://127.0.0.1:8000/images/{filename}?size={shape}")
    if "<img" in res.text:
        img = get_image_from_html(res)
        print(f"Image of size {tuple(img.size)}, requested {filename}?size={shape}")
    else:
        print(f"Error message on website: {get_error_from_html(res)}, requested: {filename}?size={shape}")

if __name__ == "__main__":
    shapes = ["320x240", "32x420", "32000x42", "3840x239", "320x2161", "3840x2160"]

    # should return image just in 320 x 240 ; 3840 x 2160 bounds
    for shape in shapes:
        run_test("sample.jpeg", shape)

    # Should only return "Not in database error"
    for shape in shapes:
        run_test("xxxxxx.jpeg", shape)

    # Should only return "Not a jpeg file"
    for shape in shapes:
        run_test(f"sample.{random.choice(['png', 'jpg', 'gif'])}", shape)
    
    print("==== Stress test ====")
    t = time()
    # stress test for cache
    for _ in range(500):
        run_test(f"sample.jpeg", f"{random.randint(320, 340)}x{random.randint(240, 250)}")
    print(f"Stress test done in {time()-t:.3f}s, should get better with increased cache")
    # res = requests.post("http://127.0.0.1:8000/images/sample.jpeg?size=320x420")
