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

STATICFILES_STORAGE = 'cloudinary_storage.storage.StaticCloudinaryStorage'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# --- A CORREÇÃO PRINCIPAL ESTÁ AQUI ---
# A configuração moderna STORAGES agora é a fonte única da verdade.
STORAGES = {
    # Define o Cloudinary como o backend para MEDIA files (uploads).
    "default": {
        "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
    },
    # Mantém o WhiteNoise para STATIC files (CSS, JS).
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# Configuração das credenciais que o Cloudinary irá usar
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.getenv('CLOUDINARY_CLOUD_NAME'),
    'API_KEY': os.getenv('CLOUDINARY_API_KEY'),
    'API_SECRET': os.getenv('CLOUDINARY_API_SECRET'),
}

# A linha abaixo é agora redundante e foi removida para evitar conflitos.
# DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# Configuração de LOGGING para vermos os erros em produção
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}
