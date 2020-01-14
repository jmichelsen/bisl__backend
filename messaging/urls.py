from django.urls import path

from messaging.views import *

messaging_patterns = [
    path('mailbox/', mailbox, name='messages_mailbox'),
    path('inbox/', inbox, name='messages_inbox'),
    path('outbox/', outbox, name='messages_outbox'),
    path('compose/', compose, name='messages_compose'),
    path('compose/<recipient>/', compose, name='messages_compose_to'),
    path('reply/<message_id>/', reply, name='messages_reply'),
    path('view/<message_id>/', message_view, name='messages_detail'),
    path('delete/<message_id>/', delete, name='messages_delete'),
    path('undelete/<message_id>/', undelete, name='messages_undelete'),
    path('trash/', trash, name='messages_trash'),

]
