from rest_framework.permissions import SAFE_METHODS, BasePermission

from apps.users.models import UserRole


class IsChief(BasePermission):
    """Выдает права только руководителю."""

    def has_permission(self, request, view):
        return UserRole.objects.filter(user=request.user, role="chief")


class IsChiefOrReadOnly(BasePermission):
    """Выдает права создавать и редактировать ИПР."""

    def has_permission(self, request, view):
        return UserRole.objects.filter(user=request.user, role="chief") or (
            request.method in SAFE_METHODS and request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            UserRole.objects.filter(user=request.user, role="chief")
            and obj.chief == request.user
        ) or obj.employee == request.user


class ReadOnly(BasePermission):
    """Выдает права на чтение ИПР только своего ИПР"""

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj.employee == request.user
