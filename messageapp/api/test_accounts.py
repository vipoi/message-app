from django.test import Client, TestCase

from messageapp.api.accounts import router
from messageapp.test.utils import basic_auth_header, create_test_user


class AccountTestPositive(TestCase):
    def test_create_account(self):
        client = Client(router)

        response = client.post("/accounts/", {
            "username": "test_user",
            "email": "user@example.com",
            "password": "tekopp1234",
            "password_confirm": "tekopp1234"
        }, content_type="application/json")

        self.assertEqual(response.status_code, 201)

        json = response.json()

        self.assertIsNotNone(json["created_at"])
        self.assertEqual(json["username"], "test_user")

    def test_get_me(self):
        create_test_user("test_user", "tekopp1234")

        client = Client(router)

        response = client.get("/accounts/me/", headers={
            **basic_auth_header("test_user", "tekopp1234")
        })

        self.assertEqual(response.status_code, 200)

        json = response.json()
        self.assertIsNotNone(json["created_at"])
        self.assertEqual(json["username"], "test_user")
