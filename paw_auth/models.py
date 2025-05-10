from django.db import models

class User(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField(max_length=254)
    contact = models.CharField(max_length=20)

class Pet(models.Model):
    name = models.CharField(max_length=30)
    type = models.CharField(max_length=30)
    DisplayIcon = models.ImageField(upload_to ='uploads/')
    
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=30)
    numGrams = models.IntegerField() 
    manufacturer = models.CharField(max_length=300)
    ingredients = models.CharField(max_length=300)
    frontPicture = models.ImageField(upload_to ='uploads/')
    backPicture = models.ImageField(upload_to ='uploads/')
   

class ProductRequest(models.Model):
    name = models.CharField(max_length=30)
    descrption = models.CharField(max_length=300)
    frontPicture =  models.ImageField(upload_to ='uploads/')
    ingredientsPicture =  models.ImageField(upload_to ='uploads/')
    requester = models.CharField(max_length=30)
    requestDate = models.IntegerField() 
    PENDING = "PD"
    APPROVE = "AP"
    DENIED = "DD"
    STATUS = {
        PENDING: "Pending",
        APPROVE: "Approve",
        DENIED: "Denied"
    }
    status = models.CharField(max_length=30)