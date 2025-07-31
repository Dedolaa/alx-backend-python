from django.urls import path, include
from rest_framework import routers, DefaultRouter, NestedDefaultRouter
router = routers.DefaultRouter()
from .views import ConversationViewSet, MessageViewSet
from . import views

# Create the base router
router = DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversations')

# Create the nested router for messages under conversations
convo_router = NestedDefaultRouter(router, r'conversations', lookup='conversation')
convo_router.register(r'messages', MessageViewSet, basename='conversation-messages')

urlpatterns = [
    path('', include(router.urls)),
]

router = routers.DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversations')

convo_router = routers.NestedDefaultRouter(router, r'conversations', lookup='conversation')
convo_router.register(r'messages', MessageViewSet, basename='conversation-messages')

urlpatterns = router.urls + convo_router.urls

urlpatterns = [
    path('conversations/<int:user_id>/', views.conversation_messages, name='conversation_messages'),
]