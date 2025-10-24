#!/usr/bin/python3.10

import os
import sys

# Add your project directory to the sys.path
path = '/home/Okemwabrianny/PamojakeBackend'
if path not in sys.path:
    sys.path.insert(0, path)

# Set the Django settings module
os.environ['DJANGO_SETTINGS_MODULE'] = 'pamojabackend.settings_production'

# Import Django and setup
import django
django.setup()

# Import the Django WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()