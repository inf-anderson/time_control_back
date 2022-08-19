# Rest Framework
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
# Models
from authentication.models import RolePermission
# Serializer
from authentication.api.serializers.index import PermissionSerializer


class RolePermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RolePermission
        fields = "__all__"
    
    def create(self, validated_data):
        return RolePermission.objects.create(**validated_data)
    

class RolePermissionReadOnlySerializer(serializers.ModelSerializer):
    permission = PermissionSerializer(read_only=True)

    class Meta:
        model = RolePermission
        fields = "__all__"
