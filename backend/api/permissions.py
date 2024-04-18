from rest_framework import permissions


class ReadOnlyPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method=='GET'
        )
    def has_object_permission(self, request, view, obj):
        return False