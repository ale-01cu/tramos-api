from django.db import models


class Dutiesrigths(models.Model):
    description = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    is_duty = models.BooleanField(default=True)
