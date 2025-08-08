# config/settings/development.py
from .base import *

DEBUG = True

ALLOWED_HOSTS = []

# Direciona todos os e-mails para o console (terminal)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'