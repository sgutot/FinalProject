"""
URL configuration for server project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import re_path
from django.urls import include, path

import paw_auth.views
from .import views
from .views import login, signup
# from .views import create_pet, pet_detail, petImage
# from .views import search_for_toxic_ingredients
from .views import new_product_name, new_product_description, new_product_front_picture, new_product_ingredients_picture, new_product_requester, new_product_detail, status_new_product, get_product
from .views import UserPetsView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    #Account
    path("accounts/", include("django.contrib.auth.urls")),
    re_path('signup', views.signup, name="signup"),
    re_path('login', views.login, name="login"),
    re_path('test_token', views.test_token, name="test_token"),
    path('paw_auth/', include('paw_auth.urls')),

    #Pet
    # path('create_pet/', create_pet.as_view(), name="create_pet"),
    # path('pet_detail/<int:pk>/', pet_detail.as_view()),
    # path('uploads/', petImage.as_view(),),

    #Scan
    # path('search_for_toxic_ingredients/', views.search_for_toxic_ingredients),
    path('scan/', views.get_product, name='get_product'),

    #New Product
    path('new_product_name/', new_product_name.as_view(), name="new_product_name"),
    path('new_product_description/', new_product_description.as_view()),
    path('uploads/', new_product_front_picture.as_view(),),
    path('uploads/', new_product_ingredients_picture.as_view(),),
    path('new_product_requester/', new_product_requester.as_view()),
    path('new_product_detail/<int:pk>/', new_product_detail.as_view()),
    path('status_new_product/',status_new_product.as_view()),
    path('my_pets/', UserPetsView.as_view(), name='my_pets'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)