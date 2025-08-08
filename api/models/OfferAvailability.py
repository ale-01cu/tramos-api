from django.db import models
from api.models import Offer
from django.utils.translation import gettext_lazy as _


class OfferAvailability(models.Model):
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE)
    time = models.TimeField()
    # time = models.CharField(max_length=24)
    availability = models.IntegerField(default=0)
    group_code = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Disponibilidad')
        verbose_name_plural = _('Disponibilidades')
