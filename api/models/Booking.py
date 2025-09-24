from django.db import models

from api.models import Client, Offer, Classroom, MultipleBooking, OfferAvailability
from django.utils import timezone
from datetime import timedelta

PAYMENTCHOICES = (
    ('Cash', 'Cash'),
    ('Online', 'Online'),
    ('Check', 'Check'),
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
            (models.Q(isPaid=False) & models.Q(expirationDate__gt=now))
        )
        
    def expired_unpaid(self):
        """Get all unpaid bookings that have expired."""
        now = timezone.now()
        return self.filter(
            isPaid=False,
            expirationDate__lte=now
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
    # classroom = models.ForeignKey(Classroom, related_name='bookings', on_delete=models.CASCADE)
    multipleBooking = models.ForeignKey(MultipleBooking, related_name='bookings', on_delete=models.SET_NULL, blank=True, null=True)
    # priceToPay = models.DecimalField(max_digits=10, decimal_places=2)
    typePayment = models.CharField(choices=PAYMENTCHOICES, default='Check')
    # scheduleOfferDate = models.DateTimeField()
    offerAvailability = models.ForeignKey(OfferAvailability, related_name='bookings', on_delete=models.CASCADE)
    registeredDate = models.DateTimeField(auto_now_add=True) # cuando se registro la reserva
    expirationDate = models.DateTimeField() # los dias que tienes para pagar que son 3 maximo
    # orderGeneratedDate = models.DateTimeField()
    paidDate = models.DateTimeField(blank=True, null=True)
    # isHistory = models.BooleanField(default=False) # cuando paso paso el tiempo permitido para pagar, es decir cuando se termino expirationDate
    isPaid = models.BooleanField(default=False)
    transactionCode = models.CharField(max_length=100)
    versatCode = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    
    objects = BookingManager()

    def save(self, *args, **kwargs):
        # Esta condición `not self.pk` verifica si el objeto es nuevo (aún no tiene una clave primaria).
        # Esto asegura que la lógica solo se ejecute al CREAR la reserva, no al actualizarla.
        if not self.pk:
            now = timezone.now()
            # Asignamos la fecha de expiración: 3 días a partir de ahora.
            self.expirationDate = now + timedelta(days=3)
            # También podemos asignar aquí la fecha de generación de la orden si es el mismo momento.
            self.orderGeneratedDate = now

        # Llamamos al método save() original para que guarde el objeto en la base de datos.
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Reserva para {self.client} en la oferta {self.offer.id}"
        
    def is_expired(self):
        """Check if the booking has expired (passed expiration date and not paid)."""
        now = timezone.now()
        return not self.isPaid and now > self.expirationDate
        
    def is_active(self):
        """Check if the booking is active (paid or not expired yet)."""
        return self.isPaid or not self.is_expired()
        
    @classmethod
    def get_active_booking(cls, booking_id):
        """Get a booking by ID and check if it's active.
        Returns the booking if it's active, or None if expired/inactive.
        """
        try:
            booking = cls.objects.get(id=booking_id)
            if booking.is_active():
                return booking
            return None  # Booking is expired
        except cls.DoesNotExist:
            return None
