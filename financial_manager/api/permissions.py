from rest_framework.permissions import BasePermission


class OnlyOwnerOrAdminHasAccess(BasePermission):
    def has_permission(self, request, view):
        print("HAS PERMISSION")
        return bool(request.user and request.user.is_authenticated or request.user.is_superuser)

    def has_object_permission(self, request, view, obj):
        print("HAS OBJECTS PERM")
        return request.user == obj.user or request.user.is_superuser
