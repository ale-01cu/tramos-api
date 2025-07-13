# your_project/apps.py
from django.apps import AppConfig
from django.contrib.auth import get_user_model
import os

class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tramos_api'

    def ready(self):
        from django.conf import settings
        try:
            User = get_user_model()
            default_username = os.getenv('DJANGO_SUPERUSER_USERNAME', 'admin')
            default_email = os.getenv('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
            default_password = os.getenv('DJANGO_SUPERUSER_PASSWORD', 'admin')

            if not User.objects.filter(username=default_username).exists():
                User.objects.create_superuser(
                    username=default_username,
                    email=default_email,
                    password=default_password,
                    role='admin'
                )
                print("✅ Superusuario creado automáticamente.")
            else:
                pass
                # print("⚠️ Superusuario ya existe.")
        except Exception as e:
            print(f"❌ Error al crear el superusuario: {e}")