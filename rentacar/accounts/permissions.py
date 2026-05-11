from rest_framework.permissions import BasePermission

class IsOwner(BasePermission):
    message = "Access restricted to cars owners only."

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_owner
 
    
class IsCustomer(BasePermission):
    message = "Access restricted to customers only."

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_customer

  
class IsPlatformAdmin(BasePermission):
    message = "Access restricted to platform admins only."

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_platform_admin


class IsOwnerOrAdmin(BasePermission):
    message = "Access restricted to cars owners and admins only."

    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.is_owner or request.user.is_platform_admin)