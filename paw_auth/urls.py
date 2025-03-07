from django.urls import path
from .views import create_pet, pet_detail

urlpatterns = [
    path('pet/', create_pet),
    path('pet/', pet_detail.as_view()),
]