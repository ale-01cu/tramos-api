import secrets
import string
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

from api.models import User


def generate_unique_code():
    length = 4
    characters = string.ascii_uppercase + string.digits
    while True:
        code = ''.join(secrets.choice(characters) for _ in range(length))
        if not User.objects.filter(code=code).exists():
            return code




