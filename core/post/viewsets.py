# from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action

from core.abstract.viewsets import AbstractViewSet
from core.post.serializers import PostSerializer
from core.auth.permissions import UserPermission
from core.post.models import Post


class PostViewSet(AbstractViewSet):
    serializer_class = PostSerializer
    http_method_names = ("post", "get", "put", "delete")
    permission_classes = [UserPermission]

    def get_queryset(self):
        return Post.objects.all()

    def get_object(self):
        obj = Post.objects.get_object_by_public_id(self.kwargs["pk"])
        self.check_object_permissions(self.request, self)
        return obj

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        # instance = self.get_object()
        instance = Post.objects.get_object_by_public_id(self.kwargs["pk"])
        if not instance.edited:
            instance.edited = True
        serializer = self.serializer_class(
            instance, data=request.data, partial=True, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    @action(methods=["post"], detail=True)
    def like(self, request, *args, **kwargs):
        user = request.user
        post = self.get_object()

        user.like(post)
        serializer = self.serializer_class(post)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=["post"], detail=True)
    def remove_like(self, request, *args, **kwargs):
        user = request.user
        post = self.get_object()

        user.remove_like(post)
        serializer = self.serializer_class(post)
        return Response(serializer.data, status=status.HTTP_200_OK)
