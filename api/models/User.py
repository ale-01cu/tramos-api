from django.contrib.auth.models import AbstractUser
from django.db import models

from api.models import School

ROLE_CHOICES = (
    ('admin', 'admin'),
    ('gestor', 'gestor'),
    ('comercial', 'comercial'),
    ('observador', 'observador'),
    ('cajero', 'cajero'),
)


class User(AbstractUser):
    groups = None
    first_name = None
    last_name = None
    email = models.EmailField(blank=True, null=True)
    full_name = models.CharField(default='Nombre Completo', max_length=100)
    school = models.ForeignKey(School, related_name='users', on_delete=models.SET_NULL, blank=True, null=True)
    role = models.CharField(choices=ROLE_CHOICES, max_length=20, blank=False, null=False, default='observador')

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        ordering = ['-id']


