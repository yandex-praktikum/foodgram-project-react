from rest_framework import serializers
from users.models import User, Subscribe
# from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404


class TokenSerializer(serializers.Serializer):
    """Сериализатор для получения токена."""
    password = serializers.CharField(
        required=True,
        max_length=150,
    )
    email = serializers.EmailField(
        required=True,
        max_length=254
    )

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            user = get_object_or_404(User, email=email, password=password)
            if user.check_password(password):
                return user
            else:
                raise serializers.ValidationError('Неверный логин или пароль')
        else:
            raise serializers.ValidationError(
                'Вы должны ввести логин и пароль'
                )


class UserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()
    password = serializers.CharField(write_only=True)

    class Meta:
        fields = (
            'email',
            'username',
            'first_name',
            'last_name',
            "password",
            'is_subscribed',
            )
        model = User

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Subscribe.objects.filter(user=user, author=obj).exists()

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
