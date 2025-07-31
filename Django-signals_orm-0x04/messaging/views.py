from django.shortcuts import render, get_object_or_404
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

def get_threaded_replies(message):
    replies = Message.objects.filter(parent_message=message).select_related('sender', 'receiver')
    result = []
    for reply in replies:
        result.append({
            'message': reply,
            'replies': get_threaded_replies(reply)
        })
    return result

@login_required
def message_thread_view(request, message_id):
    original_message = get_object_or_404(
        Message.objects.select_related('sender', 'receiver', 'parent_message'),
        id=message_id,
        receiver=request.user  # ⬅ required check
    )

    # Get all threaded replies
    thread = get_threaded_replies(original_message)

    context = {
        'original_message': original_message,
        'thread': thread,
    }
    return render(request, 'messaging/thread.html', context)
    
