from .serializers import UserSerializer, TokenSerializer
from users.models import User
from django.contrib.auth.tokens import default_token_generator
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404


class UserViewSet(viewsets.ModelViewSet):
    """Написать."""
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=True)
    def me(self, request):
        user = get_object_or_404(User, email=request.email)
        serializer = self.get_serializer(user)
        return Response(serializer.data)


@api_view(['POST'])
def token(request):
    """Получение токена авторизации по почте и паролю."""
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = request.data.get('email')
    user = get_object_or_404(
        User,
        email=email,
    )
    token = default_token_generator.make_token(user)
    user.auth_token = token
    user.save()
    return Response(
        {"auth_token": token},
        status=status.HTTP_201_CREATED
        )
