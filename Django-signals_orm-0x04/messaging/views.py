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
    
@login_required
def send_message(request):
    if request.method == 'POST':
        receiver_id = request.POST.get('receiver')
        content = request.POST.get('content')
        parent_id = request.POST.get('parent_id')  

        receiver = get_object_or_404(User, id=receiver_id)
        parent_message = Message.objects.filter(id=parent_id).first() if parent_id else None

        Message.objects.create(
            sender=request.user,  
            receiver=receiver,    
            content=content,
            parent_message=parent_message
        )

@login_required
def unread_messages_view(request):
    unread_msgs = Message.unread.unread_for_user(request.user).only('id', 'sender', 'content', 'timestamp') 
    context = {'unread_messages': unread_msgs}
    return render(request, 'messaging/unread_messages.html', context)
