from rest_framework import permissions


class IsNotAuthenticated(permissions.BasePermission):
    """
    Allows access only to "is_active" users.
    """

    def has_permission(self, request, view) -> bool:
        return not request.user.is_authenticated
