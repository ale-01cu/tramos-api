from django.db import models

from api.models import School, Municipality, Province


class Classroom(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    capacity = models.IntegerField()
    is_available = models.BooleanField(default=True)
    school = models.ForeignKey(School, related_name='classrooms', on_delete=models.CASCADE)
    address = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def get_current_bookings(self):
        """Get the current number of active bookings for this classroom."""
        from api.models.Booking import Booking
        return Booking.objects.active().filter(
            offer__classroom=self
        ).count()
    
    def get_available_capacity(self):
        """Get the number of remaining spots in this classroom."""
        current_bookings = self.get_current_bookings()
        return max(0, self.capacity - current_bookings)
    
    def is_full(self):
        """Check if the classroom is at full capacity."""
        current_bookings = self.get_current_bookings()
        return current_bookings >= self.capacity
    
    def can_accommodate(self, additional_bookings=1):
        """Check if the classroom can accommodate additional bookings."""
        current_bookings = self.get_current_bookings()
        return (current_bookings + additional_bookings) <= self.capacity

    class Meta:
        verbose_name = 'Aula'
        verbose_name_plural = 'Aulas'
        ordering = ['-id']
