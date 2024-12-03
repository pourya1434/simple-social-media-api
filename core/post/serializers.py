from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from core.abstract.serializers import AbstractSerializer
from core.post.models import Post
from core.user.models import User
from core.user.serializers import UserSerializer


class PostSerializer(AbstractSerializer):
    author = serializers.SlugRelatedField(
        queryset=User.objects.all(), slug_field="public_id"
    )
    liked = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()

    def validate_author(self, value):
        # only authenticated users can send request
        print("value:", value)
        print("request", self.context["request"].user)
        if value != self.context["request"].user:
            raise ValidationError("You can't create a post for another user.")
        return value

    def get_liked(self, instance):
        request = self.context["request", None]
        if request is None or request.user.is_anonymous:
            return False
        return request.user.has_liked(instance)

    def get_likes_count(self, instance):
        return instance.liked_by.count()

    # represent author data with post serializer
    def to_representation(self, instance):
        response = super().to_representation(instance)
        author = User.objects.get_object_by_public_id(response["author"])
        response["author"] = UserSerializer(author).data
        return response

    class Meta:
        model = Post
        fields = [
            "id",
            "author",
            "body",
            "edited",
            "liked",
            "likes_count",
            "created",
            "updated",
        ]
        read_only_fields = ["edited"]
