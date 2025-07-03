from django.db import models

from api.models.Service import Service


class Course(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=250)
    paymentCode = models.CharField(max_length=100)
    priceToPay = models.DecimalField(max_digits=10, decimal_places=2)
    rank = models.IntegerField()
    service = models.ForeignKey(Service, related_name='courses', on_delete=models.SET_NULL, null=True)
    bookingCode = models.CharField(max_length=100)
    dependencyCourseId = models.CharField(unique=True, max_length=100, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Curso'
        verbose_name_plural = 'Cursos'

