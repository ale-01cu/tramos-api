from django.db import models

from api.models import Client, Offer, MultipleBooking, OfferAvailability
from django.utils import timezone
from datetime import timedelta

PAYMENTCHOICES = (
    ('Cash', 'Cash'),
    ('Transfermovil', 'transfermovil'),
    ('Enzona', 'Enzona'),
    ('cheque', 'Cheque'),
)

# cash
# transfermovil
# enzona
# cheque



class BookingQuerySet(models.QuerySet):
    def active(self):
        """Get all bookings that are either paid or not expired yet."""
        now = timezone.now()
        return self.filter(
            models.Q(isPaid=True) |
            (models.Q(isPaid=False) & models.Q(created_at__gt=now - timedelta(hours=72)))
        )

    def expired_unpaid(self):
        """Get all unpaid bookings that have expired."""
        now = timezone.now()
        return self.filter(
            isPaid=False,
            created_at__lte=now - timedelta(hours=72)
        )

    def cancel_expired(self):
        """Delete all expired unpaid bookings."""
        expired_bookings = self.expired_unpaid()
        count = expired_bookings.count()
        expired_bookings.delete()
        return count


class BookingManager(models.Manager):
    def get_queryset(self):
        return BookingQuerySet(self.model, using=self._db)

    def active(self):
        return self.get_queryset().active()

    def expired_unpaid(self):
        return self.get_queryset().expired_unpaid()

    def cancel_expired(self):
        return self.get_queryset().cancel_expired()


class Booking(models.Model):
    client = models.ForeignKey(Client, related_name='bookings', on_delete=models.CASCADE)
    offer = models.ForeignKey(Offer, related_name='bookings', on_delete=models.CASCADE)
    multipleBooking = models.ForeignKey(MultipleBooking, related_name='bookings', on_delete=models.SET_NULL, blank=True,
                                        null=True)
    typePayment = models.CharField(choices=PAYMENTCHOICES, default='Check')
    # offerAvailability = models.ForeignKey(OfferAvailability, related_name='bookings', on_delete=models.CASCADE)
    paidDate = models.DateTimeField(blank=True, null=True)
    isPaid = models.BooleanField(default=False)
    transactionCode = models.CharField(max_length=100)
    versatCode = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=timezone.now)  # ✅ Usamos este campo

    objects = BookingManager()

    def save(self, *args, **kwargs):
        # ✅ Código mucho más simple, sin lógica de expiración
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Reserva para {self.client} en la oferta {self.offer.id}"

    @property
    def expiration_date(self):
        """Calcula la fecha de expiración dinámicamente"""
        return self.created_at + timedelta(hours=72)

    @property
    def is_expired(self):
        """Check if the booking has expired (72 hours after creation and not paid)."""
        now = timezone.now()
        return not self.isPaid and now > self.expiration_date

    def is_active(self):
        """Check if the booking is active (paid or not expired yet)."""
        return self.isPaid or not self.is_expired

    @classmethod
    def get_active_booking(cls, booking_id):
        """Get a booking by ID and check if it's active."""
        try:
            booking = cls.objects.get(id=booking_id)
            if booking.is_active():
                return booking
            return None
        except cls.DoesNotExist:
            return None

    @property
    def hours_until_expiration(self):
        """Cuántas horas faltan para que expire"""
        if self.isPaid:
            return None  # Las reservas pagadas no expiran
        now = timezone.now()
        time_left = self.expiration_date - now
        return max(0, time_left.total_seconds() / 3600)  # Horas restantes

    @property
    def expiration_status(self):
        """Estado legible de la expiración"""
        if self.isPaid:
            return "Pagada - No expira"
        elif self.is_expired:
            return "Expirada"
        else:
            hours_left = self.hours_until_expiration
            return f"Activa - {hours_left:.1f} horas restantes"
