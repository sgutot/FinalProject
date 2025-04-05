from django.contrib import admin
from .models import User, Pet, Product, ProductRequest

admin.site.register(User)
admin.site.register(Pet)
admin.site.register(Product)
admin.site.register(ProductRequest)