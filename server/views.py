from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render
from rest_framework import status, permissions, parsers

# Scan
from django.core.files.base import ContentFile
from django.core.files.temp import NamedTemporaryFile
from urllib.request import urlopen
from urllib.parse import urlparse
import os



from .serializers import UserSerializer, PetSerializer, ProductSerializer, ProductRequestSerializer
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework import generics, permissions, status
from django.contrib.auth.models import User
from .models import Pet, Product, ProductRequest
from rest_framework.views import APIView
from rest_framework.response import Response

import re
import requests

from django.shortcuts import get_object_or_404


# login and signup
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
 

from django.utils import timezone

class ProductRequestCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]

    def post(self, request, *args, **kwargs):
        data = request.data.copy()
        print(f"New Product Request! request data: {data}")
        data = request.data.copy()
        # data['requester'] = request.user.username
        # data['requestDate'] = timezone.now()

        serializer = ProductRequestSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Request submitted successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# # Pet
# class create_pet(generics.ListCreateAPIView):
#     serializer_class = PetSerializer

#     def get_queryset(self):
#         queryset = Pet.objects.all()
#         User = self.request.query_params.get('User')
#         if User is not None:
#             queryset = queryset.filter(User)
#         return queryset


# class pet_detail(generics.RetrieveUpdateDestroyAPIView):
#     serializer_class = PetSerializer
#     queryset = Pet.objects.all()
#     lookup_field = 'pk'


class petImage(APIView):
    def get(self, request, *args, **kwargs):
        uploads = Pet.objects.all()
        serializer = PetSerializer(uploads, context = {'request':request}, many=True)
        return Response(serializer.data, status = status.HTTP_200_OK)
    


# Product 
class product_name(generics.ListCreateAPIView):
    serializer_class = ProductSerializer   
    queryset = Product.objects.all()    


class product_frontPicture(APIView):
    def get(self, request, *args, **kwargs):
        uploads = Product.objects.all
        serializer= ProductSerializer(uploads, context = {'request':request}, many=True)
        return Response(serializer.data, status = status.HTTP_200_OK)


#  Scan
@api_view(['GET'])
def get_product(request):
    _barcode = request.query_params.get('barcode')

    if not _barcode:
        return Response({'error': 'Barcode is required.'}, status=status.HTTP_400_BAD_REQUEST)


    try:
        print(f'Fetching product: {_barcode}')
        # Check if product already exists in the Database
        product = Product.objects.get(barcode=_barcode)
        serializer = ProductSerializer(product)
        print("Fetched product from local database")
        return Response({'source' : 'local', 'product' : serializer.data})

    
    except Product.DoesNotExist:
        # OpenFoodFacts Database
        print(f"{_barcode} is not found in local database. Checking openfoodfact's database...")
        url = f"https://world.openfoodfacts.org/api/v0/product/{_barcode}.json"
        response = requests.get(url)

        # If connection fails
        if response.status_code != 200 or response.json().get("status") != 1:
            return Response({'error': 'Product not found in OpenFoodFacts.'}, status=status.HTTP_404_NOT_FOUND)
        
        
        # data = response.json()

        # product_data = data.get("product", {})
        # new_product = Product(
        #     id=product_barcode,
        #     name=product_data.get("product_name", "Unknown")
        #     numGrams=product_data.get("quantity", "0").split()[0] if product_data.get("quantity") else 0,
        #     manufacturer=product_data.get("brands", "Unknown"),
        #     ingredients=product_data.get("ingredients_text", "Unknown")
        # )

        # # Download and save front image
        # front_img_url = product_data.get("image_front_url")
        # if front_img_url:
        #     front_img_temp = NamedTemporaryFile(delete=True)
        #     front_img_temp.write(urlopen(front_img_url).read())
        #     front_img_temp.flush()
        #     new_product.frontPicture.save(os.path.basename(urlparse(front_img_url).path), ContentFile(front_img_temp.read()))

        # # Download and save back image
        # back_img_url = product_data.get("image_url")
        # if back_img_url:
        #     back_img_temp = NamedTemporaryFile(delete=True)
        #     back_img_temp.write(urlopen(back_img_url).read())
        #     back_img_temp.flush()
        #     new_product.backPicture.save(os.path.basename(urlparse(back_img_url).path), ContentFile(back_img_temp.read()))

        # new_product.save()
        # return new_product
        data = response.json().get('product', {})

        # Extract quantity
        quantity_str = data.get("quantity", "0").split()[0]
        try:
            num_grams = int(float(quantity_str))
        except ValueError:
            num_grams = 0

        # Create product instance
        new_product = Product(
            barcode=_barcode,
            name=data.get("product_name", "Unknown"),
            manufacturer=data.get("brands", "Unknown"),
            ingredients=data.get("ingredients_text", "Unknown"),
            numGrams=num_grams
        )

        # Download and save front image
        front_url = data.get("image_front_url")
        if front_url:
            with urlopen(front_url) as u:
                new_product.frontPicture.save(os.path.basename(urlparse(front_url).path), ContentFile(u.read()), save=False)

        # Download and save back image
        back_url = data.get("image_url")
        if back_url:
            with urlopen(back_url) as u:
                new_product.backPicture.save(os.path.basename(urlparse(back_url).path), ContentFile(u.read()), save=False)

        new_product.save()
        serializer = ProductSerializer(new_product)
        print("Fetched product from openfoodfacts database")
        return Response({'source': 'openfoodfacts', 'product': serializer.data})



