from django.db import models

from api.models import Municipality
from api.models.PaymentCode import PaymentCode

class School(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=250, blank=True)
    providerNumber = models.IntegerField()
    paymentCode = models.ForeignKey(PaymentCode, related_name='schools', on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=250)
    municipality = models.ForeignKey(Municipality, related_name='schools', on_delete=models.CASCADE)
    date = models.DateTimeField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Escuela'
        verbose_name_plural = 'Escuelas'
        ordering = ['id']

