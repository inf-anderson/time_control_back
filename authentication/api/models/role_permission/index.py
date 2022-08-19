from django.db import models
from authentication.models import Role, Permission
import uuid


class RolePermission(models.Model):
    id         = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True,  editable=False)
    role       = models.ForeignKey(Role, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)
    state      = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, default=None)

    class Meta:
        db_table = 'role_permissions'
        verbose_name = 'role_Permission'
        verbose_name_plural = 'role_Permissions'

    def __str__(self):
        return self.user.username + ' - ' + self.role.description
