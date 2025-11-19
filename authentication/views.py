from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Role, BusinessElement, AccessRule, UserRole
from .serializers import RoleSerializer, BusinessElementSerializer, AccessRuleSerializer, UserRoleSerializer
from .decorators import check_permission

class RoleListView(APIView):
    @check_permission('access_management', 'read')
    def get(self, request):
        roles = Role.objects.all()
        serializer = RoleSerializer(roles, many=True)
        return Response(serializer.data)
    
    @check_permission('access_management', 'create')
    def post(self, request):
        serializer = RoleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RoleDetailView(APIView):
    @check_permission('access_management', 'read')
    def get(self, request, pk):
        try:
            role = Role.objects.get(pk=pk)
            serializer = RoleSerializer(role)
            return Response(serializer.data)
        except Role.DoesNotExist:
            return Response({'error': 'Роль не найдена'}, status=status.HTTP_404_NOT_FOUND)
    
    @check_permission('access_management', 'update')
    def put(self, request, pk):
        try:
            role = Role.objects.get(pk=pk)
            serializer = RoleSerializer(role, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Role.DoesNotExist:
            return Response({'error': 'Роль не найдена'}, status=status.HTTP_404_NOT_FOUND)
    
    @check_permission('access_management', 'delete')
    def delete(self, request, pk):
        try:
            role = Role.objects.get(pk=pk)
            role.delete()
            return Response({'message': 'Роль удалена'}, status=status.HTTP_204_NO_CONTENT)
        except Role.DoesNotExist:
            return Response({'error': 'Роль не найдена'}, status=status.HTTP_404_NOT_FOUND)

class AccessRuleListView(APIView):
    @check_permission('access_management', 'read')
    def get(self, request):
        rules = AccessRule.objects.select_related('role', 'element').all()
        serializer = AccessRuleSerializer(rules, many=True)
        return Response(serializer.data)
    
    @check_permission('access_management', 'create')
    def post(self, request):
        serializer = AccessRuleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AccessRuleDetailView(APIView):
    @check_permission('access_management', 'read')
    def get(self, request, pk):
        try:
            rule = AccessRule.objects.get(pk=pk)
            serializer = AccessRuleSerializer(rule)
            return Response(serializer.data)
        except AccessRule.DoesNotExist:
            return Response({'error': 'Правило доступа не найдено'}, status=status.HTTP_404_NOT_FOUND)
    
    @check_permission('access_management', 'update')
    def put(self, request, pk):
        try:
            rule = AccessRule.objects.get(pk=pk)
            serializer = AccessRuleSerializer(rule, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except AccessRule.DoesNotExist:
            return Response({'error': 'Правило доступа не найдено'}, status=status.HTTP_404_NOT_FOUND)
    
    @check_permission('access_management', 'delete')
    def delete(self, request, pk):
        try:
            rule = AccessRule.objects.get(pk=pk)
            rule.delete()
            return Response({'message': 'Правило доступа удалено'}, status=status.HTTP_204_NO_CONTENT)
        except AccessRule.DoesNotExist:
            return Response({'error': 'Правило доступа не найдено'}, status=status.HTTP_404_NOT_FOUND)

class UserRoleView(APIView):
    @check_permission('access_management', 'read')
    def get(self, request):
        user_roles = UserRole.objects.select_related('user', 'role').all()
        serializer = UserRoleSerializer(user_roles, many=True)
        return Response(serializer.data)
    
    @check_permission('access_management', 'create')
    def post(self, request):
        serializer = UserRoleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserRoleDetailView(APIView):
    @check_permission('access_management', 'read')
    def get(self, request, pk):
        try:
            user_role = UserRole.objects.get(pk=pk)
            serializer = UserRoleSerializer(user_role)
            return Response(serializer.data)
        except UserRole.DoesNotExist:
            return Response({'error': 'Связь пользователь-роль не найдена'}, status=status.HTTP_404_NOT_FOUND)
    
    @check_permission('access_management', 'delete')
    def delete(self, request, pk):
        try:
            user_role = UserRole.objects.get(pk=pk)
            user_role.delete()
            return Response({'message': 'Связь пользователь-роль удалена'}, status=status.HTTP_204_NO_CONTENT)
        except UserRole.DoesNotExist:
            return Response({'error': 'Связь пользователь-роль не найдена'}, status=status.HTTP_404_NOT_FOUND)