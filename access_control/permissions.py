from rest_framework.permissions import BasePermission
from accounts.models import User
from access_control.models import BusinessElement, AccessRoleRule


class HasAccessPermission(BasePermission):
    """
    element_code задается во вьюхе (например, 'products', 'users').
    """
    def has_permission(self, request, view):
        if not request.user or not isinstance(request.user, User):
            return False

        role = getattr(request.user, 'role', None)
        element_code = getattr(view, 'element_code', None)
        if not element_code or not role:
            return False

        try:
            element = BusinessElement.objects.get(code=element_code)
            rule = AccessRoleRule.objects.get(role=role, element=element)
        except (BusinessElement.DoesNotExist, AccessRoleRule.DoesNotExist):
            return False

        method = request.method.upper()

        if method == 'GET':
            return rule.read_permission or rule.read_all_permission

        if method == 'POST':
            return rule.create_permission

        if method in ('PUT', 'PATCH'):
            return rule.update_permission or rule.update_all_permission

        if method == 'DELETE':
            return rule.delete_permission or rule.delete_all_permission

        return False
    def has_object_permission(self, request, view, obj):
        """
        Предполагается, что у объекта есть поле owner.
        """
        if not request.user or not isinstance(request.user, User):
            return False

        role = getattr(request.user, 'role', None)
        element_code = getattr(view, 'element_code', None)
        if not element_code or not role:
            return False

        try:
            element = BusinessElement.objects.get(code=element_code)
            rule = AccessRoleRule.objects.get(role=role, element=element)
        except (BusinessElement.DoesNotExist, AccessRoleRule.DoesNotExist):
            return False

        method = request.method.upper()

        if method in ('GET',):
            if rule.read_all_permission:
                return True
            if rule.read_permission and getattr(obj, 'owner_id', None) == request.user.id:
                return True

        if method in ('PUT', 'PATCH'):
            if rule.update_all_permission:
                return True
            if rule.update_permission and getattr(obj, 'owner_id', None) == request.user.id:
                return True

        if method == 'DELETE':
            if rule.delete_all_permission:
                return True
            if rule.delete_permission and getattr(obj, 'owner_id', None) == request.user.id:
                return True

        return False

class IsAdminRole(BasePermission):
    def has_permission(self, request, view):
        user = getattr(request, 'user', None)
        if not user:
            return False
        role = getattr(user, 'role', None)
        if not role:
            return False
        return role.name == 'admin'


