from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils import timezone

from messaging.forms import MessageForm
from messaging.models import Message

User = get_user_model()


@login_required
def inbox(request):

    """Display a list of received messages for the current user"""

    template_name = 'messaging/inbox.html'
    message_list = Message.objects.inbox_for(request.user)
    return render(request, template_name, {'message_list': message_list})


@login_required
def outbox(request):

    """Display a list of sent messages for the current user"""

    template_name = 'messaging/outbox.html'
    message_list = Message.objects.outbox_for(request.user)
    return render(request, template_name, {'message_list': message_list})


@login_required
def trash(request):

    """Display a list of received messages for the user"""

    template_name = 'messaging/trash.html'
    message_list = Message.objects.trash_for(request.user)
    return render(request, template_name, {'message_list': message_list})


@login_required
def compose(request):

    """Form to compose a new message"""

    template_name = 'messaging/compose.html'
    form_class = MessageForm
    success_url = None

    if request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid():
            form.save(sender=request.user)
            messages.info(request, 'Message sent successfully')
            if success_url is None:
                success_url = reverse('messaging:inbox')
            if 'next' in request.GET:
                success_url = request.GET['next']
            return HttpResponseRedirect(success_url)
    else:
        form = form_class(initial={'subject': request.GET.get('subject', '')})
    return render(request, template_name, {'form': form})


@login_required()
def reply(request, message_id):

    """Form to reply to a message"""

    template_name = 'messaging/compose.html'
    form_class = MessageForm
    success_url = None
    subject_template = 'Re: '

    parent = get_object_or_404(Message, id=message_id)

    if parent.sender != request.user and parent.recipient != request.user:
        raise Http404

    if request.method == 'POST':

        form = form_class(request.POST)
        if form.is_valid():
            form.save(sender=request.user, parent_message=parent)
            messages.info(request, 'Reply successfully sent')
            if success_url is None:
                success_url = reverse('messaging:inbox')
            return HttpResponseRedirect(success_url)
        else:
            form = form_class(initial={
                'body': {parent.sender, parent.body},
                'subject': subject_template,
                'recipient': [parent.sender, ]
            })
        return render(request, template_name, {
            'form': form
        })


@login_required
def delete(request, message_id):

    """Marks a message deleted by sender OR recipient, but not removed completely
    until both users delete it"""

    success_url = None
    user = request.user
    now = timezone.now()
    message = get_object_or_404(Message, id=message_id)
    deleted = False

    if success_url is None:
        success_url = reverse('messaging:inbox')
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
        messages.info(request, 'Message successfully deleted.')
        return HttpResponseRedirect(success_url)
    raise Http404


@login_required
def undelete(request, message_id):

    """Recovers a message from the trash"""

    success_url = None
    user = request.user
    message = get_object_or_404(Message, id=message_id)
    un_deleted = False

    if success_url is None:
        success_url = reverse('messaging:inbox')
    if 'next' in request.GET:
        success_url = request.GET['next']
    if message.sender == user:
        message.sender_deleted_at = None
        un_deleted = True
    if message.recipient == user:
        message.recipient_deleted_at = None
        un_deleted = True
    if un_deleted:
        message.save()
        messages.info(request, 'Message successfully recovered.')
        return HttpResponseRedirect(success_url)
    raise Http404

@login_required
def message_view(request, message_id):

    """Shows a single message. Only the user is allowed to see. """

    form_class = MessageForm
    subject_template = 'Re: '
    template_name = 'messaging/view.html'

    user = request.user
    now = timezone.now()
    message = get_object_or_404(Message, id=message_id)

    if message.sender != user and message.recipient != user:
        raise Http404
    if message.read_at is None and message.recipient is user:
        message.read_at = now
        message.save()

    context = {'message': message, 'reply_form': None}
    if message.recipient == user:
        form = form_class(initial={
            'body': {message.sender, message.body},
            'subject': subject_template,
            'recipient': [message.sender, ]
        })
        context['reply_form'] = form
    return render(request, template_name, context)
