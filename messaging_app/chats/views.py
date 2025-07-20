from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Conversation, Message, User
from .serializers import ConversationSerializer, MessageSerializer
from django.shortcuts import get_object_or_404

# --------------------------
# Conversation ViewSet
# --------------------------
class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer

    def create(self, request, *args, **kwargs):
        user_ids = request.data.get('user_ids', [])
        if not user_ids or not isinstance(user_ids, list):
            return Response({"error": "user_ids must be a list of valid user IDs."}, status=status.HTTP_400_BAD_REQUEST)

        conversation = Conversation.objects.create()
        participants = User.objects.filter(user_id__in=user_ids)
        conversation.participants.set(participants)
        conversation.save()

        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

# --------------------------
# Message ViewSet
# --------------------------
class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def create(self, request, *args, **kwargs):
        conversation_id = request.data.get('conversation')
        message_body = request.data.get('message_body')
        sender_id = request.data.get('sender')

        if not all([conversation_id, message_body, sender_id]):
            return Response({"error": "conversation, message_body, and sender are required."}, status=status.HTTP_400_BAD_REQUEST)

        conversation = get_object_or_404(Conversation, pk=conversation_id)
        sender = get_object_or_404(User, pk=sender_id)

        message = Message.objects.create(
            conversation=conversation,
            sender=sender,
            message_body=message_body
        )

        serializer = self.get_serializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

