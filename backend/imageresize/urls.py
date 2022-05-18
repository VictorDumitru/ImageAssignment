from django.urls import path
from . import views

urlpatterns = [
    path('<str:filename>', views.get_image, name="get_image"),
]
