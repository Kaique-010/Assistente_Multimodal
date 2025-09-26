import os
import django
from django.conf import settings

def setup_django():
    """Configura Django para uso standalone"""
    if not settings.configured:
        settings.configure(
            DEBUG=True,
            DATABASES={
                'default': {
                    'ENGINE': 'django.db.backends.sqlite3',
                    'NAME': 'db.sqlite3',
                }
            },
            INSTALLED_APPS=[
                'django.contrib.contenttypes',
                'django.contrib.auth',
                'tools',
            ],
            USE_TZ=True,
        )
        django.setup()

if __name__ == "__main__":
    setup_django()