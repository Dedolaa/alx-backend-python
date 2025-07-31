from django.shortcuts import render
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .models import Message

@login_required
def delete_user(request):
    user = request.user
    user.delete()
    return redirect('home')

@login_required
def unread_messages_view(request):
    unread_msgs = Message.unread.for_user(request.user)
    return render(request, 'messaging/unread_inbox.html', {'messages': unread_msgs})