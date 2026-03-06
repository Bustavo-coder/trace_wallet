from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from user.models import User


class TestSignUp(TestCase):
    def setUp(self):
        self.url_register = reverse("register")
        self.url_login = reverse("login")

    def test_signup_returns_201(self):
        data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "abdbasitegberongbe@gmail.com",
        "password": "1234567",
        "username" : "john",
        "phone" : "08121844363",
        }

        response = self.client.post(self.url_register, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)


    def test_signup_returns_400(self):
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "abdbasitegberongbe.com",
            "password": "1234567",
            "username": "john",
            "phone": "pass",
        }
        response = self.client.post(self.url_register, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)



class TestLogin(TestCase):
    def setUp(self):
        self.url_register = reverse("register")
        self.url_login = reverse("login")
        self.data = {
                "first_name": "John",
                "last_name": "Doe",
                "email": "abdbasitegberongbe@gmail.com",
                "password": "Password123",
                "username": "john",
                "phone": "08121844363",
        }
    def test_login_returns_200(self):
        self.client.post(self.url_register, self.data, format="json")
        login_data = {
            "email": self.data["email"],
            "password": self.data["password"],
        }
        response = self.client.post(self.url_login, login_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_returns_400(self):
        login_data = {
            "email": "abdbasitegberongbe.com",
            "password": "invalid password",
        }
        response = self.client.post(self.url_login, login_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
