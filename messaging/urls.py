from django.urls import path

from messaging.views import (undelete, delete, message_view,
                             reply, compose, mailbox, inbox_outbox_trash)

messaging_patterns = [
    path('mailbox/', mailbox, name='messages_mailbox'),
    path('inbox/', inbox_outbox_trash, {'key': 'inbox'}, name='messages_inbox'),
    path('outbox/', inbox_outbox_trash, {'key': 'outbox'}, name='messages_outbox'),
    path('compose/', compose, name='messages_compose'),
    path('compose/<recipient>/', compose, name='messages_compose_to'),
    path('reply/<message_id>/', reply, name='messages_reply'),
    path('view/<message_id>/', message_view, name='messages_detail'),
    path('delete/<message_id>/', delete, name='messages_delete'),
    path('undelete/<message_id>/', undelete, name='messages_undelete'),
    path('trash/', inbox_outbox_trash, {'key': 'trash'}, name='messages_trash'),

]
