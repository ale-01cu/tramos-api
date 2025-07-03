from django.db import models

from api.models import User


class ActionTraces(models.Model):
    model_name = models.CharField(max_length=100)
    row_id = models.IntegerField()
    registered_at = models.DateTimeField()
    action = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    changes = models.JSONField()

    class Meta:
        verbose_name = 'Traza'
        verbose_name_plural = 'Trazas'
        ordering = ['-registered_at']
