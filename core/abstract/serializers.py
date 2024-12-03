from rest_framework import serializers


class AbstractSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True, source="public_id", format="hex")
    created = serializers.DateTimeField(read_only=True, format="%Y-%m-%d %H:%M:%S")
    updated = serializers.DateTimeField(read_only=True, format="%Y-%m-%d %H:%M:%S")
