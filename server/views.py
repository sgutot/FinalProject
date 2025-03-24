from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render


from .serializers import UserSerializer, PetSerializer, ProductSerializer
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework import generics
from django.contrib.auth.models import User
from .models import Pet, Product
from rest_framework.views import APIView

import re

from django.shortcuts import get_object_or_404

@api_view(['POST'])
def login(request):
    user= get_object_or_404(User, username=request.data['username'])
    if not user.check_password(request.data['password']):
        return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
    token, created = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(instance=user)
    return Response({"token": token.key, "user": serializer.data})

@api_view(['POST'])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user = User.objects.get(username=request.data['username'])
        user.set_password(request.data['password'])
        user.save()
        token = Token.objects.create(user=user)
        return Response({"token": token.key, "user": serializer.data})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated

@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def test_token(request):
    return Response("passed for {}".format(request.user.email))


class create_pet(generics.ListCreateAPIView):
    serializer_class = PetSerializer

    def get_queryset(self):
        queryset = Pet.objects.all()
        User = self.request.query_params.get('User')
        if User is not None:
            queryset = queryset.filter(User)
        return queryset


class pet_detail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PetSerializer
    queryset = Pet.objects.all()
    lookup_field = 'pk'

class petImage(APIView):
    def get(self, request, *args, **kwargs):
        uploads = Pet.objects.all()
        serializer = PetSerializer(uploads, context = {'request':request}, many=True)
        return Response(serializer.data, status = status.HTTP_200_OK)
    
class product_name(generics.ListCreateAPIView):
    serializer_class = ProductSerializer   
    queryset = Product.objects.all()    

class product_frontPicture(APIView):
    def get(self, request, *args, **kwargs):
        uploads = Product.objects.all
        serializer= ProductSerializer(uploads, context = {'request':request}, many=True)
        return Response(serializer.data, status = status.HTTP_200_OK)

#  ~^0^~
def search_for_toxic_ingredients(product_ingredients):
    toxic_lists = []

    for toxic in toxic_ingredients:
        pattern = re.compile(r'toxic_lists')
        if pattern.search(product_ingredients):
            toxic_lists.append(toxic)

    return toxic_lists




    
    

        

