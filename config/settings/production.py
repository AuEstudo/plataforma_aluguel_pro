import os
import dj_database_url
from .base import *

DEBUG = False

ALLOWED_HOSTS = ['plataforma-aluguel-pro.onrender.com']

# Configurações de segurança para produção
# SECURE_SSL_REDIRECT = True
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True

DATABASES = {
    'default': dj_database_url.config(conn_max_age=600, ssl_require=True)
}

# --- A CORREÇÃO ESTÁ AQUI ---
# Adicionamos a configuração legada STATICFILES_STORAGE para compatibilidade
# com a biblioteca dj3-cloudinary-storage durante o collectstatic.
STATICFILES_STORAGE = 'cloudinary_storage.storage.StaticCloudinaryStorage'

STATIC_ROOT = BASE_DIR / 'staticfiles'

# A configuração moderna STORAGES continua aqui para o WhiteNoise.
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# ==============================================================================
# CONFIGURAÇÃO DO CLOUDINARY PARA ARQUIVOS DE MÍDIA
# ==============================================================================
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.getenv('CLOUDINARY_CLOUD_NAME'),
    'API_KEY': os.getenv('CLOUDINARY_API_KEY'),
    'API_SECRET': os.getenv('CLOUDINARY_API_SECRET'),
}

# Define o Cloudinary como o local de armazenamento padrão para arquivos de mídia (uploads).
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'