from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    # first_name = models.CharField(max_length=100,blank=False,null=False)
    # last_name = models.CharField(max_length=100)
    # password = models.CharField(max_length=100,null =False)
    # created_at = models.DateTimeField(auto_now_add=True)
    # the fields are available in the abstract USER CLASS SO INSTEAD OF CREATING A MOEL CLASS WE CAN JUST EXTEND AN ABSTARCT USER CLASS WHICH DEFINES ALL THE REUSED ATTRIBUTE
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=11,blank=False,null=False)
    updated_at = models.DateTimeField(auto_now=True)
