from django import forms
from django.contrib.auth import get_user_model
from django.utils import timezone

from messaging.models import Message


User = get_user_model()


class MessageForm(forms.Form):
    """
    Compose & Reply form for user to user messaging
    """
    recipient = forms.ModelChoiceField(label='Recipient', queryset=User.objects.all())
    subject = forms.CharField(label='Subject', max_length=130)
    body = forms.CharField(label='Body', widget=forms.Textarea(
        attrs={'rows': 15, 'cols': 70}
    ))

    def save(self, sender, parent_message=None):
        recipient = self.cleaned_data['recipient']
        subject = self.cleaned_data['subject']
        body = self.cleaned_data['body']

        message_list = []
        message = Message(
            sender=sender,
            recipient=recipient,
            subject=subject,
            body=body,
        )

        if parent_message is not None:
            message.parent_message = parent_message
            parent_message.replied_at = timezone.now()
            parent_message.save()
        message.save()
        message_list.append(message)
        return message_list

