from django.db import models
import uuid


class Permission(models.Model):
    id          = models.CharField(default=str(uuid.uuid4()), max_length=255, unique=True, primary_key=True, editable=False)
    description = models.TextField(blank=True)
    state       = models.BooleanField(default=True)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(null=True, default=None)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'permissions'
        verbose_name = 'permission'
        verbose_name_plural = 'permissions'
