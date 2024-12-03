from rest_framework.permissions import AllowAny

from core.user.serializers import UserSerializer
from core.user.models import User
from core.abstract.viewsets import AbstractViewSet


class UserViewSets(AbstractViewSet):
    serializer_class = UserSerializer
    http_method_names = ["get", "patch"]
    permission_classes = [AllowAny]

    def get_queryset(self):
        # is_superuser is a flag that is set to True for superusers and False for other users.
        # altho we add is_admin field to our user model, we can use is_superuser field to check if user is admin or not.
        if self.request.user.is_superuser:
            return User.objects.all()
        return User.objects.exclude(is_admin=True)

    def get_object(self):
        obj = User.objects.get_object_by_public_id(public_id=self.kwargs["pk"])
        self.check_object_permissions(self.request, obj)
        return obj
