from django.urls import path

from messaging.views import (undelete, delete, message_view,
                             reply, compose, mailbox, inbox_outbox_trash)

messaging_patterns = [
    path('mailbox/', mailbox, name='messages_mailbox'),
    path('inbox/', inbox_outbox_trash, {'key': 'inbox'}, name='messages_inbox'),
    path('outbox/', inbox_outbox_trash, {'key': 'outbox'}, name='messages_outbox'),
    path('compose/', compose, name='messages_compose'),
    path('reply/<int:message_id>/', reply, name='messages_reply'),
    path('view/<int:message_id>/', message_view, name='messages_detail'),
    path('delete/<int:message_id>/', delete, name='messages_delete'),
    path('undelete/<int:message_id>/', undelete, name='messages_undelete'),
    path('trash/', inbox_outbox_trash, {'key': 'trash'}, name='messages_trash'),

]
