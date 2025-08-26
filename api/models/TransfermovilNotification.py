import uuid
from django.db import models

class TransfermovilNotification(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    source = models.IntegerField()
    bank_id = models.CharField(max_length=255)
    tm_id = models.CharField(max_length=255)
    phone = models.CharField(max_length=50)
    msg = models.TextField()
    external_id = models.CharField(max_length=255, null=True, blank=True)
    status = models.IntegerField()
    bank = models.IntegerField(null=True, blank=True)
    paid = models.DecimalField(max_digits=10, decimal_places=2)
    is_pending = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Notificación de Transfermóvil"
        verbose_name_plural = "Notificaciones de Transfermóvil"

    def __str__(self):
        return f"Notificación de Transfermóvil {self.id} para {self.phone}"