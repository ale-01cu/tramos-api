from django.db import models
from django.utils.translation import gettext_lazy as _


class Province(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Provincia')
        verbose_name_plural = _('Provincias')
