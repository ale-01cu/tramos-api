from django.db import models
from django.utils.translation import gettext_lazy as _

from api.models import Province


class Municipality(models.Model):
    name = models.CharField(max_length=100)
    province = models.ForeignKey(Province, on_delete=models.SET_NULL, blank=True, null=True, related_name='municipalities')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Municipio')
        verbose_name_plural = _('Municipios')
