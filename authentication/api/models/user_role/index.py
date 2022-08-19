from django.db import models
from authentication.models import User, Role
import uuid


class UserRole(models.Model):
    id         = models.CharField(default=str(uuid.uuid4()), max_length=255, unique=True, primary_key=True, editable=False)
    user       = models.ForeignKey(User, on_delete=models.CASCADE)
    role       = models.ForeignKey(Role, on_delete=models.CASCADE)
    state      = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, default=None)

    class Meta:
        db_table = 'user_roles'
        verbose_name = 'user_Role'
        verbose_name_plural = 'user_Roles'

    def __str__(self):
        return self.user.username + ' - ' + self.role.description
