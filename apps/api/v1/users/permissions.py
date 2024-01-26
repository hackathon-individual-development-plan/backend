from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsOwnerOrReadOnly(BasePermission):
    """Выдает права создавать и редактировать ИПР."""

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return obj.owner == request.user


class ReadOnly(BasePermission):
    """Выдает права только на чтение ИПР."""

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS
