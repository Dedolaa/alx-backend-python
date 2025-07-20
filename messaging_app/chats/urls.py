from django.urls import path, include
from rest_framework import routers
router = routers.DefaultRouter()
from .views import ConversationViewSet, MessageViewSet

router = DefaultRouter()
router.register(r'conversations', ConversationViewSet)
router.register(r'messages', MessageViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

router = routers.DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversations')

convo_router = routers.NestedDefaultRouter(router, r'conversations', lookup='conversation')
convo_router.register(r'messages', MessageViewSet, basename='conversation-messages')

urlpatterns = router.urls + convo_router.urls
