from datetime import datetime, timedelta

from django.db import models

from api.models import Client, Offer, Classroom, MultipleBooking

PAYMENTCHOICES = (
    ('Cash', 'Cash'),
    ('Online', 'Online'),
    ('Check', 'Check'),
)


class Booking(models.Model):
    client = models.ForeignKey(Client, related_name='bookings', on_delete=models.CASCADE)
    offer = models.ForeignKey(Offer, related_name='bookings', on_delete=models.CASCADE)
    classroom = models.ForeignKey(Classroom, related_name='bookings', on_delete=models.CASCADE)
    multipleBooking = models.ForeignKey(MultipleBooking, related_name='bookings', on_delete=models.SET_NULL, blank=True, null=True)
    priceToPay = models.DecimalField(max_digits=10, decimal_places=2)
    isBookingReserve = models.BooleanField(default=True)
    typePayment = models.CharField(choices=PAYMENTCHOICES, default='Check')
    scheduleOfferDate = models.DateTimeField()
    registeredDate = models.DateTimeField()
    expirationDate = models.DateTimeField()
    ordenGeneratedDate = models.DateTimeField()
    paidDate = models.DateTimeField(blank=True, null=True)
    isHistory = models.BooleanField(default=False)
    isPaid = models.BooleanField(default=False)
    transactionCode = models.CharField(max_length=100)
    versatCode = models.CharField(max_length=100) 




