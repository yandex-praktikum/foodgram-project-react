from django.shortcuts import get_object_or_404
from users.models import CustomUser, Subscription


def get_user_object(username: str) -> CustomUser:
    """Возврашает модель пользователя по username."""

    return get_object_or_404(CustomUser, username=username)


def get_all_users() -> CustomUser:
    """Возвращает список всех пользователей."""

    return CustomUser.objects.all()


def get_user_subscriptions(user: CustomUser) -> CustomUser:
    """Возвращает подписки пользователя."""

    return CustomUser.objects.filter(author__user=user)


def get_author(author_id: int) -> CustomUser:
    """Возврашает автора по id."""

    return get_object_or_404(CustomUser, id=author_id)


def create_subscription(user: CustomUser, author: CustomUser) -> None:
    """Подписка на автора."""

    Subscription.objects.create(user=user, author=author)


def delete_subscription(user: CustomUser, author: CustomUser) -> None:
    """Отписка от автора."""

    subscription = get_object_or_404(Subscription,
                                     user=user,
                                     author=author
                                     )
    subscription.delete()
