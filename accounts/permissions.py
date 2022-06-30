from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """Permission class to check user ownership
    """

    message = "You don't have access to this profile."
    """Custom message shown when the request is denied
    """

    def has_object_permission(self, request, view, obj):
        return obj.id == request.user.id
