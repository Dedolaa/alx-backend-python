from django.urls import path, include
<<<<<<< HEAD
from rest_framework import routers
=======
from rest_framework import routers, DefaultRouter
>>>>>>> cc12cea (new changes)
router = routers.DefaultRouter()
from .views import ConversationViewSet, MessageViewSet

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

<<<<<<< HEAD
urlpatterns = router.urls + convo_router.urls
=======
urlpatterns = router.urls + convo_router.urls
>>>>>>> cc12cea (new changes)
