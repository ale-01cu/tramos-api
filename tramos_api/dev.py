import environ

env = environ.Env()

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': env('DATABASE_NAME'),
        'USER': env('DATABASE_USERNAME'),
        'PASSWORD': env('DATABASE_PASSWORD'),
        'HOST': env('DATABASE_HOST'),
        'PORT': env('DATABASE_PORT'),
    },
}

DEBUG = True
SECRET_KEY = 'django-insecure-gf4c38$1f!en@#i2^#4^9_76&2d-q8z_o4w)f2z=9*)3biz%w)'
# APPEND_SLASH = False
