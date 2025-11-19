from functools import wraps
from django.http import JsonResponse
from users.models import User
from django.contrib.auth.models import AnonymousUser

def jwt_authentication_required(view_method):
    @wraps(view_method)
    def wrapped_view(self, request, *args, **kwargs):
        request.user = AnonymousUser()
        
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        
        if not auth_header and hasattr(request, 'headers'):
            auth_header = request.headers.get('Authorization', '')
        
        if not auth_header:
            return JsonResponse({'error': 'Токен не предоставлен'}, status=401)
        
        if not auth_header.startswith('Bearer '):
            return JsonResponse({'error': 'Токен не предоставлен'}, status=401)
        
        token = auth_header.split(' ')[1].strip()
        
        if not token:
            return JsonResponse({'error': 'Токен не может быть пустым'}, status=401)
        
        user = User.verify_jwt_token(token)
        
        if not user:
            return JsonResponse({'error': 'Неверный или просроченный токен'}, status=401)
        
        request.user = user
        return view_method(self, request, *args, **kwargs)
    
    return wrapped_view


def check_permission(element_code, permission_type):
    def decorator(view_method):
        @wraps(view_method)
        @jwt_authentication_required 
        def wrapped_view(self, request, *args, **kwargs):
            from .models import BusinessElement, AccessRule
            
            
            if request.user.is_superuser:
                return view_method(self, request, *args, **kwargs)
            
            try:
                element = BusinessElement.objects.get(code=element_code)
            except BusinessElement.DoesNotExist:
                return JsonResponse({'error': 'Бизнес-элемент не найден'}, status=403)
            
            user_roles = request.user.user_roles.select_related('role').all()
            
            for user_role in user_roles:
                try:
                    access_rule = AccessRule.objects.get(
                        role=user_role.role, 
                        element=element
                    )
                    
                    
                    if getattr(access_rule, f'{permission_type}_permission', False):
                        return view_method(self, request, *args, **kwargs)
                        
                    if getattr(access_rule, f'{permission_type}_all_permission', False):
                        return view_method(self, request, *args, **kwargs)
                        
                except AccessRule.DoesNotExist:
                    continue
            
            return JsonResponse({'error': 'Доступ запрещен'}, status=403)
        return wrapped_view
    return decorator