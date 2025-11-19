from django.contrib import admin
from django.contrib import messages
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_active', 'is_staff', 'date_joined')
    
    list_filter = ('is_active', 'is_staff', 'is_superuser', 'date_joined')
    
    search_fields = ('email', 'first_name', 'last_name')
    
    ordering = ('email',)
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('email', 'password')
        }),
        ('Персональная информация', {
            'fields': ('first_name', 'last_name', 'middle_name')
        }),
        ('Права доступа', {
            'fields': ('is_active', 'is_staff', 'is_superuser')
        }),
        ('Даты', {
            'fields': ('last_login', 'date_joined'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('last_login', 'date_joined')
    
    actions = ['activate_users', 'deactivate_users', 'make_staff']
    
    def activate_users(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} пользователей активировано', messages.SUCCESS)
    activate_users.short_description = "Активировать выбранных пользователей"
    
    def deactivate_users(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} пользователей деактивировано', messages.SUCCESS)
    deactivate_users.short_description = "Деактивировать выбранных пользователей"
    
    def make_staff(self, request, queryset):
        updated = queryset.update(is_staff=True)
        self.message_user(request, f'{updated} пользователей стали staff', messages.SUCCESS)
    make_staff.short_description = "Сделать выбранных пользователей staff"