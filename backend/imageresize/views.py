from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .utils.image_grabber import ImageGrabber, get_image_and_resize, convert_base64 

image_grabber = ImageGrabber()
# print(image_grabber.cache)

# Create your views here.
def get_image(req, filename):
    """Serve image from the static folder
    """

    if req.method == "GET":
        if not filename.endswith(".jpeg"):
            return render(req, "images/index.html", {"error": "Not a jpeg file"})
        
        if filename not in list(map(lambda x: x.split('/')[-1], image_grabber.all_files)):
            return render(req, "images/index.html", {"error": "File not in our database"})
        
        size = tuple(map(int, req.GET.get('size').split("x")))
        
        if size[0] < 320 or size[0] > 3840 or size[1] < 240 or size[1] > 2160:
            return render(req, "images/index.html",
                {"error": "Size out of bounds ( Min: 320 x 240; Max:3840 x 2160 )"}
             )

        # print(image_grabber.cache)
        img = image_grabber.load_image(filename, size)
        img_str = convert_base64(img)
        
        # print(image_grabber.cache)
        print(f"Filled: {image_grabber.cache.current_size}/{image_grabber.cache.max_size}\n")
        return render(req, "images/index.html", {"img_data": img_str})
    else:
        return JsonResponse({"message": f"{req.method} requests not allowed on this route", "error": False})