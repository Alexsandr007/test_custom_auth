from django.urls import path
from .views import (
    RoleListView, 
    RoleDetailView,
    AccessRuleListView, 
    AccessRuleDetailView,
    UserRoleView,
    UserRoleDetailView
)

app_name = 'authentication'

urlpatterns = [
    path('roles/', RoleListView.as_view(), name='role-list'),
    path('roles/<int:pk>/', RoleDetailView.as_view(), name='role-detail'),
    
    path('rules/', AccessRuleListView.as_view(), name='access-rule-list'),
    path('rules/<int:pk>/', AccessRuleDetailView.as_view(), name='access-rule-detail'),
    
    path('user-roles/', UserRoleView.as_view(), name='user-role-list'),
    path('user-roles/<int:pk>/', UserRoleDetailView.as_view(), name='user-role-detail'),
]