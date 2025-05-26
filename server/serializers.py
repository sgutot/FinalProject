from rest_framework import serializers
# from django.contrib.auth.models import User
from .models import Pet, Product, ProductRequest, User
from rest_framework import status
from rest_framework.response import Response


class UserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = User
        fields = ['id', 'username', 'password', 'email']


class PetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pet
        fields = '__all__'
        read_only_fields = ['id', 'owner', 'created_at']

    def create(self, validated_data):
        request = self.context.get('request')
        if request is None or not hasattr(request, 'user'):
            raise serializers.ValidationError("Request with authenticated user is required.")

        validated_data['owner'] = request.user
        return super().create(validated_data)



class ProductSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Product 
        fields = ('__all__')


class ProductRequestSerializer(serializers.ModelSerializer):
    requestDate  = serializers.DateTimeField(format="%d-%m-%Y")
    class Meta(object):
        model = ProductRequest
        fields = ('name', 'descrption', 'frontPicture', 'ingredientsPicture', 'requester', 'requestDate')
        read_only_fields = ['id', 'requestDate', 'status']

        def get_front_photo_urls(self, obj):
            request = self.context.get('request')
            photo_url = obj.fingerprint.url
            return request.build_absolute_uri(photo_url)
        
        def get_ingredients_photo_urls(self, obj):
            request = self.context.get('request')
            photo_url = obj.fingerprint.url
            return request.build_absolute_uri(photo_url)
            
        
