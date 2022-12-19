from rest_framework import permissions , authentication
# admin permission
class AdminAuthenticationPermission(permissions.BasePermission):
    ADMIN_ONLY_AUTH_CLASSES = [authentication.BasicAuthentication, authentication.TokenAuthentication]
    def has_permission(self, request, view):
        user = request.user
        return bool(user.is_authenticated and (user.role) == 'Admin')

class DeliveryManagerPermission(permissions.BasePermission):
    ADMIN_ONLY_AUTH_CLASSES = [authentication.BasicAuthentication, authentication.TokenAuthentication]
    def has_permission(self, request, view):
        user = request.user
        return bool(user.is_authenticated and (user.role) == 'Livreur')