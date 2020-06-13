from rest_framework import permissions


# Permissions for Project View
class IsProjectCreatorOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if (request.method in permissions.SAFE_METHODS) or (request.method == 'POST'):
            return True
        return (obj.creator == request.user) or request.user.isAdmin


class IsTeamMemberOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if (request.method == 'POST') or (request.method in permissions.SAFE_METHODS):
            return True
        if request.user.isAdmin or (request.user in obj.project.team.all()):
            return True
        return False


class IsCommenter(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if (request.method in permissions.SAFE_METHODS) or (request.method == 'POST'):
            return True
        return request.user == obj.commenter


class IsAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if (request.method in permissions.SAFE_METHODS) or request.user.isAdmin:
            return True
        return False
