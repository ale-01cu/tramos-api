from django.db import models

from api.models import Company, Course, Classroom


class Offer(models.Model):
    course = models.ForeignKey(Course, related_name='offers', on_delete=models.SET_NULL, null=True)
    classroom = models.ForeignKey(Classroom, related_name='offers', on_delete=models.SET_NULL, null=True)
    description = models.CharField(max_length=200)
    date_start_course = models.DateTimeField()
    date_end_course = models.DateTimeField()
    date_start_offer = models.DateTimeField()
    date_end_offer = models.DateTimeField()
    priceToPay = models.DecimalField(max_digits=10, decimal_places=2)
    company = models.ForeignKey(Company, related_name='offers', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = 'Oferta'
        verbose_name_plural = 'Ofertas'
        ordering = ['id']

