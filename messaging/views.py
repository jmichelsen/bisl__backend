from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils import timezone

from messaging.forms import MessageForm
from messaging.models import Message, inbox_count
from messaging.utils import format_reply


@login_required
def mailbox(request):

    """View to show all mailboxes"""

    template_name = 'messaging/mailbox.html'
    return render(request, template_name, {'inbox_count': inbox_count(user=request.user)})


@login_required
def inbox_outbox_trash(request, key):

    """Views for Inbox OR Outbox OR Trash"""

    if key == 'inbox':
        message_list = Message.objects.inbox_for(request.user)
        template_name = 'messaging/inbox.html'
        return render(request, template_name, {'message_list': message_list})
    elif key == 'outbox':
        message_list = Message.objects.outbox_for(request.user)
        template_name = 'messaging/outbox.html'
        return render(request, template_name, {'message_list': message_list})
    elif key == 'trash':
        message_list = Message.objects.trash_for(request.user)
        template_name = 'messaging/trash.html'
        return render(request, template_name, {'message_list': message_list})


@login_required
def compose(request):

    """Form to compose a new message"""

    template_name = 'messaging/compose.html'
    form_class = MessageForm

    if request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid():
            form.save(sender=request.user)
            messages.info(request, 'Message sent successfully', extra_tags='sent')
            success_url = reverse_lazy('messaging:messages_outbox')
            return redirect(success_url)
    else:
        form = form_class()
    return render(request, template_name, {'form': form})


@login_required
def reply(request, message_id):

    """Form to reply to a message"""

    template_name = 'messaging/compose.html'
    user = request.user
    success_url = reverse_lazy('messaging:messages_inbox')
    form_class = MessageForm
    parent = get_object_or_404(Message, id=message_id)
    subject_template = 'Re: ' + parent.subject

    if parent.sender != user and parent.recipient != user:
        raise Http404

    if request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid():
            form.save(sender=user, parent_message=parent)
            messages.info(request, 'Reply successfully sent', extra_tags='reply')
            return redirect(success_url)
    else:
        form = form_class(initial={
            'body': format_reply(parent.sender.username, parent.body),
            'subject': subject_template,
            'recipient': parent.sender,
        })
    return render(request, template_name, {'form': form})


@login_required
def delete(request, message_id):

    """Marks a message deleted by sender OR recipient, but not removed completely, so the user
    is able to retrieve it still to undelete."""

    success_url = None
    user = request.user
    now = timezone.now()
    message = get_object_or_404(Message, id=message_id)
    deleted = False

    if success_url is None:
        success_url = reverse_lazy('messaging:messages_inbox')
    if 'next' in request.GET:
        success_url = request.GET['next']
    if message.sender == user:
        message.sender_deleted_at = now
        deleted = True
    if message.recipient == user:
        message.recipient_deleted_at = now
        deleted = True
    if deleted:
        message.save()
        messages.info(request, 'Message successfully deleted.', extra_tags='delete')
        return redirect(success_url)
    raise Http404


@login_required
def undelete(request, message_id):

    """Recovers a message from the trash"""

    success_url = None
    user = request.user
    message = get_object_or_404(Message, id=message_id)
    undeleted = False

    if success_url is None:
        success_url = reverse_lazy('messaging:messages_inbox')
    if 'next' in request.GET:
        success_url = request.GET['next']
    if message.sender == user:
        message.sender_deleted_at = None
        undeleted = True
    if message.recipient == user:
        message.recipient_deleted_at = None
        undeleted = True
    if undeleted:
        message.read_at = None
        message.save()
        messages.info(request, 'Message successfully recovered.', extra_tags='undelete')
        return redirect(success_url)
    raise Http404


@login_required
def message_view(request, message_id):

    """Shows a single message. Only the user is allowed to see. """

    form_class = MessageForm
    template_name = 'messaging/view.html'
    user = request.user
    now = timezone.now()
    message = get_object_or_404(Message, id=message_id)
    subject_template = 'Re: ' + message.subject

    if message.sender != user and message.recipient != user:
        raise Http404
    if message.read_at is None and message.recipient == user:
        message.read_at = now
        message.save()

    context = {'message': message, 'reply_form': None}
    if message.recipient == user:
        form = form_class(initial={
            'body': format_reply(message.sender.username, message.body),
            'subject': subject_template,
            'recipient': message.sender
        })
        context['reply_form'] = form
    return render(request, template_name, context)
