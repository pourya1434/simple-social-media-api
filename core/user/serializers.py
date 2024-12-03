from rest_framework import serializers

from core.user.models import User
from core.abstract.serializers import AbstractSerializer


class UserSerializer(AbstractSerializer):
    id = serializers.UUIDField(read_only=True, source="public_id", format="hex")
    created = serializers.DateTimeField(read_only=True, format="%Y-%m-%d %H:%M:%S")
    updated = serializers.DateTimeField(read_only=True, format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "is_admin",
            "is_active",
            "created",
            "updated",
        ]
        read_only_fields = ["is_admin", "is_active"]
