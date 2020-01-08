from django.conf.global_settings import AUTH_USER_MODEL
from django.db import models
from django.urls import reverse
from django.utils import timezone


class MessageManager(models.Manager):

    def inbox_for(self, user):
        """all messages received by given user & are not marked deleted"""

        return self.filter(recipient=user,
                           recipient_deleted_at__isnull=True)

    def outbox_for(self, user):
        """all messages sent by given user & are not deleted"""

        return self.filter(sender=user,
                           sender_deleted_at__isnull=True)

    def trash_for(self, user):
        """all deleted messages that were sent OR received"""

        return self.filter(
            recipient=user,
            recipient_deleted_at__isnull=False
        ) | self.filer(
            sender=user,
            sender_deleted_at__isnull=False
        )


class Message(models.Model):
    """
    User to User messaging system
    """

    sender = models.ForeignKey(AUTH_USER_MODEL, related_name='sent_messages',
                               verbose_name='Sender', on_delete=models.PROTECT)
    recipient = models.ForeignKey(AUTH_USER_MODEL, related_name='received_messages',
                                  null=True, blank=True, verbose_name='Recipient', on_delete=models.SET_NULL)
    subject = models.CharField('Subject', max_length=150)
    body = models.TextField('Body')
    parent_message = models.ForeignKey('self', related_name='next_messages', null=True, blank=True,
                                       verbose_name='Parent Message', on_delete=models.SET_NULL)
    sent_at = models.DateTimeField('sent at', null=True, blank=True)
    read_at = models.DateTimeField('read at', null=True, blank=True)
    replied_at = models.DateTimeField('replied at', null=True, blank=True)
    sender_deleted_at = models.DateTimeField('sender deleted at', null=True, blank=True)
    recipient_deleted_at = models.DateTimeField('recipient deleted at', null=True, blank=True)

    objects = MessageManager()

    def __str__(self):
        return self.subject

    class Meta:
        ordering = ['-sent_at']
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'

    def new(self):
        """returns whether the recipient has read message"""

        if self.read_at is not None:
            return False
        return True

    def replied(self):
        """returns whether the recipient has replied to message"""

        if self.replied_at is not None:
            return True
        return False

    def get_absolute_url(self):
        return reverse('messaging:messages_detail', args=[self.id])

    def save(self, **kwargs):
        if not self.id:
            self.sent_at = timezone.now()
        super(Message, self).save(**kwargs)


def inbox_count(user):
    """number of unread messages"""

    return Message.objects.filter(recipient=user, read_at__isnull=True, recipient_deleted_at__isnull=True).count()

