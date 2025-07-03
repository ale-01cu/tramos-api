from datetime import datetime

from django.db import models

from api.models import Company


class MultipleBooking(models.Model):
    company = models.ForeignKey(Company, related_name='multiplebookings', on_delete=models.CASCADE)
    created_at = models.DateTimeField()
    is_confirmed = models.BooleanField(default=False)
    is_history = models.BooleanField(default=False)

