# Rest Framework
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
# Models
from authentication.models import UserRole


class UserRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRole
        fields = "__all__"
