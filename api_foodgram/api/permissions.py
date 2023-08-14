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
                request.user.is_admin
                or obj.author == request.user
                or request.method in SAFE_METHODS
        )
