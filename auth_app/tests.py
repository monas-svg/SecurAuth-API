from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient


class AuthApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_register_and_login_flow(self):
        payload = {
            "username": "alice",
            "email": "alice@example.com",
            "password": "SecurePass123!",
            "first_name": "Alice",
            "last_name": "Tester",
        }

        register_response = self.client.post(reverse("register"), payload, format="json")
        self.assertEqual(register_response.status_code, 201)
        self.assertIn("tokens", register_response.json())

        login_response = self.client.post(
            reverse("login"),
            {"email": "alice@example.com", "password": "SecurePass123!"},
            format="json",
        )

        self.assertEqual(login_response.status_code, 200)
        self.assertIn("tokens", login_response.json())
        self.assertIn("access", login_response.json()["tokens"])
        self.assertIn("refresh", login_response.json()["tokens"])
