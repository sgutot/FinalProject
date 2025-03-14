from django.urls import path
from .views import create_pet, pet_detail, petImage
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('create_pet/', create_pet.as_view()),
    path('pet_detail/<int:pk>', pet_detail.as_view()),
    path('uploads/', petImage.as_view(),),
]