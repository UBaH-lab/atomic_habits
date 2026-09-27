from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """Только владелец привычки может её редактировать/удалять."""

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
