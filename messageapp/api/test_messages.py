from django.test import Client, TestCase

from messageapp.api.accounts import router
from messageapp.models import Message
from messageapp.test.utils import basic_auth_header, create_test_user


class MessagesTestPositive(TestCase):
    def test_create_message(self):
        """Tests positive case for message creation"""

        create_test_user("test_user_1", "tekopp1234")
        create_test_user("test_user_2", "tekopp1234")

        client = Client(router)

        response = client.post("/messages/", {
            "receiver": "test_user_2",
            "content": "hello",
        }, content_type='application/json', headers={
            **basic_auth_header("test_user_1", "tekopp1234"),
        },)

        self.assertEqual(response.status_code, 200)

    def test_delete_message(self):
        """Tests positive case for message deletion"""

        user_1 = create_test_user("test_user_1", "tekopp1234")
        user_2 = create_test_user("test_user_2", "tekopp1234")

        message = Message.objects.create(
            sender=user_1,
            receiver=user_2,
            content="Test"
        )

        client = Client(router)

        response = client.delete(f"/messages/{message.pk}", headers={
            **basic_auth_header("test_user_1", "tekopp1234"),
        },)

        self.assertEqual(response.status_code, 204)
        self.assertTrue(not Message.objects.filter(id=message.pk).exists())


class MessagesTestNegative(TestCase):
    def test_delete_nonexistend_message_returns_404(self):
        create_test_user("test_user_1", "tekopp1234")
        client = Client(router)

        response = client.delete(f"/messages/1", headers={
            **basic_auth_header("test_user_1", "tekopp1234"),
        },)

        self.assertEqual(response.status_code, 404)

    def test_delete_not_owned_message_returns_404(self):
        user_1 = create_test_user("test_user_1", "tekopp1234")
        user_2 = create_test_user("test_user_2", "tekopp1234")

        message = Message.objects.create(
            sender=user_1,
            receiver=user_2,
            content="Test"
        )
        client = Client(router)

        response = client.delete(f"/messages/{message.pk}", headers={
            **basic_auth_header("test_user_2", "tekopp1234"),
        },)

        self.assertEqual(response.status_code, 404)
