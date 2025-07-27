# import uuid
# from django.db import models
#
# class BankNotification(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     source = models.IntegerField()
#     bank_id = models.CharField(max_length=255)
#     tm_id = models.CharField(max_length=255)
#     phone = models.CharField(max_length=50)
#     msg = models.TextField()
#     external_id = models.CharField(max_length=255, null=True, blank=True)
#     status = models.IntegerField()
#     bank = models.IntegerField(null=True, blank=True)
#     paid = models.DecimalField(max_digits=10, decimal_places=2)
#     created_at = models.DateTimeField(auto_now_add=True)
#     created_at_bank = models.DateTimeField()
#     full_name = models.CharField(max_length=255)
#     classroom_name = models.CharField(max_length=255)
#     client_ci = models.CharField(max_length=20)
#     date_start = models.DateTimeField()
#     schedule_time = models.CharField(max_length=50)
#
#     class Meta:
#         verbose_name = "Notificación de Banco"
#         verbose_name_plural = "Notificaciones de Banco"
#
#     def __str__(self):
#         return f"Notificación de Banco {self.id} para {self.phone}"