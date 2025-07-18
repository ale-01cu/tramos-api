from django.db import models

from api.models import User


class ActionTraces(models.Model):
    model_name = models.CharField(max_length=100)
    row_id = models.IntegerField()
    action = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    changes = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Traza'
        verbose_name_plural = 'Trazas'
        ordering = ['-created_at']
