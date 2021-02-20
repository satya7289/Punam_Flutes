"""
WSGI config for PunamFlutes project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os
from decouple import config

from django.core.wsgi import get_wsgi_application
if config('DEPLOYMENT', cast=bool, default=False):
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PunamFlutes.deployment')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PunamFlutes.settings')

application = get_wsgi_application()
