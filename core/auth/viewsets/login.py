from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from core.auth.serializers.login import LoginSerializer
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError


class LoginViewSet(ModelViewSet):
    serializer_class = LoginSerializer
    http_method_names = ["post"]
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return Response(serializer.validated_data, status=status.HTTP_200_OK)
