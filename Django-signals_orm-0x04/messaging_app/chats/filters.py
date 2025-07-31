import django_filters
from .models import Message

class MessageFilter(django_filters.FilterSet):
    created_at__gte = django_filters.DateTimeFilter(field_name="created_at", lookup_expr='gte')
    created_at__lte = django_filters.DateTimeFilter(field_name="created_at", lookup_expr='lte')
    user = django_filters.CharFilter(field_name="sender__username", lookup_expr='icontains')

    class Meta:
        model = Message
        fields = ['user', 'created_at__gte', 'created_at__lte']

class MessageFilter(django_filters.FilterSet):
    sender = django_filters.CharFilter(field_name='sender__username', lookup_expr='icontains')
    recipient = django_filters.CharFilter(field_name='recipient__username', lookup_expr='icontains')
    timestamp = django_filters.DateFromToRangeFilter()

    class Meta:
        model = Message
        fields = ['sender', 'recipient', 'timestamp']
