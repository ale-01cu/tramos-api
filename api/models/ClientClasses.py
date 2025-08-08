from django.db import models

from api.models import Offer, Client


class ClientClasses(models.Model):
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    scheduleOfferDate = models.CharField()
    evaluation = models.IntegerField(null=True)
    is_graduated = models.BooleanField(default=False)
    graduatedDate = models.DateTimeField()
    bookingCode = models.CharField(null=True)
    tome = models.CharField(null=True)
    folio = models.CharField(null=True)
    assistenceClient = models.JSONField(blank=True)
    evaluationConfirmed = models.BooleanField(default=False)
    number = models.IntegerField(null=True, blank=True)
    registryNumber = models.IntegerField(null=True, blank=True)
    documentRegistry = models.CharField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

