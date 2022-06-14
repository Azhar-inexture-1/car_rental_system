from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """Permission class to check user ownership"""

    def has_object_permission(self, request, view, obj):
        return obj.id == request.user.id
