from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to view/edit it.
    """

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user  

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission to ensure only conversation participants can access messages.
    """

    def has_permission(self, request, view):
        # Ensure the user is authenticated
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        Called for object-level permissions.
        obj here will be a Message or Conversation instance.
        We assume the object has a `conversation` field with `participants` (many-to-many).
        """
        conversation = getattr(obj, 'conversation', None)
        if conversation and request.user in conversation.participants.all():
            return True
        return False