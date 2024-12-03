from rest_framework.viewsets import ModelViewSet
from rest_framework import filters


class AbstractViewSet(ModelViewSet):
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["created", "updated"]
    ordering = ["-updated"]
