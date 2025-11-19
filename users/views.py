from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from .models import User
from .serializers import UserRegistrationSerializer, UserProfileSerializer, UserLoginSerializer, ChangePasswordSerializer
from authentication.decorators import jwt_authentication_required, check_permission

class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'message': 'Пользователь успешно зарегистрирован',
                'user_id': user.id
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            
            try:
                user = User.objects.get(email=email, is_active=True)
                if user.check_password(password):
                    token = user.generate_jwt_token()
                    from django.utils import timezone
                    user.last_login = timezone.now()
                    user.save()
                    
                    return Response({
                        'token': token,
                        'user': UserProfileSerializer(user).data
                    })
                else:
                    return Response({'error': 'Неверный пароль'}, status=status.HTTP_401_UNAUTHORIZED)
            except User.DoesNotExist:
                return Response({'error': 'Пользователь не найден'}, status=status.HTTP_401_UNAUTHORIZED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(APIView):
    @jwt_authentication_required
    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)
    
    @jwt_authentication_required
    def put(self, request):
        serializer = UserProfileSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ChangePasswordView(APIView):
    @jwt_authentication_required
    def put(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            old_password = serializer.validated_data['old_password']
            new_password = serializer.validated_data['new_password']
            
            if not request.user.check_password(old_password):
                return Response({'error': 'Старый пароль неверный'}, status=status.HTTP_400_BAD_REQUEST)
            
            request.user.set_password(new_password)
            request.user.save()
            
            return Response({'message': 'Пароль успешно изменен'})
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLogoutView(APIView):
    def post(self, request):
        return Response({'message': 'Успешный выход из системы'})

class UserDeleteView(APIView):
    @jwt_authentication_required
    def delete(self, request):
        request.user.soft_delete()
        return Response({'message': 'Аккаунт успешно удален'})