# Django
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
# REST Framework imports
from rest_framework.decorators import APIView
# Models
from authentication.models import User, UserRole, RolePermission
# Serializers
from authentication.api.serializers.index import UserSerializer, UpdatePasswordSerializer, \
    UserRoleReadOnlySerializer, RolePermissionReadOnlySerializer
# SimpleJWT
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
import jwt
# Utils
from core.utils.index import response, send_email
from core.settings import SECRET_KEY


class RegisterAV(APIView):

    def post(self, request):
        try:
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return response(serializer.data, status=201)
            return response(serializer.errors, status=400)
        except Exception as e:
            return response(str(e), status=400)


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        roles = []
        permissions = []
        token = super().get_token(user)
        is_superuser = user.is_superuser

        # Get user roles
        dataRole       = UserRole.objects.filter(user=user)
        roleSerializer = UserRoleReadOnlySerializer(dataRole, many=True)
        for role in roleSerializer.data:
            id = role['role']['id']
            dataPermission = RolePermission.objects.filter(role_id=id)
            permissionSerializer = RolePermissionReadOnlySerializer(dataPermission, many=True)
            for permission in permissionSerializer.data:
                permissions.append(permission['permission']['description'])

        # Add custom claims
        token['name'] = f'{user.first_name} {user.last_name}'
        token['roles'] = roles
        token['permissions'] = jwt.encode({'permissions': permissions}, SECRET_KEY, algorithm="HS256")
        token['is_superuser'] = is_superuser

        return token


class LoginAV(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class ForgotPasswordAV(APIView):
    def post(self, request):
        try:
            user = User.objects.get(email=request.data['email'])
            uidb64 = urlsafe_base64_encode(force_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            current_site = get_current_site(request)
            relative_link = reverse('password-reset-confirm', kwargs={'uidb64': uidb64, 'token': token})
            url = 'http://' + str(current_site) + str(relative_link)
            send_email('recuperar contraseña','en este link podras restablecer tu contraseña: ' + url, 
                        request.data['email'],)
            return response({'message': 'Email sent'}, status=200)
        except Exception as e:
            return response({'error': str(e)}, status=500)


class CheckPasswordTokenAV(APIView):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=uid)
            if PasswordResetTokenGenerator().check_token(user, token):
                return response({'success': True, 'uidb64': uidb64, 'token': token}, status=200)
            return response({'error': 'Token is invalid'}, status=400)
        except Exception as e:
            return response({'error': str(e)}, status=500)


class ResetPasswordAV(APIView):

    def patch(self, request):
        try:
            serializer = UpdatePasswordSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            return response({'message': 'Password Reset Success'}, status=200)
        except Exception as e:
            return response({'error': str(e)}, status=500)
