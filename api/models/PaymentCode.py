from django.db import models


class PaymentCode(models.Model):
    code = models.CharField(max_length=6)

    class Meta:
        verbose_name = 'Código de Pago'
        verbose_name_plural = 'Códigos de Pagos'
        ordering = ['-id']

    def __str__(self):
        return self.code