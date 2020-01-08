from django import forms
from django.utils import timezone

from messaging.models import Message


class MessageForm(forms.Form):
    """
    Compose form for user to user messaging
    """
    recipient = forms.TypedMultipleChoiceField(label='Recipient')
    subject = forms.CharField(label='Subject', max_length=130)
    body = forms.CharField(label='Body', widget=forms.Textarea(
        attrs={'rows': 15, 'cols': 50}
    ))

    def save(self, sender, parent_message=None):
        recipients = self.cleaned_data['recipient']
        subject = self.cleaned_data['subject']
        body = self.cleaned_data['body']

        message_list = []
        for recipient in recipients:
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

