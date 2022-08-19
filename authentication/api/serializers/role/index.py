# Rest Framework
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
# Models
from authentication.models import Role
# Utils
from datetime import datetime as dt


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = "__all__"
    
    def create(self, validated_data):
        return Role.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.description = validated_data.get('description', instance.description)
        instance.state = validated_data.get('state', instance.state)
        instance.updated_at = dt.utcnow()
        instance.save()
        return instance
    
        
