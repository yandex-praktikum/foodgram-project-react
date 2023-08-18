from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrReadOnly(BasePermission):
    """Доступ только для администрации или
    только на чтение любому пользователю.
    """

    def has_permission(self, request, view):

        return (
                request.user.is_authenticated and request.user.is_admin
                or request.method in SAFE_METHODS
        )


class IsAdminOrAuthorOrReadOnly(BasePermission):
    """Доступ только для администрации, автору или
    только на чтение любому пользователю.
    """

    def has_object_permission(self, request, view, obj):

        return (
                request.method in SAFE_METHODS
                or obj.author == request.user
                or request.user.is_admin
        )


class IsAuthorOrReadOnly(BasePermission):
    """Разрешение только для автора или только на чтение."""

    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or obj.author == request.user
        )


class IsAuthorizedAndAuthor(BasePermission):
    """Доступ только для авторизированного автора."""

    def has_object_permission(self, request, view, obj):

        return request.user.is_authenticated and obj.author == request.user
