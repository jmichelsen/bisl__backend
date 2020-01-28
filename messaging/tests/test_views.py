from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from fixtureless.factory import create

from messaging.models import Message
from messaging.utils import format_reply


class TestMessageViews(TestCase):
    def setUp(self):
        super().setUp()
        self.user1 = get_user_model().objects.create(username='user1')
        self.user2 = get_user_model().objects.create(username='user2')
        self.form = create(Message, {'sender': self.user1,
                                     'recipient': self.user2,
                                     'subject': 'test_subject',
                                     'body': 'test_body'})
        self.client = Client()

    def test_inbox(self):
        self.client.force_login(user=self.user2)
        response = self.client.get(reverse('messaging:messages_inbox'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('messaging/inbox.html')
        self.assertEqual(len(response.context['message_list']), 1)

    def test_outbox(self):
        self.client.force_login(user=self.user1)
        response = self.client.get(reverse('messaging:messages_outbox'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('messaging/outbox.html')
        self.assertEqual(len(response.context['message_list']), 1)

    def test_trash(self):
        self.client.force_login(user=self.user2)
        response = self.client.get(reverse('messaging:messages_trash'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('messaging/trash.html')

    def test_compose_message(self):
        self.client.force_login(user=self.user1)
        response = self.client.post(reverse('messaging:messages_outbox'),
                                    {'subject': self.form.subject,
                                     'recipient': self.form.recipient})
        self.assertEqual(response.status_code, 200)

    def test_reply(self):
        self.client.force_login(user=self.user2)
        response = self.client.get(reverse('messaging:messages_inbox'))
        self.assertEqual(response.status_code, 200)
        pk = getattr(response.context['message_list'][0], 'pk')

        response = self.client.get(reverse('messaging:messages_reply',
                                           kwargs={'message_id': pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('messaging/compose.html')
        self.assertEqual(response.context['form'].initial['body'],
                         format_reply(self.user1, self.form.body))






