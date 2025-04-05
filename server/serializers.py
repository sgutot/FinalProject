from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Pet, Product, ProductRequest
from rest_framework import status
from rest_framework.response import Response

class UserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = User
        fields = ['id', 'username', 'password', 'email']


class PetSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Pet
        fields = ('__all__')

        def get_photo_urls(self, obj):
            request = self.context.get('request')
            photo_url = obj.fingerprint.url
            return request.build_absolute_uri(photo_url)  

class ProductSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Product 
        fields = ('__all__')

class ProductRequestSerializer(serializers.ModelSerializer):
    requestDate  = serializers.DateTimeField(format="%d-%m-%Y")
    class Meta(object):
        model = ProductRequest
        fields = ('name', 'descrption', 'frontPicture', 'ingredientsPicture', 'requester', 'requestDate')

        def get_front_photo_urls(self, obj):
            request = self.context.get('request')
            photo_url = obj.fingerprint.url
            return request.build_absolute_uri(photo_url)
        
        def get_ingredients_photo_urls(self, obj):
            request = self.context.get('request')
            photo_url = obj.fingerprint.url
            return request.build_absolute_uri(photo_url)
            
        
