from datetime import datetime

from django.db import models

from api.models import School


class Company(models.Model):
    name = models.CharField(max_length=100)
    contract = models.IntegerField()
    description = models.CharField(max_length=250, blank=True)
    authorizedPerson = models.CharField(max_length=200, blank=True, null=True)
    dateContractStart = models.DateField()
    dateContractFinish = models.DateField()
    school = models.ForeignKey(School, related_name='companys', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Empresa'
        verbose_name_plural = 'Empresas'
        ordering = ['-id']
