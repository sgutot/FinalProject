from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.models import User
from .models import Pet, ProductRequest
from django.core.files.uploadedfile import SimpleUploadedFile
import io
from PIL import Image

class UserAuthTests(APITestCase):
    def setUp(self):
        self.signup_url = reverse('signup')
        self.login_url = reverse('login')
        self.test_user = {
            "username": "shubd@gmail.com",
            "email": "shubd@gmail.com",
            "password": "Ud8Aub_9"
        }

    def test_user_signup(self):
        response = self.client.post(self.signup_url, self.test_user)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)

    def test_user_login_valid(self):
        self.client.post(self.signup_url, self.test_user)
        response = self.client.post(self.login_url, {
            "username": self.test_user["username"],
            "password": self.test_user["password"]
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)

    def test_user_login_invalid_email(self):
        response = self.client.post(self.login_url, {
            "username": "wronguser@gmail.com",
            "password": self.test_user["password"]
        })
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class PetTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="tester", password="Test1234")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.pet_url = reverse('create_pet')

    def generate_test_image(self, name='pet.jpg'):
        file = io.BytesIO()
        image = Image.new('RGB', (100, 100))
        image.save(file, 'jpeg')
        file.seek(0)
        return SimpleUploadedFile(name, file.read(), content_type='image/jpeg')

    def test_add_pet_successfully(self):
        image = self.generate_test_image()
        data = {
            "name": "Choco",
            "type": "Dog",
            "DisplayIcon": image
        }
        response = self.client.post(self.pet_url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_add_pet_without_name(self):
        image = self.generate_test_image()
        data = {
            "type": "Cat",
            "DisplayIcon": image
        }
        response = self.client.post(self.pet_url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ProductRequestTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="tester2", password="Pass1234")
        self.client.force_authenticate(user=self.user)
        self.product_url = reverse('new_product_name') 

    def generate_test_image(self, name='test.jpg'):
        file = io.BytesIO()
        image = Image.new('RGB', (100, 100))
        image.save(file, 'jpeg')
        file.seek(0)
        return SimpleUploadedFile(name, file.read(), content_type='image/jpeg')

    def test_add_new_product_request(self):
        front_img = self.generate_test_image('front.jpg')
        ingredients_img = self.generate_test_image('ingredients.jpg')

        data = {
            "name": "Rebisco",
            "descrption": "HEHE",
            "frontPicture": front_img,
            "ingredientsPicture": ingredients_img,
            "requester": "tester2",
            "requestDate": 20250425,
            "status": "PD"
        }
        response = self.client.post(self.product_url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


from rest_framework.test import APITestCase

class ScanTests(APITestCase):
    def test_scan_known_product(self):
        product_ingredients = "Water, Sodium Lauryl Sulfate, Alcohol"
        toxic_ingredients = ["Sodium Lauryl Sulfate", "Parabens", "Phthalates"]

        from .views import search_for_toxic_ingredients

        result = search_for_toxic_ingredients(product_ingredients, toxic_ingredients)
        
        self.assertIsInstance(result, list)
        self.assertIn("Sodium Lauryl Sulfate", result)
