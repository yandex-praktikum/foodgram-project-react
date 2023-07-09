from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.IsAuthenticatedOrReadOnly):
    """Доступ на изменение только автору"""
    message = 'У вас недостаточно прав для выполнения данного действия.'

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
        )


class IsAuthenticatedOrPostOnly(permissions.BasePermission):
    message = 'Учетные данные не были предоставлены.'

    def has_permission(self, request, view):
        return (
            request.method == 'POST'
            or request.user.is_authenticated
        )
