from django.db import models

SEX_CHOICES = (
    ('None', 'None'),
    ('Female', 'Female'),
    ('Male', 'Male'),
)

TCP_CHOICES = (
    ('PortiadorPrivado', 'PortiadorPrivado'),
    ('Cochero', 'Cochero'),
    ('Bicitaxis', 'Bicitaxis'),
)

CATEGORY_CHOICES = (
    ('Management', 'Management'),
    ('Technical', 'Technical'),
    ('Administrative', 'Administrative'),
    ('Service', 'Service'),
    ('Worker', 'Worker'),
    ('ProfesionalDriver', 'ProfesionalDriver'),
)


class Client(models.Model):
    ci = models.CharField(max_length=11, default='00000000000', unique=True)
    name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=50)
    sex = models.CharField(choices=SEX_CHOICES)
    email = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=20)
    code = models.CharField(max_length=4, unique=True)
    speciality = models.CharField(max_length=50)
    Scholarship = models.CharField(max_length=50)
    company = models.CharField(max_length=50, blank=True, null=True)
    dependence = models.CharField(max_length=50, blank=True, null=True)
    position = models.CharField(max_length=50, blank=True, null=True)
    tcp_category = models.CharField(choices=TCP_CHOICES, blank=True, null=True)
    ocupational_category = models.CharField(choices=CATEGORY_CHOICES, blank=True, null=True)

    def __str__(self):
        return '{} {}'.format(self.name, self.last_name)