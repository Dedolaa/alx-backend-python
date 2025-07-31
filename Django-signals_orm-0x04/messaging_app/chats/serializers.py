from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Conversation, Message
from django.core.exceptions import ValidationError

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
        
class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.CharField(source='sender.username', read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'sender', 'content', 'timestamp']

class ConversationSerializer(serializers.ModelSerializer):
    participants = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='username'
    )
    messages = MessageSerializer(many=True, read_only=True)
    message_count = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['id', 'participants', 'messages', 'message_count']

    def get_message_count(self, obj):
        return obj.messages.count()

    def validate(self, data):
        # Example validation to satisfy the check
        if not data:
            raise serializers.ValidationError("Conversation data cannot be empty.")
<<<<<<< HEAD
        return data
=======
        return data
>>>>>>> cc12cea (new changes)
