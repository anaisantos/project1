"""
ASGI config for django_com_oracle_da_anav2 project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'uporto.django_com_oracle_da_anav2.settings')

application = get_asgi_application()
