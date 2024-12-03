from rest_framework import serializers

from core.abstract.serializers import AbstractSerializer
from core.comment.models import Comment
from core.user.models import User
from core.post.models import Post
from core.user.serializers import UserSerializer
from core.post.serializers import PostSerializer


class CommentSerializer(AbstractSerializer):
    post = serializers.SlugRelatedField(
        slug_field="public_id",
        queryset=Post.objects.all(),
    )
    author = serializers.SlugRelatedField(
        slug_field="public_id",
        queryset=User.objects.all(),
    )
    """
    The purpose of this function is to ensure that during an update operation,
    the post field retains its original value, while during a create operation,
    it accepts the new value provided.
    """

    def validate_post(self, value):
        if self.instance:
            return self.instance.post
        return value

    # instead post and author show their details
    def to_representation(self, instance):
        response = super().to_representation(instance)
        # {'id': '1ae03cb112734f62bc00840c9051e4af',
        #  'author': UUID('f70510f1-f2d4-4fde-ae6f-476d711e2f57'),
        #  'post': UUID('5f106ca2-f63a-4079-82d3-ececd6914abe'),
        #  'body': 'New Comment', 'edited': False, 'created': '2024-09-19 20:59:06',
        #  'updated': '2024-09-19 20:59:06'}

        # response["post"] = PostSerializer(instance.post).data
        # response["author"] = UserSerializer(instance.author).data
        author = User.objects.get_object_by_public_id(response["author"])
        response["author"] = UserSerializer(author).data

        return response

    class Meta:
        model = Comment
        fields = ["id", "author", "post", "body", "edited", "created", "updated"]
        read_only_fields = ["created", "updated"]