# def search_for_toxic_ingredients(product_ingredients):
    
#     toxic_lists = []

#     for toxic in toxic_ingredients:
#         pattern = re.compile(r'toxic_lists')
#         if pattern.search(product_ingredients):
#             toxic_lists.append(toxic)

#     return toxic_lists




# New Product
class new_product_name(generics.ListCreateAPIView):
    serializer_class = ProductRequestSerializer
    queryset = ProductRequest.objects.all()
          

class new_product_description(generics.ListAPIView):
    serializer_class = ProductRequestSerializer
    queryset = ProductRequest.objects.all()


class new_product_front_picture(APIView):
    def get(self, request, *args, **kwargs):
        uploads = ProductRequest.objects.all()
        serializer = ProductRequestSerializer(uploads, context = {'request':request}, many=True)
        return Response(serializer.data, status = status.HTTP_200_OK)
    

class new_product_ingredients_picture(APIView):
    def get(self, request, *args, **kwargs):
        uploads = ProductRequest.objects.all()
        serializer = ProductRequestSerializer(uploads, context = {'request':request}, many=True)
        return Response(serializer.data, status = status.HTTP_200_OK) 
    

class new_product_requester(generics.ListAPIView):
    serializer_class = ProductRequestSerializer

    def get_queryset(self):
        queryset = ProductRequest.objects.all()
        User = self.request.query_params.get('User')
        if User is not None:
            queryset = queryset.filter(User)
        return queryset
    

class new_product_detail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProductRequestSerializer
    queryset = ProductRequest.objects.all()
    lookup_field = 'pk'


class status_new_product(generics.UpdateAPIView):
    queryset = ProductRequest.objects.all()
    serializer_class = ProductRequestSerializer
    permission_classes = [permissions.IsAdminUser]

    def approve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.status != ProductRequest.PENDING:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        instance.status = ProductRequest.APPROVE
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


from django.contrib.auth import get_user_model

class UserPetsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        print(type(request.user), request.user) 
        
        if request.user.is_authenticated:
            User = get_user_model()
            user = User.objects.get(username=str(request.user))
            pets = Pet.objects.filter(owner=user)

        else:
            pets = Pet.objects.none()

        serializer = PetSerializer(pets, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PetSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()  # owner is passed via context
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

