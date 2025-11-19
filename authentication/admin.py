from django.contrib import admin
from django.contrib import messages
from .models import Role, BusinessElement, AccessRule, UserRole

class AccessRuleInline(admin.TabularInline):
    model = AccessRule
    extra = 1
    fields = ('element', 'read_permission', 'read_all_permission', 'create_permission', 
              'update_permission', 'update_all_permission', 'delete_permission', 'delete_all_permission')

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'users_count')
    search_fields = ('name', 'description')
    inlines = [AccessRuleInline]
    
    def users_count(self, obj):
        return obj.user_roles.count()
    users_count.short_description = 'Количество пользователей'

@admin.register(BusinessElement)
class BusinessElementAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'description')
    search_fields = ('name', 'code', 'description')
    list_filter = ('code',)

@admin.register(AccessRule)
class AccessRuleAdmin(admin.ModelAdmin):
    list_display = ('role', 'element', 'read_permission', 'create_permission', 'update_permission', 'delete_permission')
    list_filter = ('role', 'element')
    search_fields = ('role__name', 'element__name')
    
    fieldsets = (
        (None, {
            'fields': ('role', 'element')
        }),
        ('Права доступа', {
            'fields': (
                ('read_permission', 'read_all_permission'),
                ('create_permission',),
                ('update_permission', 'update_all_permission'),
                ('delete_permission', 'delete_all_permission'),
            )
        }),
    )

@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'user_email', 'user_name')
    list_filter = ('role',)
    search_fields = ('user__email', 'user__first_name', 'user__last_name', 'role__name')
    autocomplete_fields = ['user']
    
    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = 'Email'
    
    def user_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"
    user_name.short_description = 'Имя пользователя'