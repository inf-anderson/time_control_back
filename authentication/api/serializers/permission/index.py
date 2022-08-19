# Rest Framework
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
# Models
from authentication.models import Permission
# Utils
from datetime import datetime as dt


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = "__all__"
    
    def create(self, validated_data):
        return Permission.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.description = validated_data.get('description', instance.description)
        instance.state = validated_data.get('state', instance.state)
        instance.updated_at = dt.utcnow()
        instance.save()
        return instance
