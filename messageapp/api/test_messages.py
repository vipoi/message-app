from django.test import TestCase
from django.test import Client
from messageapp.api.accounts import router
from messageapp.test.utils import basic_auth_header, create_test_user


class MessagesTestPositive(TestCase):
    def test_create_message(self):
        """Tests positive case for message creation"""

        create_test_user("test_user_1", "tekopp1234")
        create_test_user("test_user_2", "tekopp1234")

        client = Client(router)

        response = client.post("/messages/", {
            "username": "test_user_2",
            "content": "hello",
        }, content_type='application/json', headers={
            **basic_auth_header("test_user_1", "tekopp1234"),
        },)

        self.assertEqual(response.status_code, 200)
