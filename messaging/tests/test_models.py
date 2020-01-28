from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from messaging.models import Message


class TestMessageModel(TestCase):
    def setUp(self):
        super().setUp()
        self.user1 = get_user_model().objects.create(username='user1')
        self.user2 = get_user_model().objects.create(username='user2')
        self.msg1 = Message(sender=self.user1, recipient=self.user2,
                            subject='test_subject', body='test_body')
        self.msg1.save()

    def test_str(self):
        """
        Test the __str__ output is equal to the Message.subject value
        """

        expected = 'test_subject'
        actual = Message.objects.get(subject='test_subject').__str__()
        self.assertEqual(expected, actual)

    def test_inbox_for(self):
        """
        Test recipient inbox count is equal to 1
        """
        self.assertEqual(Message.objects.inbox_for(self.user2).count(), 1)
        self.assertEqual(Message.objects.inbox_for(self.user2)[0].subject,
                         'test_subject')

        # if message is marked as read, it stays in the inbox
        self.msg1.read_at = timezone.now()
        self.assertEqual(Message.objects.inbox_for(self.user2).count(), 1)

    def test_outbox_for(self):
        """
        Test Sender outbox count is equal to 1
        """
        self.assertEqual(Message.objects.outbox_for(self.user1).count(), 1)
        self.assertEqual(Message.objects.outbox_for(self.user1)[0].subject,
                         'test_subject')

    def test_trash(self):

        # If only one user deletes a message, it stays in database
        self.msg1.sender_deleted_at = timezone.now()
        self.msg1.save()
        self.assertEqual(Message.objects.trash_for(self.user1).count(), 1)

        # If both users delete the same message, it deletes from database
        self.msg1.recipient_deleted_at = timezone.now()
        self.msg1.save()
        self.assertEqual(Message.objects.trash_for(self.user2).count(), 0)
        self.assertEqual(Message.objects.trash_for(self.user1).count(), 0)

    def test_new_message(self):

        # Message marked as read IS NOT new
        self.msg1.read_at = timezone.now()
        self.msg1.save()
        self.assertFalse(self.msg1.new())

        # Message not marked as read IS new
        self.msg1.read_at = None
        self.msg1.save()
        self.assertTrue(self.msg1.new())



