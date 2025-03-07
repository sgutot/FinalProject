from rest_framework import serializers
from .models import User, Pet

class UserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = User
        fields = ['id', 'username', 'password', 'email']


class PetSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Pet
        fields = ('__all__')