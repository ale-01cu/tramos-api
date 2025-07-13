from django.db import models

from api.models import School, Municipality, Province


class Classroom(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    capacity = models.IntegerField()
    is_available = models.BooleanField(default=True)
    school = models.ForeignKey(School, related_name='classrooms', on_delete=models.CASCADE)
    address = models.CharField(max_length=100)
    # province = models.ForeignKey(Province, related_name='classrooms', on_delete=models.CASCADE)
    municipality = models.ForeignKey(Municipality, related_name='classrooms', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Aula'
        verbose_name_plural = 'Aulas'
        ordering = ['-id']
