from rest_framework.response import Response
from rest_framework import status
from django.http import Http404

from core.abstract.viewsets import AbstractViewSet

# from core.auth.permissions import UserPermission
from rest_framework.permissions import IsAuthenticated

from core.comment.models import Comment
from core.comment.serializers import CommentSerializer


class CommentViewSet(AbstractViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = CommentSerializer
    http_method_names = ["get", "post", "put", "delete"]

    def get_queryset(self):
        # return Comment.objects.filter(author=self.request.user)
        user = self.request.user
        # print(user)
        if user.is_superuser:
            return Comment.objects.all()
        post_pk = self.kwargs["post_pk"]
        # print(post_pk) => 5f106ca2f63a407982d3ececd6914abe
        if post_pk is None:
            return Http404
        return Comment.objects.filter(post__public_id=post_pk)

    def get_object(self):
        obj = Comment.objects.get_object_by_public_id(self.kwargs.get("pk"))
        self.check_object_permissions(self.request, obj)
        return obj

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        instance = Comment.objects.get_object_by_public_id(self.kwargs["pk"])
        if not instance.edited:
            instance.edited = True
        serializer = self.serializer_class(
            instance, data=request.data, partial=True, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
