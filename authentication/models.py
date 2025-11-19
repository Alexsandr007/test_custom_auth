from django.db import models

class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    
    class Meta:
        db_table = 'roles'

class BusinessElement(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    code = models.CharField(max_length=50, unique=True)
    
    class Meta:
        db_table = 'business_elements'

class AccessRule(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='access_rules')
    element = models.ForeignKey(BusinessElement, on_delete=models.CASCADE, related_name='access_rules')
    read_permission = models.BooleanField(default=False)
    read_all_permission = models.BooleanField(default=False)
    create_permission = models.BooleanField(default=False)
    update_permission = models.BooleanField(default=False)
    update_all_permission = models.BooleanField(default=False)
    delete_permission = models.BooleanField(default=False)
    delete_all_permission = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'access_rules'
        unique_together = ['role', 'element']

class UserRole(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='user_roles')
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='user_roles')
    
    class Meta:
        db_table = 'user_roles'
        unique_together = ['user', 'role']