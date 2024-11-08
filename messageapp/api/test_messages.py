from django.utils import timezone
from django.test import Client, TestCase

from messageapp.api.accounts import router
from messageapp.models import Message
from messageapp.test.utils import basic_auth_header, create_test_message, create_test_user


class MessagesTestPositive(TestCase):
    def test_create_message(self):
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

    def test_list_messages(self):
        user_1 = create_test_user("test_user_1", "tekopp1234")
        user_2 = create_test_user("test_user_2", "tekopp1234")

        message_1 = create_test_message(user_1, user_2, "First Message")
        message_2 = create_test_message(user_2, user_1, "Second Message")
        message_3 = create_test_message(user_1, user_2, "Third Message")

        client = Client(router)

        response = client.get("/messages/", content_type='application/json', headers={
            **basic_auth_header("test_user_1", "tekopp1234"),
        },)

        json = response.json()
        self.assertEqual(len(json), 3)

        self.assertEqual(json[0]['sender'], "test_user_1")
        self.assertEqual(json[0]['receiver'], "test_user_2")
        self.assertEqual(json[0]['content'], "First Message")
        self.assertEqual(json[0]['id'], message_1.id)
        self.assertIsNotNone(json[0]['created_at'])

        self.assertEqual(json[1]['sender'], "test_user_2")
        self.assertEqual(json[1]['receiver'], "test_user_1")
        self.assertEqual(json[1]['content'], "Second Message")
        self.assertEqual(json[1]['id'], message_2.id)
        self.assertIsNotNone(json[1]['created_at'])

        self.assertEqual(json[2]['sender'], "test_user_1")
        self.assertEqual(json[2]['receiver'], "test_user_2")
        self.assertEqual(json[2]['content'], "Third Message")
        self.assertEqual(json[2]['id'], message_3.id)
        self.assertIsNotNone(json[2]['created_at'])

        self.assertEqual(response.status_code, 200)

    def test_list_messages_filter(self):
        user_1 = create_test_user("test_user_1", "tekopp1234")
        user_2 = create_test_user("test_user_2", "tekopp1234")
        user_3 = create_test_user("test_user_3", "tekopp1234")

        create_test_message(user_2, user_1)
        create_test_message(user_1, user_2)
        create_test_message(user_2, user_1)

        create_test_message(user_3, user_1)
        user_3_message_2 = create_test_message(user_1, user_3)
        user_3_message_3 = create_test_message(user_1, user_3)

        client = Client(router)

        response = client.get("/messages/?limit=2&offset=1&username=test_user_3", content_type='application/json', headers={
            **basic_auth_header("test_user_1", "tekopp1234"),
        },)

        json = response.json()

        self.assertEqual(len(json), 2)

        self.assertEqual(json[0]['id'], user_3_message_2.id)
        self.assertEqual(json[1]['id'], user_3_message_3.id)

        self.assertEqual(response.status_code, 200)

    def test_list_messages_filter_read(self):
        user_1 = create_test_user("test_user_1", "tekopp1234")
        user_2 = create_test_user("test_user_2", "tekopp1234")

        create_test_message(user_2, user_1, read_at=timezone.now())
        message_2 = create_test_message(user_2, user_1)

        client = Client(router)

        response = client.get("/messages/?only_unread=true&username=test_user_2", content_type='application/json', headers={
            **basic_auth_header("test_user_1", "tekopp1234"),
        },)

        json = response.json()

        self.assertEqual(len(json), 1)

        self.assertEqual(json[0]['id'], message_2.id)
        self.assertEqual(response.status_code, 200)

    def test_delete_message(self):
        user_1 = create_test_user("test_user_1", "tekopp1234")
        user_2 = create_test_user("test_user_2", "tekopp1234")

        message = create_test_message(user_1, user_2)

        client = Client(router)

        response = client.delete(f"/messages/{message.pk}", headers={
            **basic_auth_header("test_user_1", "tekopp1234"),
        },)

        self.assertEqual(response.status_code, 204)
        self.assertTrue(not Message.objects.filter(id=message.pk).exists())

    def test_mark_as_read(self):
        user_1 = create_test_user("test_user_1", "tekopp1234")
        user_2 = create_test_user("test_user_2", "tekopp1234")

        message = create_test_message(user_1, user_2)

        client = Client(router)

        response = client.patch(f"/messages/{message.id}/mark_as_read", headers={
            **basic_auth_header("test_user_2", "tekopp1234"),
        })

        self.assertEqual(response.status_code, 204)

        updated_message = Message.objects.filter(id=message.pk).get()
        self.assertIsNotNone(updated_message.read_at)


class MessagesTestNegative(TestCase):
    def test_delete_nonexistend_message_returns_404(self):
        create_test_user("test_user_1", "tekopp1234")
        client = Client(router)

        response = client.delete(f"/messages/1", headers={
            **basic_auth_header("test_user_1", "tekopp1234"),
        },)

        self.assertEqual(response.status_code, 404)

    def test_delete_unowned_message_returns_404(self):
        user_1 = create_test_user("test_user_1", "tekopp1234")
        user_2 = create_test_user("test_user_2", "tekopp1234")

        message = create_test_message(user_1, user_2)
        client = Client(router)

        response = client.delete(f"/messages/{message.pk}", headers={
            **basic_auth_header("test_user_2", "tekopp1234"),
        },)

        self.assertEqual(response.status_code, 404)

    def test_mark_unowned_message_as_read_returns_404(self):
        user_1 = create_test_user("test_user_1", "tekopp1234")
        user_2 = create_test_user("test_user_2", "tekopp1234")
        create_test_user("test_user_3", "tekopp1234")
        message = create_test_message(user_1, user_2)

        client = Client(router)

        response = client.patch(f"/messages/{message.id}/mark_as_read", headers={
            **basic_auth_header("test_user_3", "tekopp1234"),
        })

        self.assertEqual(response.status_code, 404)
