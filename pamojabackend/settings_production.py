"""
Production settings for PythonAnywhere deployment
"""

from .settings import *

# Production settings
DEBUG = False

ALLOWED_HOSTS = [
    'okemwabrianny.pythonanywhere.com',
    'pamojake.netlify.app',
]

# CORS settings for production
CORS_ALLOWED_ORIGINS = [
    "https://pamojake.netlify.app",
]

# CSRF trusted origins
CSRF_TRUSTED_ORIGINS = [
    "https://pamojake.netlify.app",
]

# Static files settings for PythonAnywhere
STATIC_ROOT = '/home/Okemwabrianny/PamojakeBackend/static'
MEDIA_ROOT = '/home/Okemwabrianny/PamojakeBackend/media'

# Security settings for production
SECURE_SSL_REDIRECT = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Database for production (you can keep SQLite or switch to MySQL)
# For MySQL on PythonAnywhere, uncomment and configure:
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'Okemwabrianny$pamoja',
#         'USER': 'Okemwabrianny',
#         'PASSWORD': 'your_mysql_password',
#         'HOST': 'Okemwabrianny.mysql.pythonanywhere-services.com',
#         'OPTIONS': {
#             'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
#         },
#     }
# }