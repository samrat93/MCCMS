from rest_framework import permissions


class UpdateOwnProfile(permissions.BasePermission):
    """ This will allow only for user to update their profile """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.id == request.user.id