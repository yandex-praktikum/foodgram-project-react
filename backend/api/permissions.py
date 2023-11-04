from rest_framework.permissions import (BasePermission,
                                        SAFE_METHODS,
                                        IsAdminUser,
                                        IsAuthenticatedOrReadOnly,
                                        IsAuthenticated
                                        )


class AuthorStaffOrReadOnly(BasePermission):
    """Если не админ или не автор, то только чтение"""
    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or request.user == obj.author
            or request.user == request.user_is_staff
        )


class AdminOrReadOnly(IsAdminUser):
    """Если не админ, то только чтение"""
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_staff)

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or request.user.is_staff
        )


class IsAuthenticatedOrReadOnlyFoodgram(IsAuthenticatedOrReadOnly):
    """Если не пользователь, то только чтение"""
