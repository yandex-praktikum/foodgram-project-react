from rest_framework import serializers
from users.models import User, Subscribe


class TokenSerializer(serializers.Serializer):
    """Сериализатор для получения токена."""
    class Meta:
        fields = (
            'email',
            'password',
            )
        model = User


class UserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            )
        model = User

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Subscribe.objects.filter(user=user, author=obj).exists()
