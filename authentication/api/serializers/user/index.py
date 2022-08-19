# Django
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
# Rest Framework
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
# Model
from authentication.models import User, UserRole


class UserSerializer(serializers.ModelSerializer):
    role = serializers.CharField(style={'input_type': 'text'}, write_only=True)
    password2 = serializers.CharField(style={'input_type': 'text'}, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name',
                  'email', 'password', 'password2', 'company', 'role']
        extra_kwargs = {
            'username'  : {'required': True},
            'email'     : {'required': True},
            'first_name': {'required': True},
            'last_name' : {'required': True},
            'role'      : {'required': True},
            'password'  : {'required': True},
            'password2' : {'required': True},
        }

    def save(self):
        password  = self.validated_data['password']
        password2 = self.validated_data['password2']
        if password != password2:
            raise AuthenticationFailed('Passwords must match')

        if User.objects.filter(email=self.validated_data['email']).exists():
            raise AuthenticationFailed('Email already exists')

        account = User(email=self.validated_data['email'],
                       first_name=self.validated_data['first_name'],
                       last_name=self.validated_data['last_name'],
                       username=self.validated_data['username'])
        account.set_password(password)
        account.save()
        user = User.objects.get(id=account.id)
        try:
            role = UserRole.objects.create(user_id=user.id, role_id=self.validated_data['role'])
            role.save()
        except Exception as e:
            user.delete()
            raise AuthenticationFailed('invalid role')


class UserReadOnlySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email']
        read_only_fields = ['id', 'first_name', 'last_name', 'email']


class UpdatePasswordSerializer(serializers.Serializer):
    token         = serializers.CharField(write_only=True, required=True)
    uidb64        = serializers.CharField(write_only=True, required=True)
    new_password  = serializers.CharField(write_only=True, required=True)
    new_password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        fields = ['token', 'uidb64', 'new_password', 'new_password2']

    def validate(self, data):
        try:
            if data['new_password'] != data['new_password2']:
                raise serializers.ValidationError('Passwords must match')

            id = force_str(urlsafe_base64_decode(data['uidb64']))
            user = User.objects.get(pk=id)

            if not PasswordResetTokenGenerator().check_token(user, data['token']):
                raise AuthenticationFailed('The reset password link is invalid.')

            user.set_password(data['new_password'])
            user.save()
            return data
        except Exception as e:
            raise AuthenticationFailed(str(e))
