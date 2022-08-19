# Rest Framework
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
# Models
from authentication.models import UserRole
# Serializer
from authentication.api.serializers.index import RoleSerializer


class UserRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRole
        fields = "__all__"

    def create(self, validated_data):
        return UserRole.objects.create(**validated_data)


class UserRoleReadOnlySerializer(serializers.ModelSerializer):
    role = RoleSerializer(read_only=True)

    class Meta:
        model = UserRole
        fields = ['id', 'user', 'role']
        read_only_fields = ['id', 'user', 'role']
