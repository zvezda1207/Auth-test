from django.contrib import admin
from .models import Role, BusinessElement, AccessRoleRule

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']

@admin.register(BusinessElement)
class BusinessElementAdmin(admin.ModelAdmin):
    list_display = ['code', 'description']

@admin.register(AccessRoleRule)
class AccessRoleRuleAdmin(admin.ModelAdmin):
    list_display = ['role', 'element', 'read_permission', 'create_permission']
    list_filter = ['role', 'element']
